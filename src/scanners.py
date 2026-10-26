from src.cursor import SourceCursor
from src.token import Token
from src.token_type import TokenType
from src.errors import LexicalError
from src.conventions import KEYWORDS


def scan_word_or_number_or_string(
    cursor: SourceCursor
) -> Token | LexicalError | None:
    """
    Sub-scanner for Task 3: Handles Words (Keywords/Identifiers),
    Numbers (Int/Float), Invalid Identifiers, and Strings.
    Returns Token, LexicalError, or None if no match.
    """
    ch = cursor.peek()

    # 1. String Literals (Double or Single quotes)
    if ch in ('"', "'"):
        return scan_string(cursor)

    # 2. Invalid Identifier Case: Starts with digit but followed by letters/underscore
    if ch.isdigit():
        return scan_number_or_invalid_id(cursor)

    # 3. Words: Keywords vs Identifiers (Starts with letter or '_')
    if ch.isalpha() or ch == '_':
        return scan_word(cursor)

    return None


def scan_word(cursor: SourceCursor) -> Token:
    line = cursor.getLine()
    col = cursor.getColumn()
    lexeme = []

    while cursor.peek().isalnum() or cursor.peek() == '_':
        lexeme.append(cursor.advance())

    lexeme_str = "".join(lexeme)
    token_type = KEYWORDS.get(lexeme_str, TokenType.IDENTIFIER)

    return Token(type=token_type, lexeme=lexeme_str, line=line, column=col)


def scan_number_or_invalid_id(cursor: SourceCursor) -> Token | LexicalError:
    line = cursor.getLine()
    col = cursor.getColumn()
    lexeme = []

    # Read leading digits
    while cursor.peek().isdigit():
        lexeme.append(cursor.advance())

    # Check for invalid identifier (e.g. 1name, 10_total)
    if cursor.peek().isalpha() or cursor.peek() == '_':
        while cursor.peek().isalnum() or cursor.peek() == '_':
            lexeme.append(cursor.advance())
        invalid_id = "".join(lexeme)
        return LexicalError(
            message=f"Error: invalid identifier '{invalid_id}' at line {line}, column {col}.",
            line=line,
            column=col
        )

    # Check for Floating Point Number (e.g. 25.5)
    if cursor.peek() == '.' and cursor.peekNext().isdigit():
        lexeme.append(cursor.advance())  # consume '.'
        while cursor.peek().isdigit():
            lexeme.append(cursor.advance())

    return Token(type=TokenType.NUMBER, lexeme="".join(lexeme), line=line, column=col)


def scan_string(cursor: SourceCursor) -> Token | LexicalError:
    line = cursor.getLine()
    col = cursor.getColumn()
    quote_char = cursor.advance()  # Consume opening quote (' or ")
    lexeme = [quote_char]

    # A string cannot span lines, so stop at the end of the line too
    while not cursor.isAtEnd() and cursor.peek() not in (quote_char, '\n', '\r'):
        # Handle escape characters like \" or \n if present
        if cursor.peek() == '\\' and cursor.peekNext() not in ('\0', '\n', '\r'):
            lexeme.append(cursor.advance())
        lexeme.append(cursor.advance())

    if cursor.peek() != quote_char:
        return LexicalError(
            message=f"Error: unclosed string literal starting at line {line}, column {col}.",
            line=line,
            column=col
        )

    lexeme.append(cursor.advance())  # Consume closing quote
    return Token(type=TokenType.STRING, lexeme="".join(lexeme), line=line, column=col)