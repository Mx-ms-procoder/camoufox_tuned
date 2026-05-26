from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, Union

from playwright.async_api import APIResponse as AsyncAPIResponse
from playwright.async_api import Page as AsyncPage
from playwright.async_api import Response as AsyncResponse
from playwright.sync_api import APIResponse as SyncAPIResponse
from playwright.sync_api import Page as SyncPage
from playwright.sync_api import Response as SyncResponse

from .recaptcha_box import RecaptchaBox

PageT = TypeVar("PageT", AsyncPage, SyncPage)
APIResponse = Union[AsyncAPIResponse, SyncAPIResponse]
Response = Union[AsyncResponse, SyncResponse]


class BaseSolver(ABC, Generic[PageT]):
    """Base class for reCAPTCHA v2 audio-challenge solvers.

    Image challenges are not supported — audio is the only path that
    does not require a commercial third-party service.
    """

    def __init__(self, page: PageT, *, attempts: int = 5) -> None:
        self._page = page
        self._attempts = attempts
        self._token: Optional[str] = None
        self._payload_response: Union[APIResponse, Response, None] = None
        self._page.on("response", self._response_callback)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(page={self._page!r}, "
            f"attempts={self._attempts!r})"
        )

    def close(self) -> None:
        try:
            self._page.remove_listener("response", self._response_callback)
        except Exception:
            pass

    @abstractmethod
    def _response_callback(self, response: Response) -> None:
        """Intercept payload and userverify responses."""

    @abstractmethod
    def _transcribe_audio(self, audio_url: str, *, language: str) -> Optional[str]:
        """Transcribe the reCAPTCHA audio challenge URL to text."""

    @abstractmethod
    def _click_checkbox(self, recaptcha_box: RecaptchaBox) -> None:
        """Click the reCAPTCHA checkbox."""

    @abstractmethod
    def _get_audio_url(self, recaptcha_box: RecaptchaBox) -> str:
        """Return the audio download URL from the challenge frame."""

    @abstractmethod
    def _submit_audio_text(self, recaptcha_box: RecaptchaBox, text: str) -> None:
        """Fill and submit the audio response text."""

    @abstractmethod
    def _solve_audio_challenge(self, recaptcha_box: RecaptchaBox) -> None:
        """Drive the full audio-challenge solve loop."""

    @abstractmethod
    def recaptcha_is_visible(self) -> bool:
        """Return True if an unsolved reCAPTCHA is visible on the page."""

    @abstractmethod
    def solve_recaptcha(
        self,
        *,
        attempts: Optional[int] = None,
        wait: bool = False,
        wait_timeout: float = 30,
    ) -> str:
        """Solve the reCAPTCHA and return the g-recaptcha-response token."""
