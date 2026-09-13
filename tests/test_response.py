from ro_utils.response import (
    client_error,
    error,
    response,
    server_error,
    success,
)


def test_response_custom():
    res = response(
        success=True,
        data={"user": "alice"},
        code=200,
        message="ok",
        error="",
        error_code=0,
    )
    assert res == {
        "success": True,
        "data": {"user": "alice"},
        "code": 200,
        "message": "ok",
        "error": "",
        "error_code": 0,
    }


def test_success():
    res = success(data=[1, 2, 3])
    assert res["success"] is True
    assert res["data"] == [1, 2, 3]
    assert res["code"] == 200
    assert res["message"] == "success"
    assert res["error"] == ""
    assert res["error_code"] == 0


def test_error():
    res = error(
        message="Failed",
        description="Something broke",
        code=500,
        error_code=5001,
    )
    assert res["success"] is False
    assert res["data"] is None
    assert res["code"] == 500
    assert res["message"] == "Failed"
    assert res["error"] == "Something broke"
    assert res["error_code"] == 5001


def test_client_error():
    res = client_error("Invalid parameters", description="Missing id")
    assert res["success"] is False
    assert res["code"] == 400
    assert res["message"] == "Invalid parameters"
    assert res["error"] == "Missing id"


def test_server_error():
    res = server_error("Internal error", description="DB connection failed")
    assert res["success"] is False
    assert res["code"] == 500
    assert res["message"] == "Internal error"
    assert res["error"] == "DB connection failed"
