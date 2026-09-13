"""ro-utils: daily Python utilities."""

from ro_utils.cookie import CookieBase, JSONCookie, TextCookie, parse_cookie_str
from ro_utils.debug import pprint
from ro_utils.decorator import (
    async_retry_when_error,
    async_retry_when_error_with_params,
    continue_when_error,
    retry_when_error,
    retry_when_error_with_params,
    retry_when_error_with_times,
    singleton,
)
from ro_utils.response import (
    ResponseDict,
    client_error,
    error,
    response,
    server_error,
    success,
)

__version__ = "0.5.0"

__all__ = [
    "CookieBase",
    "JSONCookie",
    "ResponseDict",
    "TextCookie",
    "__version__",
    "async_retry_when_error",
    "async_retry_when_error_with_params",
    "client_error",
    "continue_when_error",
    "error",
    "parse_cookie_str",
    "pprint",
    "response",
    "retry_when_error",
    "retry_when_error_with_params",
    "retry_when_error_with_times",
    "server_error",
    "singleton",
    "success",
]
