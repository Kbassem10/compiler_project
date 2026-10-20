"""Shared conventions and lookup mappings for Mini Java Compiler.

FROZEN CONTRACT: Predefined keywords, operators, delimiters, and sentinel constants.
Do not modify without team-wide review and consensus.
"""

from types import MappingProxyType
from typing import Mapping
from .token_type import TokenType

# 1. Keywords mapping (case-sensitive)
# Notice: 'String' maps to TokenType.STRING_TYPE
_KEYWORDS: dict[str, TokenType] = {
    # Class-structure keywords
    "class": TokenType.CLASS,
    "public": TokenType.PUBLIC,
    "static": TokenType.STATIC,
    "void": TokenType.VOID,
    "main": TokenType.MAIN,
    # Type keywords
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "boolean": TokenType.BOOLEAN,
    "char": TokenType.CHAR,
    "String": TokenType.STRING_TYPE,
    # Control keywords
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
}
KEYWORDS: Mapping[str, TokenType] = MappingProxyType(_KEYWORDS)

# 2. Operators mapping
# '=' -> ASSIGN; '==', '!=', '<', '>', '<=', '>=' -> LOGOP; '+', '-', '*', '/' -> MATHOP
_OPERATORS: dict[str, TokenType] = {
    # Assignment
    "=": TokenType.ASSIGN,
    # Logical / Relational operators (LOGOP)
    "==": TokenType.LOGOP,
    "!=": TokenType.LOGOP,
    "<": TokenType.LOGOP,
    ">": TokenType.LOGOP,
    "<=": TokenType.LOGOP,
    ">=": TokenType.LOGOP,
    # Mathematical operators (MATHOP)
    "+": TokenType.MATHOP,
    "-": TokenType.MATHOP,
    "*": TokenType.MATHOP,
    "/": TokenType.MATHOP,
}
OPERATORS: Mapping[str, TokenType] = MappingProxyType(_OPERATORS)

# 3. Delimiters mapping
_DELIMITERS: dict[str, TokenType] = {
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
DELIMITERS: Mapping[str, TokenType] = MappingProxyType(_DELIMITERS)

# Sentinel for EOF character reading
EOF_CHAR: str = "\0"
