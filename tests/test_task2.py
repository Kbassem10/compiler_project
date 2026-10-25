import os
import sys
import tempfile
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cursor import FileCursor, StringCursor, skip_whitespace_and_comments
from src.errors import LexicalError


def test_cursor_empty():
    cursor = FileCursor("")
    assert cursor.isAtEnd()
    assert cursor.peek() == '\0'
    assert cursor.peekNext() == '\0'
    assert cursor.advance() == '\0'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 1


def test_cursor_advance_and_lookahead():
    cursor = FileCursor("abc")
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 1
    assert cursor.peek() == 'a'
    assert cursor.peekNext() == 'b'

    assert cursor.advance() == 'a'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 2
    assert cursor.peek() == 'b'
    assert cursor.peekNext() == 'c'

    assert cursor.advance() == 'b'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 3
    assert cursor.peek() == 'c'
    assert cursor.peekNext() == '\0'

    assert cursor.advance() == 'c'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 4
    assert cursor.isAtEnd()
    assert cursor.peek() == '\0'
    assert cursor.peekNext() == '\0'


def test_newlines_lf():
    cursor = FileCursor("a\nb")
    assert cursor.advance() == 'a'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 2

    assert cursor.advance() == '\n'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 1

    assert cursor.advance() == 'b'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 2


def test_newlines_crlf():
    cursor = FileCursor("a\r\nb")
    assert cursor.advance() == 'a'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 2

    assert cursor.advance() == '\r\n'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 1

    assert cursor.advance() == 'b'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 2


def test_lone_cr_and_tab():
    cursor = FileCursor("a\rb\tc")
    assert cursor.advance() == 'a'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 2

    # Lone \r counts as normal whitespace, line not incremented
    assert cursor.advance() == '\r'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 3

    assert cursor.advance() == 'b'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 4

    # Tab counts as one column
    assert cursor.advance() == '\t'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 5

    assert cursor.advance() == 'c'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 6


def test_skip_whitespace():
    cursor = FileCursor("   \t\r \n  x")
    err = cursor.skip_whitespace_and_comments()
    assert err is None
    assert cursor.peek() == 'x'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 3


def test_single_line_comments():
    cursor = FileCursor("// first line comment\nx")
    err = cursor.skip_whitespace_and_comments()
    assert err is None
    assert cursor.peek() == 'x'
    assert cursor.getLine() == 2
    assert cursor.getColumn() == 1

    # Single-line comment with CRLF
    cursor_crlf = FileCursor("// crlf comment\r\ny")
    err = cursor_crlf.skip_whitespace_and_comments()
    assert err is None
    assert cursor_crlf.peek() == 'y'
    assert cursor_crlf.getLine() == 2
    assert cursor_crlf.getColumn() == 1

    # Single-line comment ending at EOF without trailing newline
    cursor_eof = FileCursor("// comment at eof")
    err = cursor_eof.skip_whitespace_and_comments()
    assert err is None
    assert cursor_eof.isAtEnd()


def test_multi_line_comments():
    cursor = FileCursor("/* simple comment */x")
    err = cursor.skip_whitespace_and_comments()
    assert err is None
    assert cursor.peek() == 'x'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 21

    # Multi-line comment across lines
    cursor_multiline = FileCursor("/* line 1\nline 2 */y")
    err = cursor_multiline.skip_whitespace_and_comments()
    assert err is None
    assert cursor_multiline.peek() == 'y'
    assert cursor_multiline.getLine() == 2
    assert cursor_multiline.getColumn() == 10

    # Multi-line comment with embedded single-line comment markers
    cursor_embedded = FileCursor("/* // inside block */z")
    err = cursor_embedded.skip_whitespace_and_comments()
    assert err is None
    assert cursor_embedded.peek() == 'z'


def test_unclosed_block_comment():
    cursor = FileCursor("/* unclosed comment")
    err = cursor.skip_whitespace_and_comments()
    assert isinstance(err, LexicalError)
    assert err.line == 1
    assert err.column == 1
    assert "unclosed comment" in err.message
    assert cursor.isAtEnd()

    # Unclosed comment starting on line 3
    cursor_line3 = FileCursor("\n\n  /* unclosed block")
    err2 = cursor_line3.skip_whitespace_and_comments()
    assert isinstance(err2, LexicalError)
    assert err2.line == 3
    assert err2.column == 3


def test_slash_operator_not_consumed():
    cursor = FileCursor(" / 10")
    err = cursor.skip_whitespace_and_comments()
    assert err is None
    assert cursor.peek() == '/'
    assert cursor.getLine() == 1
    assert cursor.getColumn() == 2


def test_from_file(tmp_path=None):
    # Own temp file, so this test does not depend on the test corpus layout
    with tempfile.TemporaryDirectory() as tmp:
        filepath = os.path.join(tmp, "prog.java")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("// header comment\n/* block */\nclass A { }")
        cursor = FileCursor.from_file(filepath)
    err = cursor.skip_whitespace_and_comments()
    assert err is None
    # First non-comment/whitespace code is 'class'
    assert cursor.peek() == 'c'


def run_all():
    print("--- Running Task 2 Tests ---")
    test_cursor_empty()
    print("✅ PASS: test_cursor_empty")
    test_cursor_advance_and_lookahead()
    print("✅ PASS: test_cursor_advance_and_lookahead")
    test_newlines_lf()
    print("✅ PASS: test_newlines_lf")
    test_newlines_crlf()
    print("✅ PASS: test_newlines_crlf")
    test_lone_cr_and_tab()
    print("✅ PASS: test_lone_cr_and_tab")
    test_skip_whitespace()
    print("✅ PASS: test_skip_whitespace")
    test_single_line_comments()
    print("✅ PASS: test_single_line_comments")
    test_multi_line_comments()
    print("✅ PASS: test_multi_line_comments")
    test_unclosed_block_comment()
    print("✅ PASS: test_unclosed_block_comment")
    test_slash_operator_not_consumed()
    print("✅ PASS: test_slash_operator_not_consumed")
    test_from_file()
    print("✅ PASS: test_from_file")
    print("All Task 2 tests passed successfully!")


if __name__ == "__main__":
    run_all()
