"""Token data contract for Mini Java Compiler.

FROZEN CONTRACT: Immutable token representation.
Do not modify without team-wide review and consensus.
"""

from dataclasses import dataclass
from typing import Any
from .token_type import TokenType


@dataclass(frozen=True)
class Token:
    """Immutable lexical token representation.
    
    Attributes:
        type: The category of the token (TokenType enum member).
        lexeme: The exact raw source characters representing this token.
        line: 1-indexed source line where the first character begins.
        column: 1-indexed source column where the first character begins.
    """

    type: TokenType
    lexeme: str
    line: int
    column: int

    def __post_init__(self) -> None:
        """Defensive validation of immutable token fields."""
        if not isinstance(self.type, TokenType):
            # Allow string coercion if valid token name, otherwise fail fast
            if isinstance(self.type, str) and hasattr(TokenType, self.type):
                object.__setattr__(self, "type", TokenType[self.type])
            else:
                raise TypeError(
                    f"Token 'type' must be an instance of TokenType, got {type(self.type).__name__}: {self.type!r}"
                )

        if not isinstance(self.lexeme, str):
            raise TypeError(
                f"Token 'lexeme' must be a str, got {type(self.lexeme).__name__}: {self.lexeme!r}"
            )

        if not isinstance(self.line, int) or self.line < 1:
            raise ValueError(
                f"Token 'line' must be a positive 1-indexed integer, got {self.line!r}"
            )

        if not isinstance(self.column, int) or self.column < 1:
            raise ValueError(
                f"Token 'column' must be a positive 1-indexed integer, got {self.column!r}"
            )

    def __repr__(self) -> str:
        # Matches format: Token(CLASS, "class", line=1, column=1)
        return f'Token({self.type.name}, "{self.lexeme}", line={self.line}, column={self.column})'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.lexeme == other.lexeme
            and self.line == other.line
            and self.column == other.column
        )

    def __hash__(self) -> int:
        return hash((self.type, self.lexeme, self.line, self.column))
