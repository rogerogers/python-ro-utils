import pytest

from ro_utils.decorator import (
    async_retry_when_error,
    async_retry_when_error_with_params,
    continue_when_error,
    retry_when_error,
    retry_when_error_with_params,
    retry_when_error_with_times,
    singleton,
)


def test_continue_when_error_success():
    @continue_when_error
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


def test_continue_when_error_failure():
    @continue_when_error
    def fail():
        raise ValueError("Something went wrong")

    assert fail() is None


def test_retry_when_error_success_after_retries():
    attempts = 0

    @retry_when_error
    def flaky():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("Temporary error")
        return "success"

    assert flaky() == "success"
    assert attempts == 3


def test_retry_when_error_exhausted():
    attempts = 0

    @retry_when_error
    def always_fail():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Persistent error")

    assert always_fail() is None
    assert attempts == 3


def test_retry_when_error_reraise():
    @retry_when_error(reraise=True)
    def always_fail():
        raise RuntimeError("Fatal error")

    with pytest.raises(RuntimeError, match="Fatal error"):
        always_fail()


@pytest.mark.asyncio
async def test_async_retry_when_error_success():
    attempts = 0

    @async_retry_when_error
    async def flaky_async():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("Async error")
        return "async_ok"

    result = await flaky_async()
    assert result == "async_ok"
    assert attempts == 2


@pytest.mark.asyncio
async def test_async_retry_with_params():
    attempts = 0

    @async_retry_when_error_with_params(max_attempts=2, backoff_factor=0.01)
    async def fail_async():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Exhausted")

    result = await fail_async()
    assert result is None
    assert attempts == 2


def test_retry_when_error_with_params():
    attempts = 0

    @retry_when_error_with_params(times=2, delay=0.01)
    def fail_fn():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Fail")

    assert fail_fn() is None
    assert attempts == 2


def test_retry_when_error_with_times():
    attempts = 0

    @retry_when_error_with_times(times=4)
    def fail_fn():
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Fail")

    assert fail_fn() is None
    assert attempts == 4


def test_singleton():
    @singleton
    class Counter:
        def __init__(self):
            self.count = 0

    c1 = Counter()
    c2 = Counter()
    assert c1 is c2
    c1.count += 1
    assert c2.count == 1
    assert Counter.__name__ == "Counter"
