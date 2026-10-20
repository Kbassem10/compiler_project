"""Comprehensive test suite verifying Task 1 core contracts.

Tests cover:
  1. TokenType enum completeness (exactly 31 members).
  2. Exact character-for-character member name matches.
  3. Immutability of Token and LexicalError (dataclass FrozenInstanceError).
  4. Value equality and hashing for Token and LexicalError.
  5. SourceCursor interface purity (cannot instantiate, pure abstract methods).
  6. Defensive validation on negative/zero lines and columns.
  7. Empty project clean build/execution (prints nothing, exits 0).
  8. Shared conventions mappings (KEYWORDS, OPERATORS, DELIMITERS, EOF_CHAR).
"""

import io
import unittest
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import FrozenInstanceError

from src.token_type import TokenType
from src.token import Token
from src.errors import LexicalError
from src.cursor import SourceCursor
from src.conventions import KEYWORDS, OPERATORS, DELIMITERS, EOF_CHAR
from src.main import main


class TestTokenTypeContracts(unittest.TestCase):
    """Verifies TokenType enum contains exactly the 31 required members."""

    EXPECTED_MEMBERS = {
        # Class-structure keywords (5)
        "CLASS", "PUBLIC", "STATIC", "VOID", "MAIN",
        # Type keywords (5)
        "INT", "FLOAT", "BOOLEAN", "CHAR", "STRING_TYPE",
        # Control keywords (5)
        "IF", "ELSE", "WHILE", "FOR", "RETURN",
        # Literals and names (3)
        "IDENTIFIER", "NUMBER", "STRING",
        # Operators (3)
        "ASSIGN", "MATHOP", "LOGOP",
        # Delimiters (9)
        "LPAR", "RPAR", "LCUR", "RCUR", "LSQU", "RSQU", "SEMICOLON", "COMMA", "DOT",
        # Control (1)
        "EOF",
    }

    def test_member_count_is_exactly_31(self) -> None:
        self.assertEqual(
            len(TokenType),
            31,
            f"TokenType must have exactly 31 members, but found {len(TokenType)}.",
        )

    def test_all_expected_members_exist_verbatim(self) -> None:
        actual_members = {member.name for member in TokenType}
        self.assertEqual(
            actual_members,
            self.EXPECTED_MEMBERS,
            f"Mismatch in TokenType members: diff={actual_members ^ self.EXPECTED_MEMBERS}",
        )

    def test_string_representation(self) -> None:
        self.assertEqual(str(TokenType.CLASS), "CLASS")
        self.assertEqual(repr(TokenType.STRING_TYPE), "STRING_TYPE")


class TestTokenContracts(unittest.TestCase):
    """Verifies immutability, equality, representation, and edge cases of Token."""

    def test_token_creation_and_fields(self) -> None:
        t = Token(type=TokenType.CLASS, lexeme="class", line=1, column=1)
        self.assertEqual(t.type, TokenType.CLASS)
        self.assertEqual(t.lexeme, "class")
        self.assertEqual(t.line, 1)
        self.assertEqual(t.column, 1)

    def test_token_immutability(self) -> None:
        t = Token(type=TokenType.IDENTIFIER, lexeme="myVar", line=2, column=5)
        with self.assertRaises(FrozenInstanceError):
            t.lexeme = "otherVar"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            t.line = 3  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            t.column = 10  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            t.type = TokenType.STRING  # type: ignore[misc]

    def test_token_equality_and_hash(self) -> None:
        t1 = Token(TokenType.IDENTIFIER, "foo", line=4, column=10)
        t2 = Token(TokenType.IDENTIFIER, "foo", line=4, column=10)
        t3 = Token(TokenType.IDENTIFIER, "bar", line=4, column=10)

        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        self.assertEqual(hash(t1), hash(t2))
        self.assertNotEqual(t1, "not_a_token")

    def test_token_representation(self) -> None:
        t1 = Token(TokenType.CLASS, "class", line=1, column=1)
        self.assertEqual(repr(t1), 'Token(CLASS, "class", line=1, column=1)')

        t_eof = Token(TokenType.EOF, "", line=1, column=12)
        self.assertEqual(repr(t_eof), 'Token(EOF, "", line=1, column=12)')

    def test_defensive_checks_line_column(self) -> None:
        # Line must be >= 1
        with self.assertRaises(ValueError):
            Token(TokenType.INT, "int", line=0, column=1)
        with self.assertRaises(ValueError):
            Token(TokenType.INT, "int", line=-1, column=1)

        # Column must be >= 1
        with self.assertRaises(ValueError):
            Token(TokenType.INT, "int", line=1, column=0)
        with self.assertRaises(ValueError):
            Token(TokenType.INT, "int", line=1, column=-5)

        # Lexeme must be string
        with self.assertRaises(TypeError):
            Token(TokenType.INT, 123, line=1, column=1)  # type: ignore[arg-type]

        # Invalid token type
        with self.assertRaises(TypeError):
            Token("UNKNOWN_TYPE", "val", line=1, column=1)  # type: ignore[arg-type]


class TestLexicalErrorContracts(unittest.TestCase):
    """Verifies immutability, representation, and edge cases of LexicalError."""

    def test_error_creation_and_fields(self) -> None:
        err = LexicalError(
            message="Error: invalid character '@' at line 2, column 4.",
            line=2,
            column=4,
        )
        self.assertEqual(err.message, "Error: invalid character '@' at line 2, column 4.")
        self.assertEqual(err.line, 2)
        self.assertEqual(err.column, 4)

    def test_error_immutability(self) -> None:
        err = LexicalError("msg", line=1, column=1)
        with self.assertRaises(FrozenInstanceError):
            err.message = "new msg"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            err.line = 2  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            err.column = 5  # type: ignore[misc]

    def test_error_equality_and_hash(self) -> None:
        err1 = LexicalError("Error: '@'", line=1, column=5)
        err2 = LexicalError("Error: '@'", line=1, column=5)
        err3 = LexicalError("Error: '#'", line=1, column=5)

        self.assertEqual(err1, err2)
        self.assertNotEqual(err1, err3)
        self.assertEqual(hash(err1), hash(err2))
        self.assertNotEqual(err1, "not_an_error")

    def test_error_representation(self) -> None:
        err = LexicalError("Error: invalid character '@' at line 2, column 4.", line=2, column=4)
        self.assertEqual(
            repr(err),
            'LexicalError("Error: invalid character \'@\' at line 2, column 4.", line=2, column=4)',
        )

    def test_defensive_checks_error(self) -> None:
        with self.assertRaises(ValueError):
            LexicalError("msg", line=0, column=1)
        with self.assertRaises(ValueError):
            LexicalError("msg", line=1, column=0)
        with self.assertRaises(TypeError):
            LexicalError(12345, line=1, column=1)  # type: ignore[arg-type]


class TestSourceCursorInterface(unittest.TestCase):
    """Verifies SourceCursor is a pure abstract interface that cannot be directly instantiated."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        with self.assertRaises(TypeError):
            SourceCursor()  # type: ignore[abstract]

    def test_abstract_methods_present(self) -> None:
        required_methods = {"peek", "peekNext", "advance", "isAtEnd", "getLine", "getColumn"}
        self.assertTrue(required_methods.issubset(SourceCursor.__abstractmethods__))

    def test_concrete_subclass_must_implement_all_abstract_methods(self) -> None:
        class IncompleteCursor(SourceCursor):
            def peek(self) -> str:
                return "\0"

        with self.assertRaises(TypeError):
            IncompleteCursor()  # type: ignore[abstract]

        class CompleteCursor(SourceCursor):
            def peek(self) -> str:
                return "\0"
            def peekNext(self) -> str:
                return "\0"
            def advance(self) -> str:
                return "\0"
            def isAtEnd(self) -> bool:
                return True
            def getLine(self) -> int:
                return 1
            def getColumn(self) -> int:
                return 1

        cursor = CompleteCursor()
        self.assertEqual(cursor.peek(), "\0")
        self.assertEqual(cursor.peekNext(), "\0")
        self.assertEqual(cursor.advance(), "\0")
        self.assertTrue(cursor.isAtEnd())
        self.assertEqual(cursor.getLine(), 1)
        self.assertEqual(cursor.getColumn(), 1)


class TestConventions(unittest.TestCase):
    """Verifies shared conventions and lookup tables."""

    def test_keywords_table(self) -> None:
        # Exactly 15 keywords
        self.assertEqual(len(KEYWORDS), 15)
        # Verify specific case-sensitivity & types
        self.assertEqual(KEYWORDS["class"], TokenType.CLASS)
        self.assertEqual(KEYWORDS["public"], TokenType.PUBLIC)
        self.assertEqual(KEYWORDS["static"], TokenType.STATIC)
        self.assertEqual(KEYWORDS["void"], TokenType.VOID)
        self.assertEqual(KEYWORDS["main"], TokenType.MAIN)
        self.assertEqual(KEYWORDS["int"], TokenType.INT)
        self.assertEqual(KEYWORDS["float"], TokenType.FLOAT)
        self.assertEqual(KEYWORDS["boolean"], TokenType.BOOLEAN)
        self.assertEqual(KEYWORDS["char"], TokenType.CHAR)
        self.assertEqual(KEYWORDS["String"], TokenType.STRING_TYPE)
        self.assertEqual(KEYWORDS["if"], TokenType.IF)
        self.assertEqual(KEYWORDS["else"], TokenType.ELSE)
        self.assertEqual(KEYWORDS["while"], TokenType.WHILE)
        self.assertEqual(KEYWORDS["for"], TokenType.FOR)
        self.assertEqual(KEYWORDS["return"], TokenType.RETURN)

    def test_operators_table(self) -> None:
        self.assertEqual(OPERATORS["="], TokenType.ASSIGN)
        # LOGOP: ==, !=, <, >, <=, >=
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            self.assertEqual(OPERATORS[op], TokenType.LOGOP, f"{op} should map to LOGOP")
        # MATHOP: +, -, *, /
        for op in ["+", "-", "*", "/"]:
            self.assertEqual(OPERATORS[op], TokenType.MATHOP, f"{op} should map to MATHOP")

    def test_delimiters_table(self) -> None:
        delims = {
            "(": TokenType.LPAR,
            ")": TokenType.RPAR,
            "{": TokenType.LCUR,
            "}": TokenType.RCUR,
            "[": TokenType.LSQU,
            "]": TokenType.RSQU,
            ";": TokenType.SEMICOLON,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
        }
        for char, token_type in delims.items():
            self.assertEqual(DELIMITERS[char], token_type)

    def test_eof_sentinel(self) -> None:
        self.assertEqual(EOF_CHAR, "\0")
        self.assertEqual(SourceCursor.SENTINEL, "\0")


class TestProjectExecution(unittest.TestCase):
    """Verifies the empty project builds and runs with zero output and code 0."""

    def test_main_exits_zero_and_prints_nothing(self) -> None:
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            exit_code = main([])
        self.assertEqual(exit_code, 0)
        self.assertEqual(out_buf.getvalue(), "")
        self.assertEqual(err_buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
