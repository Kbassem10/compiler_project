from .cursor import FileCursor
from .errors import LexicalError
from .scanner_delimiters import scan_operator_or_delimiter
from .scanners import scan_word_or_number_or_string
from .symbol_table import SymbolTable
from .token import Token
from .token_type import TokenType


# Minimal main loop so the CLI can run end to end.
# Task 7 owns this file and may extend or replace it.
def tokenize(source: str) -> tuple[list[Token], list[LexicalError], SymbolTable]:
    cursor = FileCursor(source)
    tokens: list[Token] = []
    errors: list[LexicalError] = []
    table = SymbolTable()

    while True:
        comment_error = cursor.skip_whitespace_and_comments()
        if comment_error:
            errors.append(comment_error)
        if cursor.isAtEnd():
            break

        # Words, numbers and strings first; anything else is an operator,
        # a delimiter, or an illegal character.
        item = scan_word_or_number_or_string(cursor)
        if item is None:
            item = scan_operator_or_delimiter(cursor)

        if isinstance(item, LexicalError):
            errors.append(item)
        else:
            tokens.append(item)
            if item.type is TokenType.IDENTIFIER:
                table.insert(item)

    tokens.append(Token(TokenType.EOF, "", cursor.getLine(), cursor.getColumn()))
    return tokens, errors, table
