from .base import CookieBase
from .parser import parse_cookie_str


class TextCookie(CookieBase):
    def __init__(self, cookie_str: str) -> None:
        self.cookie_str = cookie_str

    def to_cookie(self) -> dict[str, str]:
        return parse_cookie_str(self.cookie_str)
