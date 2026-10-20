from enum import Enum


class TokenType(Enum):
    # Class-structure keywords
    CLASS = "CLASS"
    PUBLIC = "PUBLIC"
    STATIC = "STATIC"
    VOID = "VOID"
    MAIN = "MAIN"

    # Type keywords
    INT = "INT"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    STRING_TYPE = "STRING_TYPE"

    # Control keywords
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"

    # Literals and names
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    ASSIGN = "ASSIGN"
    MATHOP = "MATHOP"
    LOGOP = "LOGOP"

    # Delimiters
    LPAR = "LPAR"
    RPAR = "RPAR"
    LCUR = "LCUR"
    RCUR = "RCUR"
    LSQU = "LSQU"
    RSQU = "RSQU"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"

    # Control
    EOF = "EOF"
