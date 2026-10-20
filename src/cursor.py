"""SourceCursor interface contract for Mini Java Compiler.

FROZEN CONTRACT: Abstract interface with no implementation logic.
Task 2 will implement this contract.
"""

from abc import ABC, abstractmethod


class SourceCursor(ABC):
    """Abstract cursor interface for character stream traversal.
    
    All methods defined here are abstract and must be implemented by concrete
    classes (Task 2). This contract specifies expected signatures, semantics,
    and sentinel invariants.
    """

    SENTINEL: str = "\0"

    @abstractmethod
    def peek(self) -> str:
        """Returns the current character without consuming it.
        
        Returns:
            Current character string, or '\0' (sentinel) if at or past EOF.
            Must never raise an exception when at EOF.
        """
        raise NotImplementedError

    @abstractmethod
    def peekNext(self) -> str:
        """Returns the character immediately after the current one without consuming.
        
        Returns:
            Next character string, or '\0' (sentinel) if at end or past end.
            Must never raise an exception when at or past EOF.
        """
        raise NotImplementedError

    @abstractmethod
    def advance(self) -> str:
        """Consumes and returns the current character, updating line and column counters.
        
        Returns:
            The consumed character string, or '\0' if already at EOF.
        """
        raise NotImplementedError

    @abstractmethod
    def isAtEnd(self) -> bool:
        """Checks if the cursor has reached or surpassed the end of the input source.
        
        Returns:
            True if at or past the end of input; False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def getLine(self) -> int:
        """Gets the 1-indexed line number of the NEXT character to be read.
        
        Returns:
            1-indexed line number (int >= 1).
        """
        raise NotImplementedError

    @abstractmethod
    def getColumn(self) -> int:
        """Gets the 1-indexed column number of the NEXT character to be read.
        
        Returns:
            1-indexed column number (int >= 1).
        """
        raise NotImplementedError
