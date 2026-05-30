from __future__ import annotations

import re
import time
from io import BytesIO
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

import speech_recognition
from playwright.sync_api import Page, Response
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from tenacity import Retrying, retry_if_exception_type, stop_after_delay, wait_fixed

from ..api_config import require_external_captcha_allowed
from ..errors import (
    RecaptchaNotFoundError,
    RecaptchaRateLimitError,
    RecaptchaSolveError,
)
from .base_solver import BaseSolver
from .recaptcha_box import SyncRecaptchaBox
from .translations import ORIGINAL_LANGUAGE_AUDIO


class SyncSolver(BaseSolver[Page]):
    """Sync reCAPTCHA v2 solver — audio challenge only."""

    def _wait_for_token(self, timeout: float) -> str:
        deadline = time.monotonic() + timeout
        while self._token is None:
            if time.monotonic() >= deadline:
                raise RecaptchaSolveError("Timed out waiting for reCAPTCHA token.")
            self._page.wait_for_timeout(250)
        return self._token

    def __enter__(self) -> SyncSolver:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def _response_callback(self, response: Response) -> None:
        if (
            re.search("/recaptcha/(api2|enterprise)/payload", response.url) is not None
            and self._payload_response is None
        ):
            self._payload_response = response
        elif re.search("/recaptcha/(api2|enterprise)/userverify", response.url) is not None:
            token_match = re.search('"uvresp","(.*?)"', response.text())
            if token_match is not None:
                self._token = token_match.group(1)

    def _transcribe_audio(
        self, audio_url: str, *, language: str = "en-US"
    ) -> Optional[str]:
        # R4: gate the actual egress (see async_solver._transcribe_audio).
        # recognize_google() ships the captcha audio to Google's unofficial
        # Web Speech endpoint; enforce the opt-in here so a direct SyncSolver
        # user cannot bypass CAMOU_CAPTCHA_ALLOW_EXTERNAL.
        require_external_captcha_allowed("Google Web Speech API (reCAPTCHA audio)")
        response = self._page.request.get(audio_url)
        wav_audio = BytesIO()
        mp3_audio = BytesIO(response.body())
        try:
            audio: AudioSegment = AudioSegment.from_mp3(mp3_audio)
        except CouldntDecodeError:
            return None
        audio.export(wav_audio, format="wav")
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(wav_audio) as source:
            audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language=language)
        except speech_recognition.UnknownValueError:
            return None

    def _click_checkbox(self, recaptcha_box: SyncRecaptchaBox) -> None:
        recaptcha_box.checkbox.click()
        while recaptcha_box.frames_are_attached() and self._token is None:
            if recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if recaptcha_box.any_challenge_is_visible():
                return
            self._page.wait_for_timeout(250)

    def _get_audio_url(self, recaptcha_box: SyncRecaptchaBox) -> str:
        while True:
            if recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if recaptcha_box.audio_challenge_is_visible():
                return recaptcha_box.audio_download_button.get_attribute("href")
            self._page.wait_for_timeout(250)

    def _submit_audio_text(self, recaptcha_box: SyncRecaptchaBox, text: str) -> None:
        recaptcha_box.audio_challenge_textbox.fill(text)
        with self._page.expect_response(
            re.compile("/recaptcha/(api2|enterprise)/userverify")
        ):
            recaptcha_box.verify_button.click()
        while recaptcha_box.frames_are_attached():
            if recaptcha_box.rate_limit_is_visible():
                raise RecaptchaRateLimitError
            if (
                not recaptcha_box.audio_challenge_is_visible()
                or recaptcha_box.solve_failure_is_visible()
                or recaptcha_box.challenge_is_solved()
            ):
                return
            self._page.wait_for_timeout(250)

    def _solve_audio_challenge(self, recaptcha_box: SyncRecaptchaBox) -> None:
        parsed_url = urlparse(recaptcha_box.anchor_frame.url)
        query_params = parse_qs(parsed_url.query)
        language = (query_params.get("hl") or ["en-US"])[0] or "en-US"
        if language not in ORIGINAL_LANGUAGE_AUDIO:
            language = "en-US"
        while True:
            url = self._get_audio_url(recaptcha_box)
            text = self._transcribe_audio(url, language=language)
            if text is not None:
                break
            with self._page.expect_response(
                re.compile("/recaptcha/(api2|enterprise)/reload")
            ):
                recaptcha_box.new_challenge_button.click()
            while url == self._get_audio_url(recaptcha_box):
                self._page.wait_for_timeout(250)
        self._submit_audio_text(recaptcha_box, text)

    def recaptcha_is_visible(self) -> bool:
        try:
            SyncRecaptchaBox.from_frames(self._page.frames)
        except RecaptchaNotFoundError:
            return False
        return True

    def solve_recaptcha(
        self,
        *,
        attempts: Optional[int] = None,
        wait: bool = False,
        wait_timeout: float = 30,
    ) -> str:
        """Solve reCAPTCHA v2 via the audio challenge.

        Image challenges are not supported without a commercial solver service.
        """
        self._token = None
        attempts = attempts or self._attempts

        if wait:
            retry = Retrying(
                sleep=self._page.wait_for_timeout,
                stop=stop_after_delay(wait_timeout),
                wait=wait_fixed(0.25),
                retry=retry_if_exception_type(RecaptchaNotFoundError),
                reraise=True,
            )
            recaptcha_box = retry(
                lambda: SyncRecaptchaBox.from_frames(self._page.frames)
            )
        else:
            recaptcha_box = SyncRecaptchaBox.from_frames(self._page.frames)

        if recaptcha_box.rate_limit_is_visible():
            raise RecaptchaRateLimitError

        if recaptcha_box.checkbox.is_visible():
            self._click_checkbox(recaptcha_box)
            if self._token is not None:
                return self._token
            if (
                recaptcha_box.frames_are_detached()
                or not recaptcha_box.any_challenge_is_visible()
                or recaptcha_box.challenge_is_solved()
            ):
                return self._wait_for_token(wait_timeout)

        while not recaptcha_box.any_challenge_is_visible():
            self._page.wait_for_timeout(250)

        if recaptcha_box.audio_challenge_button.is_visible():
            recaptcha_box.audio_challenge_button.click()
        elif not recaptcha_box.audio_challenge_is_visible():
            raise RecaptchaSolveError(
                "reCAPTCHA presented an image challenge. Audio-only solver cannot "
                "proceed. Rotate the IP/proxy and retry."
            )

        while attempts > 0:
            self._token = None
            self._solve_audio_challenge(recaptcha_box)
            if (
                recaptcha_box.frames_are_detached()
                or not recaptcha_box.any_challenge_is_visible()
                or recaptcha_box.challenge_is_solved()
            ):
                return self._wait_for_token(wait_timeout)
            attempts -= 1

        raise RecaptchaSolveError
