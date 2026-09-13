from ro_utils.cookie import JSONCookie, TextCookie, parse_cookie_str


def test_parse_cookie_str():
    cookie_str = "sessionid=xyz123; theme=dark; token=abc"
    result = parse_cookie_str(cookie_str)
    assert result == {"sessionid": "xyz123", "theme": "dark", "token": "abc"}


def test_text_cookie():
    cookie_str = "user_id=42; lang=zh"
    cookie = TextCookie(cookie_str)
    assert cookie.to_cookie() == {"user_id": "42", "lang": "zh"}


def test_json_cookie():
    cookie_str = '{"session_id": "s123", "logged_in": "true"}'
    cookie = JSONCookie(cookie_str)
    assert cookie.to_cookie() == {"session_id": "s123", "logged_in": "true"}
