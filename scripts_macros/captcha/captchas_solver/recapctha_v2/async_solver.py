from __future__ import annotations

import asyncio
import functools
import re
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Any, BinaryIO, Optional, Union
from urllib.parse import parse_qs, urlparse

import speech_recognition
from playwright.async_api import Page, Response
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_delay,
    wait_fixed,
)

from ..errors import (
    RecaptchaNotFoundError,
    RecaptchaRateLimitError,
    RecaptchaSolveError,
)
from .base_solver import BaseSolver
from .recaptcha_box import AsyncRecaptchaBox
from .translations import ORIGINAL_LANGUAGE_AUDIO


class AsyncAudioFile(speech_recognition.AudioFile):
    def __init__(
        self,
        file: Union[BinaryIO, str],
        *,
        executor: Optional[ThreadPoolExecutor] = None,
    ) -> None:
        super().__init__(file)
        self._loop = asyncio.get_running_loop()
        self._executor = executor

    async def __aenter__(self) -> AsyncAudioFile:
        await self._loop.run_in_executor(self._executor, self.__enter__)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._loop.run_in_executor(self._executor, self.__exit__, *args)


class AsyncSolver(BaseSolver[Page]):
    """Async reCAPTCHA v2 solver — audio challenge only."""

    def __init__(self, page: Page, *, attempts: int = 5) -> None:
        super().__init__(page, attempts=attempts)
        self._token_event = asyncio.Event()

    async def __aenter__(self) -> AsyncSolver:
        return self

    async def __aexit__(self, *_: Any) -> None:
        self.close()

    async def _wait_for_token(self, timeout: float) -> str:
        try:
            await asyncio.wait_for(self._token_event.wait(), timeout=timeout)
        except asyncio.TimeoutError as exc:
            raise RecaptchaSolveError("Timed out waiting for reCAPTCHA token.") from exc
        if self._token is None:
            raise RecaptchaSolveError("Token event fired without a token.")
        return self._token

    async def _response_callback(self, response: Response) -> None:
        if (
            re.search("/recaptcha/(api2|enterprise)/payload", response.url) is not None
            and self._payload_response is None
        ):
            self._payload_response = response
        elif re.search("/recaptcha/(api2|enterprise)/userverify", response.url) is not None:
            text = await response.text()
            token_match = re.search('"uvresp","(.*?)"', text)
            if token_match is not None:
                self._token = token_match.group(1)
                self._token_event.set()

    async def _transcribe_audio(
        self, audio_url: str, *, language: str = "en-US"
    ) -> Optional[str]:
        loop = asyncio.get_running_loop()
        response = await self._page.request.get(audio_url)
        wav_audio = BytesIO()
        mp3_audio = BytesIO(await response.body())
        try:
            audio: AudioSegment = await loop.run_in_executor(
                None, AudioSegment.from_mp3, mp3_audio
            )
        except CouldntDecodeError:
            return None
        await loop.run_in_executor(
            None, functools.partial(audio.export, wav_audio, format="wav")
        )
        recognizer = speech_recognition.Recognizer()
        async with AsyncAudioFile(wav_audio) as source:
            audio_data = await loop.run_in_executor(None, recognizer.record, source)
        try:
            return await loop.run_in_executor(
                None,
                functools.partial(
                    recognizer.recognize_google, audio_data, language=language
                ),
            )
        except speech_recognition.UnknownValueError:
            return None

    async def _click_checkbox(self, recaptcha_box: AsyncRecaptchaBox) -> None:
        await recaptcha_box.checkbox.click()
        while recaptcha_box.frames_are_attached() and self._token is None:
            if await recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if await recaptcha_box.any_challenge_is_visible():
                return
            await self._page.wait_for_timeout(250)

    async def _get_audio_url(self, recaptcha_box: AsyncRecaptchaBox) -> str:
        while True:
            if await recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if await recaptcha_box.audio_challenge_is_visible():
                return await recaptcha_box.audio_download_button.get_attribute("href")
            await self._page.wait_for_timeout(250)

    async def _submit_audio_text(
        self, recaptcha_box: AsyncRecaptchaBox, text: str
    ) -> None:
        await recaptcha_box.audio_challenge_textbox.fill(text)
        async with self._page.expect_response(
            re.compile("/recaptcha/(api2|enterprise)/userverify")
        ) as response:
            await recaptcha_box.verify_button.click()
        await response.value
        while recaptcha_box.frames_are_attached():
            if await recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if (
                not await recaptcha_box.audio_challenge_is_visible()
                or await recaptcha_box.solve_failure_is_visible()
                or await recaptcha_box.challenge_is_solved()
            ):
                return
            await self._page.wait_for_timeout(250)

    async def _solve_audio_challenge(self, recaptcha_box: AsyncRecaptchaBox) -> None:
        parsed_url = urlparse(recaptcha_box.anchor_frame.url)
        query_params = parse_qs(parsed_url.query)
        language = (query_params.get("hl") or ["en-US"])[0] or "en-US"
        if language not in ORIGINAL_LANGUAGE_AUDIO:
            language = "en-US"
        while True:
            url = await self._get_audio_url(recaptcha_box)
            text = await self._transcribe_audio(url, language=language)
            if text is not None:
                break
            async with self._page.expect_response(
                re.compile("/recaptcha/(api2|enterprise)/reload")
            ) as response:
                await recaptcha_box.new_challenge_button.click()
            await response.value
            while url == await self._get_audio_url(recaptcha_box):
                await self._page.wait_for_timeout(250)
        await self._submit_audio_text(recaptcha_box, text)

    async def recaptcha_is_visible(self) -> bool:
        try:
            await AsyncRecaptchaBox.from_frames(self._page.frames)
        except RecaptchaNotFoundError:
            return False
        return True

    async def solve_recaptcha(
        self,
        *,
        attempts: Optional[int] = None,
        wait: bool = False,
        wait_timeout: float = 30,
    ) -> str:
        """Solve reCAPTCHA v2 via the audio challenge.

        Image challenges are not supported without a commercial solver service.
        If reCAPTCHA insists on an image challenge (suspicious IP/fingerprint),
        rotate the proxy or IP and retry.
        """
        self._token = None
        self._token_event.clear()
        attempts = attempts or self._attempts

        if wait:
            retry = AsyncRetrying(
                sleep=self._page.wait_for_timeout,
                stop=stop_after_delay(wait_timeout),
                wait=wait_fixed(0.25),
                retry=retry_if_exception_type(RecaptchaNotFoundError),
                reraise=True,
            )
            recaptcha_box = await retry(
                lambda: AsyncRecaptchaBox.from_frames(self._page.frames)
            )
        else:
            recaptcha_box = await AsyncRecaptchaBox.from_frames(self._page.frames)

        if await recaptcha_box.rate_limit_is_visible():
            raise RecaptchaRateLimitError

        if await recaptcha_box.checkbox.is_visible():
            await self._click_checkbox(recaptcha_box)
            if self._token is not None:
                return self._token
            if (
                recaptcha_box.frames_are_detached()
                or not await recaptcha_box.any_challenge_is_visible()
                or await recaptcha_box.challenge_is_solved()
            ):
                return await self._wait_for_token(wait_timeout)

        while not await recaptcha_box.any_challenge_is_visible():
            await self._page.wait_for_timeout(250)

        if await recaptcha_box.audio_challenge_button.is_visible():
            await recaptcha_box.audio_challenge_button.click()
        elif not await recaptcha_box.audio_challenge_is_visible():
            raise RecaptchaSolveError(
                "reCAPTCHA presented an image challenge. Audio-only solver cannot "
                "proceed. Rotate the IP/proxy and retry."
            )

        while attempts > 0:
            self._token = None
            self._token_event.clear()
            await self._solve_audio_challenge(recaptcha_box)
            if (
                recaptcha_box.frames_are_detached()
                or not await recaptcha_box.any_challenge_is_visible()
                or await recaptcha_box.challenge_is_solved()
            ):
                return await self._wait_for_token(wait_timeout)
            attempts -= 1

        raise RecaptchaSolveError
