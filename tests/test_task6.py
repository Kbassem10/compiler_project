import io
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.errors import LexicalError
from src.formatter import format_output, format_token
from src.lexer import tokenize
from src.main import main
from src.symbol_table import SymbolTable
from src.token import Token
from src.token_type import TokenType
from tests.verify import split_cases


def run_cli(*args):
    """Run the CLI and return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            code = main(list(args))
        except SystemExit as e:  # argparse exits on bad arguments
            code = e.code
    return code, out.getvalue(), err.getvalue()


def test_format_token():
    assert format_token(Token(TokenType.CLASS, "class", 1, 1)) == "Lexeme: class, Token: CLASS"
    assert format_token(Token(TokenType.EOF, "", 3, 1)) == "Lexeme: EOF, Token: EOF"


def test_lexeme_with_comma_and_colon():
    token = Token(TokenType.STRING, '"a, b: c"', 1, 1)
    assert format_token(token) == 'Lexeme: "a, b: c", Token: STRING'


def test_errors_printed_inline():
    tokens = [
        Token(TokenType.INT, "int", 1, 1),
        Token(TokenType.NUMBER, "5", 1, 7),
        Token(TokenType.EOF, "", 1, 8),
    ]
    errors = [LexicalError("Error: invalid character '@' at line 1, column 5.", 1, 5)]
    lines = format_output(tokens, errors, SymbolTable()).splitlines()
    assert lines[:4] == [
        "Lexeme: int, Token: INT",
        "Error: invalid character '@' at line 1, column 5.",
        "Lexeme: 5, Token: NUMBER",
        "Lexeme: EOF, Token: EOF",
    ]


def test_symbol_table_section():
    output = format_output(*tokenize("x = y + x;"))
    assert output.endswith(
        "Lexeme: EOF, Token: EOF\n"
        "\n"
        "Symbol Table\n"
        "Index: 0, Name: x, Occurrences: 1:1, 1:9\n"
        "Index: 1, Name: y, Occurrences: 1:5\n"
    )


def test_split_cases_crlf_and_empty_body():
    text = "header\r\n### TEST 01: first\r\nint a;\r\n### TEST 02: empty\r\n"
    assert split_cases(text) == [("01", "first", "int a;"), ("02", "empty", "")]


def test_cli_prints_tokens():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "prog.java"
        path.write_text("class A { }", encoding="utf-8")
        code, out, err = run_cli(str(path))
    assert code == 0 and err == ""
    assert out.startswith("Lexeme: class, Token: CLASS\nLexeme: A, Token: IDENTIFIER\n")


def test_cli_empty_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "empty.java"
        path.write_text("", encoding="utf-8")
        code, out, _ = run_cli(str(path))
    assert code == 0
    assert out == "Lexeme: EOF, Token: EOF\n\nSymbol Table\n(empty)\n"


def test_cli_missing_argument():
    code, out, err = run_cli()
    assert code != 0 and out == ""
    assert "usage:" in err and "Traceback" not in err


def test_cli_missing_file_and_directory():
    with tempfile.TemporaryDirectory() as tmp:
        for path in (str(Path(tmp) / "nope.java"), tmp):
            code, out, err = run_cli(path)
            assert code == 1 and out == ""
            assert err.startswith("Error: cannot read") and "Traceback" not in err


def test_cli_strict_and_output_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bad.java"
        path.write_text("int x = 10 @ 5;", encoding="utf-8")
        out_path = Path(tmp) / "result.txt"

        # Lexical errors are normal output: exit 0 by default, 1 with --strict
        assert run_cli(str(path))[0] == 0
        code, out, _ = run_cli(str(path), "--strict", "-o", str(out_path))
        assert code == 1 and out == ""
        assert "Error: invalid character '@' at line 1, column 12." in out_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    tests = [
        test_format_token,
        test_lexeme_with_comma_and_colon,
        test_errors_printed_inline,
        test_symbol_table_section,
        test_split_cases_crlf_and_empty_body,
        test_cli_prints_tokens,
        test_cli_empty_file,
        test_cli_missing_argument,
        test_cli_missing_file_and_directory,
        test_cli_strict_and_output_file,
    ]
    for test in tests:
        test()
        print(f"✅ PASS: {test.__name__}")
    print("\nAll Task 6 tests passed.")
