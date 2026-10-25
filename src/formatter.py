from .errors import LexicalError
from .symbol_table import SymbolTable
from .token import Token
from .token_type import TokenType


def format_token(token: Token) -> str:
    # EOF has no source text, so its lexeme is printed as "EOF"
    lexeme = "EOF" if token.type is TokenType.EOF else token.lexeme
    return f"Lexeme: {lexeme}, Token: {token.type.name}"


def format_symbol_table(table: SymbolTable) -> list[str]:
    lines = ["Symbol Table"]
    if len(table) == 0:
        lines.append("(empty)")
    for entry in table.entries():
        places = ", ".join(f"{line}:{column}" for line, column in entry.occurrences)
        lines.append(f"Index: {entry.index}, Name: {entry.name}, Occurrences: {places}")
    return lines


def format_output(tokens: list[Token], errors: list[LexicalError], table: SymbolTable) -> str:
    # Sort tokens and errors together by position, so every error
    # is printed exactly where it happened in the source.
    items = sorted(tokens + errors, key=lambda item: (item.line, item.column))

    lines = []
    for item in items:
        if isinstance(item, LexicalError):
            lines.append(item.message)
        else:
            lines.append(format_token(item))

    lines.append("")
    lines.extend(format_symbol_table(table))
    return "\n".join(lines) + "\n"
