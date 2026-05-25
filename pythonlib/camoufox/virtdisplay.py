import os
import subprocess  # nosec
import time
from shutil import which
from threading import Lock
from typing import List, Optional

from camoufox.exceptions import (
    CannotExecuteXvfb,
    CannotFindXvfb,
    VirtualDisplayError,
    VirtualDisplayNotSupported,
)
from camoufox.pkgman import OS_NAME

DISPLAY_LOCK = Lock()


class VirtualDisplay:
    """
    A minimal virtual display implementation for Linux.

    Uses Xvfb's ``-displayfd`` flag (xorg-server >= 1.13, 2012) so the
    server atomically picks a free display, claims its X11 lockfile and
    reports the chosen number back through a pipe. This removes the
    previous retry-loop-on-random-numbers approach (PR #618 upstream),
    which had a TOCTOU race between two parallel Camoufox launches that
    happened to roll the same display in their respective
    ``_free_display`` reads.
    """

    def __init__(self, debug: Optional[bool] = False) -> None:
        """
        Constructor for the VirtualDisplay class (singleton object).
        """
        self.debug = debug
        self.proc: Optional[subprocess.Popen] = None
        self._display: Optional[int] = None
        self._lock = Lock()

    # First display number Xvfb is allowed to claim. Vanilla X servers
    # default to :0/:1 (real X), so we start the search at :99 to stay
    # out of their way and keep parity with the historical Camoufox
    # behaviour.
    _STARTING_DISPLAY = 99
    _DISPLAYFD_READ_TIMEOUT = 5.0
    _TERMINATE_TIMEOUT = 5

    xvfb_args = (
        # fmt: off
        "-screen", "0", "1x1x24",
        "-ac",
        "-nolisten", "tcp",
        "-extension", "RENDER",
        "+extension", "GLX",
        "-extension", "COMPOSITE",
        "-extension", "XVideo",
        "-extension", "XVideo-MotionCompensation",
        "-extension", "XINERAMA",
        "-shmem",
        "-fp", "built-ins",
        "-nocursor",
        "-br",
        # fmt: on
    )

    @property
    def xvfb_path(self) -> str:
        """
        Get the path to the xvfb executable
        """
        path = which("Xvfb")
        if not path:
            raise CannotFindXvfb("Please install Xvfb to use headless mode.")
        if not os.access(path, os.X_OK):
            raise CannotExecuteXvfb(f"I do not have permission to execute Xvfb: {path}")
        return path

    def xvfb_cmd(self, displayfd: int) -> List[str]:
        """
        Build the Xvfb command line. ``-displayfd <fd>`` makes Xvfb
        atomically pick a free display starting from ``_STARTING_DISPLAY``
        and report the chosen number back through that file descriptor.
        """
        return [
            self.xvfb_path,
            "-displayfd",
            str(displayfd),
            "-displaynum",
            str(self._STARTING_DISPLAY),
            *self.xvfb_args,
        ]

    def execute_xvfb(self) -> None:
        """
        Spawn Xvfb and read the chosen display number back through the
        ``-displayfd`` pipe. The pipe avoids the race that the old
        retry-on-random-number loop had: two concurrent VirtualDisplay
        instances cannot collide because Xvfb itself handles the X11
        lockfile contention.
        """
        r_fd, w_fd = os.pipe()
        try:
            cmd = self.xvfb_cmd(w_fd)
            if self.debug:
                print('Starting virtual display:', ' '.join(cmd))

            proc = subprocess.Popen(  # nosec
                cmd,
                stdout=None if self.debug else subprocess.DEVNULL,
                stderr=None if self.debug else subprocess.DEVNULL,
                pass_fds=(w_fd,),
                close_fds=True,
            )
        except OSError as exc:
            os.close(r_fd)
            os.close(w_fd)
            raise CannotExecuteXvfb(f"Failed to spawn Xvfb: {exc}") from exc

        # Xvfb keeps `w_fd` open and writes the chosen display number to
        # it once the server is ready. Close our end so EOF propagates
        # if Xvfb crashes before writing.
        os.close(w_fd)

        try:
            display = self._read_display_number(r_fd, proc)
        except Exception:
            os.close(r_fd)
            # Make sure we never leak the child process / let it become
            # a zombie if reading the display number failed.
            self._reap_proc(proc)
            raise
        finally:
            try:
                os.close(r_fd)
            except OSError:
                pass

        self.proc = proc
        self._display = display

    def _read_display_number(
        self, r_fd: int, proc: subprocess.Popen
    ) -> int:
        """
        Block until Xvfb writes the chosen display number (followed by
        a newline) to ``r_fd`` and parse the result. If Xvfb exits
        before writing — or writes garbage — raise CannotExecuteXvfb.
        """
        deadline = time.monotonic() + self._DISPLAYFD_READ_TIMEOUT
        buf = b""
        while True:
            if proc.poll() is not None and not buf:
                raise CannotExecuteXvfb(
                    f"Xvfb exited with code {proc.returncode} before reporting a display number."
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise CannotExecuteXvfb(
                    "Timed out waiting for Xvfb to report a display number "
                    f"(after {self._DISPLAYFD_READ_TIMEOUT:.1f}s)."
                )
            try:
                chunk = os.read(r_fd, 16)
            except (BlockingIOError, InterruptedError):
                time.sleep(0.05)
                continue
            if not chunk:
                # EOF — Xvfb closed the fd. Either it printed the
                # number already (in `buf`) or it exited prematurely.
                break
            buf += chunk
            if b"\n" in buf:
                break

        token = buf.strip()
        if not token:
            raise CannotExecuteXvfb(
                "Xvfb closed -displayfd without writing a display number "
                f"(return code: {proc.returncode})."
            )
        try:
            return int(token)
        except ValueError:
            raise CannotExecuteXvfb(
                f"Xvfb wrote non-numeric data on -displayfd: {token!r}"
            )

    def get(self) -> str:
        """
        Get the display number
        """
        self.assert_linux()

        with self._lock:
            if self.proc is None:
                with DISPLAY_LOCK:
                    self.execute_xvfb()
            elif self.debug:
                print(f'Using virtual display: {self.display}')
            return f':{self.display}'

    def _reap_proc(self, proc: subprocess.Popen) -> None:
        """
        Terminate ``proc`` if it is still alive and always call
        ``wait()`` afterwards so it does not become a <defunct> zombie.
        Safe to call multiple times.
        """
        if proc.poll() is None:
            try:
                proc.terminate()
            except OSError:
                pass
            try:
                proc.wait(timeout=self._TERMINATE_TIMEOUT)
            except subprocess.TimeoutExpired:
                try:
                    proc.kill()
                except OSError:
                    pass
                try:
                    proc.wait(timeout=self._TERMINATE_TIMEOUT)
                except subprocess.TimeoutExpired:
                    # Last-ditch: give the kernel time to deliver SIGKILL.
                    # If we still cannot reap, give up to avoid blocking
                    # the launcher; the OS will reap it once we exit.
                    return
        else:
            # Process already exited but its status may not have been
            # collected yet (the canonical zombie-prevention pattern
                # — see PR #618).
            try:
                proc.wait(timeout=self._TERMINATE_TIMEOUT)
            except subprocess.TimeoutExpired:
                return

    def kill(self):
        """
        Terminate the xvfb process and reap it. Idempotent.
        """
        with self._lock:
            proc = self.proc
            display = self._display
            self.proc = None
            self._display = None

            if proc is None:
                return
            if self.debug:
                print('Terminating virtual display:', display)
            self._reap_proc(proc)

    def __del__(self):
        """
        Kill and delete the VirtualDisplay object.
        Wraps everything in a defensive try/except so interpreter
        shutdown noise (modules torn down, ``os`` already gone) cannot
        leak a CleanupError that masks the real exit cause.
        """
        try:
            self.kill()
        except Exception:
            pass

    @property
    def display(self) -> int:
        """
        Get the display number
        """
        if self._display is None:
            raise VirtualDisplayError("Virtual display has not been started yet.")
        return self._display

    @staticmethod
    def assert_linux():
        """
        Assert that the current OS is Linux
        """
        if OS_NAME != 'lin':
            raise VirtualDisplayNotSupported("Virtual display is only supported on Linux.")
