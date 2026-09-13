from abc import ABC, abstractmethod
from typing import Any


class CookieBase(ABC):
    @abstractmethod
    def to_cookie(self) -> dict[str, Any]:
        """Convert cookie to dictionary."""
        pass
