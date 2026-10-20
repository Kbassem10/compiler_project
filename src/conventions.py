from .token_type import TokenType

# Keywords map (case-sensitive)
KEYWORDS = {
    "class": TokenType.CLASS,
    "public": TokenType.PUBLIC,
    "static": TokenType.STATIC,
    "void": TokenType.VOID,
    "main": TokenType.MAIN,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "boolean": TokenType.BOOLEAN,
    "char": TokenType.CHAR,
    "String": TokenType.STRING_TYPE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
}

# Operators map
OPERATORS = {
    "=": TokenType.ASSIGN,
    "==": TokenType.LOGOP,
    "!=": TokenType.LOGOP,
    "<": TokenType.LOGOP,
    ">": TokenType.LOGOP,
    "<=": TokenType.LOGOP,
    ">=": TokenType.LOGOP,
    "+": TokenType.MATHOP,
    "-": TokenType.MATHOP,
    "*": TokenType.MATHOP,
    "/": TokenType.MATHOP,
}

# Delimiters map
DELIMITERS = {
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
