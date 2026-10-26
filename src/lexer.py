from collections.abc import Callable, Iterator

from .cursor import FileCursor, SourceCursor, skip_whitespace_and_comments
from .errors import LexicalError
from .scanner_delimiters import scan_operator_or_delimiter
from .scanners import scan_number_or_invalid_id, scan_string, scan_word
from .symbol_table import SymbolTable
from .token import Token
from .token_type import TokenType


class Lexer:
    """Mini Java Lexical Analyzer (Scanner).

    Coordinates the SourceCursor, sub-scanners, SymbolTable,
    and LexicalErrors into a single unified token stream.
    """

    def __init__(
        self,
        source: str | SourceCursor,
        on_token: Callable[[Token], None] | None = None,
        on_error: Callable[[LexicalError], None] | None = None,
    ):
        if isinstance(source, SourceCursor):
            self.cursor = source
        else:
            self.cursor = FileCursor(source)

        self.on_token = on_token
        self.on_error = on_error

        self.tokens: list[Token] = []
        self.errors: list[LexicalError] = []
        self.symbol_table = SymbolTable()
        self._eof_token: Token | None = None

    def getNextToken(self) -> Token:
        """Returns the next Token in the source stream.

        Skips whitespace and comments, dispatches to sub-scanners based on
        the current character, records any lexical errors, updates the
        symbol table for identifiers, and returns Token(EOF, ...) once the
        end of source is reached. Never returns an error object.
        """
        if self._eof_token is not None:
            return self._eof_token

        while True:
            # 1. Skip whitespace and comments
            err = skip_whitespace_and_comments(self.cursor)
            if err is not None:
                self.errors.append(err)
                if self.on_error:
                    self.on_error(err)

            # Check for end of input
            if self.cursor.isAtEnd():
                self._eof_token = Token(
                    TokenType.EOF,
                    "",
                    self.cursor.getLine(),
                    self.cursor.getColumn(),
                )
                self.tokens.append(self._eof_token)
                if self.on_token:
                    self.on_token(self._eof_token)
                return self._eof_token

            # 2. Dispatch based on current character
            c = self.cursor.peek()
            if c.isalpha() or c == '_':
                result = scan_word(self.cursor)
            elif c.isdigit():
                result = scan_number_or_invalid_id(self.cursor)
            elif c in ('"', "'"):
                result = scan_string(self.cursor)
            else:
                result = scan_operator_or_delimiter(self.cursor)

            # 3. Handle result (Token | LexicalError)
            if isinstance(result, LexicalError):
                self.errors.append(result)
                if self.on_error:
                    self.on_error(result)
                # Panic-mode recovery: the sub-scanner already advanced past
                # the bad input, so we continue the loop for the next token.
                continue

            if result.type is TokenType.IDENTIFIER:
                self.symbol_table.insert(result)

            self.tokens.append(result)
            if self.on_token:
                self.on_token(result)
            return result

    # snake_case alias for Python convention
    get_next_token = getNextToken

    def tokenize(self) -> tuple[list[Token], list[LexicalError], SymbolTable]:
        """Consumes the entire source until EOF and returns (tokens, errors, symbol_table)."""
        while True:
            token = self.getNextToken()
            if token.type is TokenType.EOF:
                break
        return self.tokens, self.errors, self.symbol_table

    def __iter__(self) -> Iterator[Token]:
        while True:
            token = self.getNextToken()
            yield token
            if token.type is TokenType.EOF:
                break


def tokenize(source: str | SourceCursor) -> tuple[list[Token], list[LexicalError], SymbolTable]:
    """Helper function to tokenize source string or cursor into (tokens, errors, symbol_table)."""
    lexer = Lexer(source)
    return lexer.tokenize()
