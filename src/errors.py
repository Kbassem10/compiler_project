"""LexicalError data contract for Mini Java Compiler.

FROZEN CONTRACT: Immutable error representation.
Do not modify without team-wide review and consensus.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LexicalError:
    """Immutable lexical error diagnostic.
    
    Attributes:
        message: Full formatted diagnostic text,
                 e.g. "Error: invalid character '@' at line 1, column 5."
        line: 1-indexed source line where the offending construct begins.
        column: 1-indexed source column where the offending construct begins.
    """

    message: str
    line: int
    column: int

    def __post_init__(self) -> None:
        """Defensive validation of immutable error fields."""
        if not isinstance(self.message, str):
            raise TypeError(
                f"LexicalError 'message' must be a str, got {type(self.message).__name__}: {self.message!r}"
            )

        if not isinstance(self.line, int) or self.line < 1:
            raise ValueError(
                f"LexicalError 'line' must be a positive 1-indexed integer, got {self.line!r}"
            )

        if not isinstance(self.column, int) or self.column < 1:
            raise ValueError(
                f"LexicalError 'column' must be a positive 1-indexed integer, got {self.column!r}"
            )

    def __repr__(self) -> str:
        # Matches format: LexicalError("Error: invalid character '@' at line 2, column 4.", line=2, column=4)
        return f'LexicalError("{self.message}", line={self.line}, column={self.column})'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LexicalError):
            return False
        return (
            self.message == other.message
            and self.line == other.line
            and self.column == other.column
        )

    def __hash__(self) -> int:
        return hash((self.message, self.line, self.column))
