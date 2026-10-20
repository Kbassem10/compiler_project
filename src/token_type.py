"""TokenType definition for Mini Java Compiler.

FROZEN CONTRACT: Exactly 31 members across 7 groups.
Do not modify without team-wide review and consensus.
"""

from enum import Enum, unique


@unique
class TokenType(Enum):
    """Enumeration of lexical token types.
    
    Contains exactly 31 members partitioned across 7 grammatical categories:
      1. Class-structure keywords (5)
      2. Type keywords (5)
      3. Control keywords (5)
      4. Literals and names (3)
      5. Operators (3)
      6. Delimiters (9)
      7. Control (1)
    """

    # 1. Class-structure keywords
    CLASS = "CLASS"
    PUBLIC = "PUBLIC"
    STATIC = "STATIC"
    VOID = "VOID"
    MAIN = "MAIN"

    # 2. Type keywords
    INT = "INT"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    STRING_TYPE = "STRING_TYPE"

    # 3. Control keywords
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"

    # 4. Literals and names
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # 5. Operators
    ASSIGN = "ASSIGN"
    MATHOP = "MATHOP"
    LOGOP = "LOGOP"

    # 6. Delimiters
    LPAR = "LPAR"
    RPAR = "RPAR"
    LCUR = "LCUR"
    RCUR = "RCUR"
    LSQU = "LSQU"
    RSQU = "RSQU"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"

    # 7. Control
    EOF = "EOF"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
