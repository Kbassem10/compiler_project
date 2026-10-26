import sys
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cursor import FileCursor
from src.errors import LexicalError
from src.lexer import Lexer, tokenize
from src.token import Token
from src.token_type import TokenType


def test_get_next_token_sequence():
    source = "int count = 42;"
    lexer = Lexer(source)

    t1 = lexer.getNextToken()
    assert t1 == Token(TokenType.INT, "int", 1, 1)

    t2 = lexer.getNextToken()
    assert t2 == Token(TokenType.IDENTIFIER, "count", 1, 5)

    t3 = lexer.getNextToken()
    assert t3 == Token(TokenType.ASSIGN, "=", 1, 11)

    t4 = lexer.getNextToken()
    assert t4 == Token(TokenType.NUMBER, "42", 1, 13)

    t5 = lexer.getNextToken()
    assert t5 == Token(TokenType.SEMICOLON, ";", 1, 15)

    t6 = lexer.getNextToken()
    assert t6 == Token(TokenType.EOF, "", 1, 16)

    # Calling getNextToken() after EOF returns the same EOF token and doesn't duplicate
    t7 = lexer.getNextToken()
    assert t7 == t6
    assert len(lexer.tokens) == 6


def test_comments_and_whitespace_skipped():
    source = """
    // Single line comment
    /* Multi line
       comment */
    int x;
    """
    lexer = Lexer(source)
    tok1 = lexer.getNextToken()
    assert tok1 == Token(TokenType.INT, "int", 5, 5)
    tok2 = lexer.getNextToken()
    assert tok2 == Token(TokenType.IDENTIFIER, "x", 5, 9)
    tok3 = lexer.getNextToken()
    assert tok3 == Token(TokenType.SEMICOLON, ";", 5, 10)
    tok4 = lexer.getNextToken()
    assert tok4.type is TokenType.EOF
    assert len(lexer.errors) == 0


def test_panic_mode_illegal_character():
    # '@' should be skipped, recording an error, and lexer continues to 'x'
    source = "int @ x = 5;"
    lexer = Lexer(source)

    assert lexer.getNextToken().type is TokenType.INT
    # '@' causes an error, but getNextToken() skips it and returns 'x'
    tok = lexer.getNextToken()
    assert tok == Token(TokenType.IDENTIFIER, "x", 1, 7)
    assert len(lexer.errors) == 1
    assert "invalid character '@'" in lexer.errors[0].message
    assert lexer.errors[0].line == 1 and lexer.errors[0].column == 5


def test_panic_mode_invalid_identifier():
    # '1name' is an invalid identifier error; lexer recovers and reads ';'
    source = "int 1name;"
    lexer = Lexer(source)

    assert lexer.getNextToken().type is TokenType.INT
    tok = lexer.getNextToken()
    assert tok == Token(TokenType.SEMICOLON, ";", 1, 10)
    assert len(lexer.errors) == 1
    assert "invalid identifier '1name'" in lexer.errors[0].message


def test_panic_mode_unclosed_string():
    # unclosed string on line 1, continues to line 2
    source = 'String s = "hello\nint y = 10;'
    lexer = Lexer(source)

    assert lexer.getNextToken().type is TokenType.STRING_TYPE
    assert lexer.getNextToken().type is TokenType.IDENTIFIER
    assert lexer.getNextToken().type is TokenType.ASSIGN

    # string literal is unclosed, so next token read is 'int' on line 2
    tok = lexer.getNextToken()
    assert tok == Token(TokenType.INT, "int", 2, 1)
    assert len(lexer.errors) == 1
    assert "unclosed string literal" in lexer.errors[0].message


def test_panic_mode_unclosed_comment():
    # unclosed comment at EOF
    source = "int z; /* unclosed comment"
    lexer = Lexer(source)

    assert lexer.getNextToken().type is TokenType.INT
    assert lexer.getNextToken().type is TokenType.IDENTIFIER
    assert lexer.getNextToken().type is TokenType.SEMICOLON

    eof = lexer.getNextToken()
    assert eof.type is TokenType.EOF
    assert len(lexer.errors) == 1
    assert "unclosed comment" in lexer.errors[0].message


def test_symbol_table_population():
    source = "class Main { int count; count = count + 1; }"
    tokens, errors, table = tokenize(source)

    assert len(errors) == 0
    # Keywords (class, int) must not be in symbol table.
    assert table.lookup("class") is None
    assert table.lookup("int") is None

    # Identifiers: Main and count
    assert len(table) == 2
    main_entry = table.lookup("Main")
    assert main_entry is not None
    assert main_entry.occurrences == [(1, 7)]

    count_entry = table.lookup("count")
    assert count_entry is not None
    assert len(count_entry.occurrences) == 3


def test_callbacks_streaming():
    source = "int @ y;"
    seen_tokens = []
    seen_errors = []

    lexer = Lexer(
        source,
        on_token=lambda t: seen_tokens.append(t),
        on_error=lambda e: seen_errors.append(e),
    )
    tokens, errors, _ = lexer.tokenize()

    assert seen_tokens == tokens
    assert seen_errors == errors
    assert len(seen_errors) == 1
    assert len(seen_tokens) == 4  # int, y, ;, EOF


def test_iteration_protocol():
    source = "a + b"
    lexer = Lexer(source)
    tokens = list(lexer)
    types = [t.type for t in tokens]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.MATHOP,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]


def test_file_cursor_input():
    cursor = FileCursor("boolean flag = true;")
    tokens, errors, table = tokenize(cursor)
    assert len(errors) == 0
    assert tokens[0].type is TokenType.BOOLEAN
    assert tokens[1].type is TokenType.IDENTIFIER
    assert tokens[1].lexeme == "flag"


if __name__ == "__main__":
    test_get_next_token_sequence()
    print("✅ PASS: test_get_next_token_sequence")
    test_comments_and_whitespace_skipped()
    print("✅ PASS: test_comments_and_whitespace_skipped")
    test_panic_mode_illegal_character()
    print("✅ PASS: test_panic_mode_illegal_character")
    test_panic_mode_invalid_identifier()
    print("✅ PASS: test_panic_mode_invalid_identifier")
    test_panic_mode_unclosed_string()
    print("✅ PASS: test_panic_mode_unclosed_string")
    test_panic_mode_unclosed_comment()
    print("✅ PASS: test_panic_mode_unclosed_comment")
    test_symbol_table_population()
    print("✅ PASS: test_symbol_table_population")
    test_callbacks_streaming()
    print("✅ PASS: test_callbacks_streaming")
    test_iteration_protocol()
    print("✅ PASS: test_iteration_protocol")
    test_file_cursor_input()
    print("✅ PASS: test_file_cursor_input")
    print("\nAll Task 7 tests passed successfully!")
