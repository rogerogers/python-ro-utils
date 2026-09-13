import pprint as _py_pprint
from typing import Any


def pprint(obj: Any, *args: Any, **kwargs: Any) -> None:
    """
    Pretty-print an object with optional formatting arguments.
    """
    _py_pprint.pprint(obj, *args, **kwargs)
