import sys
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cursor import SourceCursor
from src.scanners import scan_word_or_number_or_string
from src.token_type import TokenType
from src.errors import LexicalError

# 1. Mock Cursor بسيط عشان نختبر بيه الدوال
class StringCursor(SourceCursor):
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def peek(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else '\0'

    def peekNext(self) -> str:
        return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else '\0'

    def advance(self) -> str:
        ch = self.peek()
        if ch != '\0':
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        return ch

    def isAtEnd(self) -> bool:
        return self.pos >= len(self.source)

    def getLine(self) -> int:
        return self.line

    def getColumn(self) -> int:
        return self.col


# 2. حالات الاختبار لـ Task 3
def run_tests():
    test_cases = [
        # (Input Text, Expected Type/Class, Expected Lexeme/Error Keyword)
        ("class", TokenType.CLASS, "class"),
        ("String", TokenType.STRING_TYPE, "String"),
        ("myVar", TokenType.IDENTIFIER, "myVar"),
        ("123", TokenType.NUMBER, "123"),
        ("45.67", TokenType.NUMBER, "45.67"),
        ('"Hello World"', TokenType.STRING, '"Hello World"'),
        ("boolean", TokenType.BOOLEAN, "boolean"),
        ("true", TokenType.BOOLEAN, "true"),
        ("false", TokenType.BOOLEAN, "false"),
        ("1invalidId", LexicalError, "invalid identifier"),
        ('"Unclosed String', LexicalError, "unclosed string"),
    ]

    print("--- Running Task 3 Tests ---")
    for src, expected_type, expected_val in test_cases:
        cursor = StringCursor(src)
        result = scan_word_or_number_or_string(cursor)

        if isinstance(result, LexicalError):
            assert expected_type == LexicalError, f"Failed for {src}"
            assert expected_val in result.message, f"Failed message for {src}"
            print(f"✅ PASS [Error Case]: '{src}' -> {result.message}")
        elif result is not None:
            assert result.type == expected_type, f"Failed type for {src}"
            assert result.lexeme == expected_val, f"Failed lexeme for {src}"
            print(f"✅ PASS [Token Case]: '{src}' -> Token({result.type.name}, '{result.lexeme}')")
        else:
            print(f"❌ FAIL: Returned None for '{src}'")

if __name__ == "__main__":
    run_tests()