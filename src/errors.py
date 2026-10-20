from dataclasses import dataclass


@dataclass(frozen=True)
class LexicalError:
    message: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f'LexicalError("{self.message}", line={self.line}, column={self.column})'
