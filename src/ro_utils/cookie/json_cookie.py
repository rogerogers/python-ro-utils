import json
from typing import Any

from .base import CookieBase


class JSONCookie(CookieBase):
    def __init__(self, cookie_str: str) -> None:
        self.cookie_str = cookie_str

    def to_cookie(self) -> dict[str, Any]:
        return json.loads(self.cookie_str)
