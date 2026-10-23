from .cursor import SourceCursor
from .token import Token
from .token_type import TokenType
from .errors import LexicalError
from .conventions import OPERATORS, DELIMITERS


# Two-character operators that need lookahead
_TWO_CHAR_OPS = {"==", "!=", "<=", ">="}


def scan_operator_or_delimiter(
    cursor: SourceCursor,
) -> Token | LexicalError:
    line = cursor.getLine()
    col = cursor.getColumn()
    ch = cursor.peek()

    # --- Try two-character operator first ---
    two = ch + cursor.peekNext()
    if two in _TWO_CHAR_OPS:
        cursor.advance()
        cursor.advance()
        return Token(OPERATORS[two], two, line, col)

    # --- Single-character operator ---
    if ch in OPERATORS:
        cursor.advance()
        return Token(OPERATORS[ch], ch, line, col)

    # --- Delimiter ---
    if ch in DELIMITERS:
        cursor.advance()
        return Token(DELIMITERS[ch], ch, line, col)

    # --- Illegal character ---
    cursor.advance()
    return LexicalError(
        f"Error: invalid character '{ch}' at line {line}, column {col}.",
        line=line,
        column=col,
    )
