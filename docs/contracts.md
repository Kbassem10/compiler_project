# Mini Java Compiler — Core Data Contracts (Frozen)

This document formalizes the immutable specifications established in **Task 1**. These contracts are **FROZEN**. No modification may be introduced without team-wide communication and an approved pull request.

---

## 1. TokenType Enum (Exactly 31 Members)

The enumeration consists of exactly 31 members categorized into 7 grammatical groups:

| Group | Members | Purpose |
| :--- | :--- | :--- |
| **Class-structure keywords** | `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `MAIN` | Top-level class, method declaration and program entrypoint |
| **Type keywords** | `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE` | Primitive & string data types (`String` → `STRING_TYPE`) |
| **Control keywords** | `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN` | Flow control and function return constructs |
| **Literals and names** | `IDENTIFIER`, `NUMBER`, `STRING` | Variable/method identifiers, numeric literals, and double-quoted string literals |
| **Operators** | `ASSIGN`, `MATHOP`, `LOGOP` | Assignment (`=`), Arithmetic (`+`, `-`, `*`, `/`), Relational & Logical (`==`, `!=`, `<`, `>`, `<=`, `>=`) |
| **Delimiters** | `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT` | `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`, `.` |
| **Control** | `EOF` | End-Of-File sentinel token |

---

## 2. Token Contract

```python
@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
```

- **Immutability:** Attributes cannot be modified after instantiation (`FrozenInstanceError`).
- **Positions:** `line` and `column` are **1-indexed** and point to the **first character** of the token's lexeme.
- **Lexeme:** Contains the exact raw slice of source text. String literals preserve enclosing quotation marks (`"hello"`).
- **String Representation:** Formats as `Token(<TYPE>, "<lexeme>", line=<line>, column=<column>)`.
- **Value Equality:** Two tokens with matching fields evaluate as equal (`t1 == t2`).

---

## 3. LexicalError Contract

```python
@dataclass(frozen=True)
class LexicalError:
    message: str
    line: int
    column: int
```

- **Immutability:** Attributes cannot be modified after instantiation (`FrozenInstanceError`).
- **Positions:** `line` and `column` are **1-indexed** and point to the start of the offending construct.
- **Message:** Standard formatted string, e.g.:
  `"Error: invalid character '@' at line 2, column 4."`
- **Error vs Token:** Lexical scanning produces a `LexicalError` and **no token**; scanner recovers and continues.

---

## 4. SourceCursor (Abstract Interface)

```python
class SourceCursor(ABC):
    @abstractmethod
    def peek(self) -> str:
        """Returns the current character without consuming. Returns '\0' at EOF."""
        ...

    @abstractmethod
    def peekNext(self) -> str:
        """Returns the character after current without consuming. Returns '\0' at EOF."""
        ...

    @abstractmethod
    def advance(self) -> str:
        """Consumes and returns current character, updating line/column tracking."""
        ...

    @abstractmethod
    def isAtEnd(self) -> bool:
        """Returns True if the cursor is at or past EOF."""
        ...

    @abstractmethod
    def getLine(self) -> int:
        """Returns 1-indexed line number of the NEXT character to be read."""
        ...

    @abstractmethod
    def getColumn(self) -> int:
        """Returns 1-indexed column number of the NEXT character to be read."""
        ...
```

- Pure interface with no implementation logic. Concrete implementation provided by Task 2.
- `peek()` and `peekNext()` return sentinel `'\0'` when out of bounds and never throw exceptions.

---

## 5. Shared Conventions

1. **Keywords:** `class public static void main int float boolean char String if else while for return` (case-sensitive).
2. **Operators:**
   - `=` → `ASSIGN`
   - `==`, `!=`, `<`, `>`, `<=`, `>=` → `LOGOP`
   - `+`, `-`, `*`, `/` → `MATHOP`
3. **Delimiters:**
   - `(` → `LPAR`, `)` → `RPAR`
   - `{` → `LCUR`, `}` → `RCUR`
   - `[` → `LSQU`, `]` → `RSQU`
   - `;` → `SEMICOLON`, `,` → `COMMA`, `.` → `DOT`
4. **EOF Token:** Emitted once, positioned immediately following the last character of source code.
