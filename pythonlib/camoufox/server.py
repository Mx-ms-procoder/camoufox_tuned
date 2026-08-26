import subprocess
from pathlib import Path
from typing import Any, Dict, NoReturn

import base64
import orjson
from playwright._impl._driver import compute_driver_executable

from camoufox.pkgman import LOCAL_DATA
from camoufox.utils import launch_options

LAUNCH_SCRIPT: Path = LOCAL_DATA / "launchServer.js"


def camel_case(snake_str: str) -> str:
    """
    Convert a string to camelCase
    """
    if len(snake_str) < 2:
        return snake_str
    camel_case_str = ''.join(x.capitalize() for x in snake_str.lower().split('_'))
    # A leading underscore is meaningful (private option names round-trip through
    # here); ''.split('_') drops it, so put it back.
    return ("_" if snake_str[0] == "_" else "") + camel_case_str[0].lower() + camel_case_str[1:]


def to_camel_case_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a dictionary to camelCase
    """
    return {camel_case(key): value for key, value in data.items()}


def get_nodejs() -> str:
    """
    Get the bundled Node.js executable
    """
    # Note: Older versions of Playwright return a string rather than a tuple.
    _nodejs = compute_driver_executable()
    if isinstance(_nodejs, tuple):
        return _nodejs[0]
    return _nodejs


def launch_server(**kwargs) -> NoReturn:
    """
    Launch a Playwright server. Takes the same arguments as `Camoufox()`.
    Prints the websocket endpoint to the console.

    Note: persistent contexts are not servable. Playwright's `launchServer`
    routes through `BrowserType.launch()`, and its `PlaywrightServer` only
    accepts a `preLaunchedBrowser` -- there is no way to expose a persistent
    `BrowserContext` over a websocket endpoint. Reject those options up front
    rather than accepting them and silently launching a throwaway profile,
    which looks like a working persistent session until the cookies are gone.
    """
    for unsupported in ('persistent_context', 'user_data_dir'):
        if kwargs.get(unsupported):
            raise ValueError(
                f"launch_server() does not support {unsupported!r}: Playwright cannot "
                "serve a persistent context over a websocket endpoint. Use "
                "Camoufox(persistent_context=True, ...) in-process instead."
            )
        kwargs.pop(unsupported, None)

    config = launch_options(**kwargs)
    nodejs = get_nodejs()

    data = orjson.dumps(to_camel_case_dict(config))

    process = subprocess.Popen(  # nosec
        [
            nodejs,
            str(LAUNCH_SCRIPT),
        ],
        cwd=Path(nodejs).parent / "package",
        stdin=subprocess.PIPE,
        text=True,
    )
    # Write data to stdin and close the stream
    if process.stdin:
        process.stdin.write(base64.b64encode(data).decode())
        process.stdin.close()

    # Wait forever
    process.wait()

    # Add an explicit return statement to satisfy the NoReturn type hint
    raise RuntimeError("Server process terminated unexpectedly")
