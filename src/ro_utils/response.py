from typing import Any, TypedDict


class ResponseDict(TypedDict):
    success: bool
    data: Any
    code: int
    message: str
    error: str
    error_code: int


def response(
    success: bool,
    data: Any,
    code: int,
    message: str,
    error: str,
    error_code: int = 0,
) -> ResponseDict:
    """
    Return a dictionary containing the results of the request and the associated error message.

    Parameters:
        success (bool): Indicates whether the request was successful
        data: The data returned by the request
        code (int): HTTP status code indicating the success or failure of the request
        message (str): Text message detailing the request outcome
        error (str): Error message indicating the reason for the request failure
        error_code (int): Error code associated with the error message

    Return:
        ResponseDict: A dictionary containing the response information

    Usage example:
        >>> response(True, {"key": "value"}, 200, "success msg", "", 0)
        {'success': True, 'data': {'key': 'value'}, 'code': 200, 'message': 'success msg', 'error': '', 'error_code': 0}
    """
    return {
        "success": success,
        "data": data,
        "code": code,
        "message": message,
        "error": error,
        "error_code": error_code,
    }


def success(data: Any, code: int = 200) -> ResponseDict:
    """
    Return a success response dictionary.

    Parameters:
        data: The data returned by the request
        code (int): HTTP status code indicating the success of the request

    Return:
        ResponseDict: A dictionary containing the success status, data, and a success message

    Usage example:
        >>> success({"key": "value"}, 200)
        {'success': True, 'data': {'key': 'value'}, 'code': 200, 'message': 'success', 'error': '', 'error_code': 0}
    """
    return response(
        True,
        data,
        code,
        "success",
        "",
    )


def error(
    message: str,
    description: str,
    code: int,
    error_code: int = 0,
) -> ResponseDict:
    """
    Generate a dictionary of error responses.

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        ResponseDict: Error response dictionary

    Usage example:
        >>> error("Request failed", "Server internal error", 500, 5000)
        {'success': False, 'data': None, 'code': 500, 'message': 'Request failed', 'error': 'Server internal error', 'error_code': 5000}
    """
    return response(False, None, code, message, description, error_code)


def client_error(
    message: str,
    description: str = "",
    code: int = 400,
    error_code: int = 0,
) -> ResponseDict:
    """
    Generate a dictionary of client error responses.

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        ResponseDict: Error response dictionary

    Usage example:
        >>> client_error("Request failed", "Parameter error", 400, 1001)
        {'success': False, 'data': None, 'code': 400, 'message': 'Request failed', 'error': 'Parameter error', 'error_code': 1001}
    """
    return error(message, description, code, error_code)


def server_error(
    message: str,
    description: str = "",
    code: int = 500,
    error_code: int = 0,
) -> ResponseDict:
    """
    Generate a dictionary of server error responses.

    Parameters:
        message (str): Error message
        description (str): Error description
        code (int): Status code
        error_code (int): Error code

    Return:
        ResponseDict: Error response dictionary

    Usage example:
        >>> server_error("Request failed", "Server internal error", 500, 5000)
        {'success': False, 'data': None, 'code': 500, 'message': 'Request failed', 'error': 'Server internal error', 'error_code': 5000}
    """
    return error(message, description, code, error_code)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
