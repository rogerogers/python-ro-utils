import http.cookies


def parse_cookie_str(cookie_str: str) -> dict[str, str]:
    """
    Convert a cookie string to a dictionary.
    """
    cookies = http.cookies.SimpleCookie()
    cookies.load(cookie_str)
    return {k: v.value for k, v in cookies.items()}
