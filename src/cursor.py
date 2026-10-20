from abc import ABC, abstractmethod


class SourceCursor(ABC):
    @abstractmethod
    def peek(self) -> str:
        """Returns current char, or '\0' at end."""
        pass

    @abstractmethod
    def peekNext(self) -> str:
        """Returns char after current, or '\0' if none."""
        pass

    @abstractmethod
    def advance(self) -> str:
        """Consumes and returns current char, updating line/column."""
        pass

    @abstractmethod
    def isAtEnd(self) -> bool:
        pass

    @abstractmethod
    def getLine(self) -> int:
        """1-indexed line of NEXT char."""
        pass

    @abstractmethod
    def getColumn(self) -> int:
        """1-indexed column of NEXT char."""
        pass
