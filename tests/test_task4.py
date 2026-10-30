import sys
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cursor import FileCursor
from src.scanner_delimiters import scan_operator_or_delimiter
from src.token_type import TokenType
from src.errors import LexicalError


def test_two_char_operators():
    ops = [("==", TokenType.LOGOP), ("!=", TokenType.LOGOP), ("<=", TokenType.LOGOP), (">=", TokenType.LOGOP)]
    for op, expected_type in ops:
        cursor = FileCursor(op)
        token = scan_operator_or_delimiter(cursor)
        assert isinstance(token, type(scan_operator_or_delimiter(FileCursor("="))))
        assert token.type == expected_type
        assert token.lexeme == op
        assert cursor.isAtEnd()
    print("✅ PASS: test_two_char_operators")


def test_single_char_operators():
    ops = [
        ("=", TokenType.ASSIGN),
        ("+", TokenType.MATHOP),
        ("-", TokenType.MATHOP),
        ("*", TokenType.MATHOP),
        ("/", TokenType.MATHOP),
        ("<", TokenType.LOGOP),
        (">", TokenType.LOGOP),
    ]
    for op, expected_type in ops:
        cursor = FileCursor(op)
        token = scan_operator_or_delimiter(cursor)
        assert token.type == expected_type
        assert token.lexeme == op
        assert cursor.isAtEnd()
    print("✅ PASS: test_single_char_operators")


def test_delimiters():
    delims = [
        ("(", TokenType.LPAR),
        (")", TokenType.RPAR),
        ("{", TokenType.LCUR),
        ("}", TokenType.RCUR),
        ("[", TokenType.LSQU),
        ("]", TokenType.RSQU),
        (";", TokenType.SEMICOLON),
        (",", TokenType.COMMA),
        (".", TokenType.DOT),
    ]
    for ch, expected_type in delims:
        cursor = FileCursor(ch)
        token = scan_operator_or_delimiter(cursor)
        assert token.type == expected_type
        assert token.lexeme == ch
        assert cursor.isAtEnd()
    print("✅ PASS: test_delimiters")


def test_illegal_characters():
    for illegal in ["@", "$", "#", "`", "?", "~"]:
        cursor = FileCursor(illegal)
        err = scan_operator_or_delimiter(cursor)
        assert isinstance(err, LexicalError)
        assert err.line == 1
        assert err.column == 1
        assert f"Error: invalid character '{illegal}' at line 1, column 1." == err.message
        assert cursor.isAtEnd(), "Scanner should advance past illegal character"
    print("✅ PASS: test_illegal_characters")


def test_operator_lookahead_stream():
    # Verify that in '===' it scans '==' then leaves '=' for next
    cursor = FileCursor("===")
    t1 = scan_operator_or_delimiter(cursor)
    assert t1.type == TokenType.LOGOP and t1.lexeme == "=="
    t2 = scan_operator_or_delimiter(cursor)
    assert t2.type == TokenType.ASSIGN and t2.lexeme == "="
    assert cursor.isAtEnd()
    print("✅ PASS: test_operator_lookahead_stream")


if __name__ == "__main__":
    print("--- Running Task 4 Tests ---")
    test_two_char_operators()
    test_single_char_operators()
    test_delimiters()
    test_illegal_characters()
    test_operator_lookahead_stream()
    print("All Task 4 tests passed successfully!")
