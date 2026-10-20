from dataclasses import dataclass
from .token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f'Token({self.type.name}, "{self.lexeme}", line={self.line}, column={self.column})'
