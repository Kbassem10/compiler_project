from abc import ABC, abstractmethod
from src.errors import LexicalError


class SourceCursor(ABC):
    @abstractmethod
    def peek(self) -> str:
        """Returns current char, or '\0' at end."""
        pass

    @abstractmethod
    def peekNext(self) -> str:
        """Returns char after current, or '\0' if none."""
        pass

    @abstractmethod
    def advance(self) -> str:
        """Consumes and returns current char, updating line/column."""
        pass

    @abstractmethod
    def isAtEnd(self) -> bool:
        pass

    @abstractmethod
    def getLine(self) -> int:
        """1-indexed line of NEXT char."""
        pass

    @abstractmethod
    def getColumn(self) -> int:
        """1-indexed column of NEXT char."""
        pass


class FileCursor(SourceCursor):
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    @classmethod
    def from_file(cls, filepath: str) -> "FileCursor":
        with open(filepath, "r", encoding="utf-8") as f:
            return cls(f.read())

    def peek(self) -> str:
        if self.pos >= len(self.source):
            return '\0'
        return self.source[self.pos]

    def peekNext(self) -> str:
        if self.pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.pos + 1]

    def advance(self) -> str:
        if self.isAtEnd():
            return '\0'

        ch = self.source[self.pos]

        # CRLF is treated as one line break
        if ch == '\r' and self.peekNext() == '\n':
            self.pos += 2
            self.line += 1
            self.column = 1
            return '\r\n'

        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return ch

    def isAtEnd(self) -> bool:
        return self.pos >= len(self.source)

    def getLine(self) -> int:
        return self.line

    def getColumn(self) -> int:
        return self.column

    def skip_whitespace_and_comments(self) -> LexicalError | None:
        while not self.isAtEnd():
            ch = self.peek()

            if ch in (' ', '\t', '\r', '\n'):
                self.advance()
            elif ch == '/' and self.peekNext() == '/':
                self.advance()
                self.advance()
                while not self.isAtEnd():
                    if self.peek() == '\n' or (self.peek() == '\r' and self.peekNext() == '\n'):
                        break
                    self.advance()
            elif ch == '/' and self.peekNext() == '*':
                start_line = self.getLine()
                start_col = self.getColumn()
                self.advance()
                self.advance()
                closed = False
                while not self.isAtEnd():
                    if self.peek() == '*' and self.peekNext() == '/':
                        self.advance()
                        self.advance()
                        closed = True
                        break
                    self.advance()
                if not closed:
                    return LexicalError(
                        f"Error: unclosed comment starting at line {start_line}, column {start_col}.",
                        line=start_line,
                        column=start_col,
                    )
            else:
                break

        return None


StringCursor = FileCursor


def skip_whitespace_and_comments(cursor: SourceCursor) -> LexicalError | None:
    if hasattr(cursor, "skip_whitespace_and_comments"):
        return cursor.skip_whitespace_and_comments()

    while not cursor.isAtEnd():
        ch = cursor.peek()
        if ch in (' ', '\t', '\r', '\n'):
            cursor.advance()
        elif ch == '/' and cursor.peekNext() == '/':
            cursor.advance()
            cursor.advance()
            while not cursor.isAtEnd():
                if cursor.peek() == '\n' or (cursor.peek() == '\r' and cursor.peekNext() == '\n'):
                    break
                cursor.advance()
        elif ch == '/' and cursor.peekNext() == '*':
            start_line = cursor.getLine()
            start_col = cursor.getColumn()
            cursor.advance()
            cursor.advance()
            closed = False
            while not cursor.isAtEnd():
                if cursor.peek() == '*' and cursor.peekNext() == '/':
                    cursor.advance()
                    cursor.advance()
                    closed = True
                    break
                cursor.advance()
            if not closed:
                return LexicalError(
                    f"Error: unclosed comment starting at line {start_line}, column {start_col}.",
                    line=start_line,
                    column=start_col,
                )
        else:
            break

    return None
