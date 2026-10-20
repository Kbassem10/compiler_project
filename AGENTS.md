# AGENTS.md — System Architecture, Context & Compiler Implementation Guide

This document serves as the authoritative architectural blueprint and developer/agent reference for the **Mini Java Compiler** (`mini-java-compiler`). Any AI coding assistant or engineer working on this codebase MUST follow the specifications and constraints documented here.

---

## 1. System Overview & Core Philosophy

The **Mini Java Compiler** is an educational, clean compiler pipeline built from scratch without external lexical/parsing libraries (e.g., Lex, Yacc, ANTLR) for **CSCI415 - Compiler Design**.

Phase 01 implements **Lexical Analysis (Scanner)** with exact source coordinates (1-indexed line and column) and a custom symbol table.

```
┌─────────────────────────────────────────────────────────────┐
│                       Source Code                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   SourceCursor Interface                    │
│                                                             │
│  - Tracks 1-indexed (line, column) coordinate state         │
│  - Sentinel lookahead: peek(), peekNext() -> '\0'           │
│  - Skips whitespace & single-line / multi-line comments     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Sequential Lexer Pipeline                   │
│                                                             │
│  - WordScanner: Keywords vs IDENTIFIER                      │
│  - NumberScanner: Integer & Float literals                  │
│  - StringScanner: Double-quoted strings with escapes        │
│  - Delimiter & Operator Scanner: Math/Log/Assign symbols    │
│  - Illegal Character Scanner: Emits LexicalError diagnostic │
└──────────────────────────────┬──────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
┌───────────────────────────┐     ┌───────────────────────────┐
│       Token Stream        │     │       Symbol Table        │
│                           │     │                           │
│ - Immutable Token objects │     │ - User Identifiers        │
│ - Preserves exact lexeme  │     │ - Scope/Type attributes   │
│ - 1-indexed token start   │     │ - Collision resolution    │
└───────────────────────────┘     └───────────────────────────┘
```

---

## 2. Core Developer & Agent Directives

### 2.1 No Overengineering (Simplicity First)
- **Keep it Simple & Clean:** Write concise, readable, and idiomatic Python (3.10+). Avoid unnecessary boilerplate, excessive wrapper classes, custom metaclasses, or bloated defensive checks.
- **Easy to Explain:** The codebase is for an academic compiler course. Any student must be able to read, understand, and explain the code during an oral discussion or code review.
- **Minimal, Focused Comments:** Write brief, meaningful comments only where needed. Avoid cluttering code with obvious comments or long docstrings on every line.
- **Zero External Dependencies:** Use only the Python Standard Library. Do not introduce 3rd-party parsing, regex, or utility packages.

### 2.2 Self-Updating Documentation Mandate
Whenever any agent or developer completes or modifies a task:
1. **Update `AGENTS.md`:** Update the **Task Status Tracker** (Section 4) and document any new functions, classes, or conventions added.
2. **Update `README.md`:** Keep the run instructions and project tree aligned with the actual files in `src/`.
3. **Always Ready for Queries:** `AGENTS.md` must always reflect the current, exact state of the project so any agent can instantly answer questions about architecture, progress, and file roles without ambiguity.

---

## 3. Frozen Data Contracts Reference (Task 1)

These contracts are **FROZEN**. Modifying them requires team-wide communication and consensus.

### 3.1 `TokenType` (src/token_type.py — Exactly 31 Members)
- **Class keywords:** `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `MAIN`
- **Type keywords:** `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`
- **Control keywords:** `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`
- **Literals & names:** `IDENTIFIER`, `NUMBER`, `STRING`
- **Operators:** `ASSIGN` (`=`), `MATHOP` (`+`, `-`, `*`, `/`), `LOGOP` (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Delimiters:** `LPAR` (`(`), `RPAR` (`)`), `LCUR` (`{`), `RCUR` (`}`), `LSQU` (`[`), `RSQU` (`]`), `SEMICOLON` (`;`), `COMMA` (`,`), `DOT` (`.`)
- **Control:** `EOF`

### 3.2 `Token` (src/token.py — Immutable)
```python
@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
```
- `line` and `column` are **1-indexed** and point to the first character of the lexeme.
- `lexeme` is the exact source text slice (string literals retain surrounding quotes).
- Formats cleanly as: `Token(CLASS, "class", line=1, column=1)`.
- Value equality (`t1 == t2`) is automatic via `@dataclass(frozen=True)`.

### 3.3 `LexicalError` (src/errors.py — Immutable)
```python
@dataclass(frozen=True)
class LexicalError:
    message: str
    line: int
    column: int
```
- Emitted when an invalid character or unclosed literal is encountered.
- Standard format: `LexicalError("Error: invalid character '@' at line 2, column 4.", line=2, column=4)`.
- Scanning **continues** after an error is recorded (never crash or raise unhandled exceptions).

### 3.4 `SourceCursor` (src/cursor.py — Abstract Interface)
```python
class SourceCursor(ABC):
    @abstractmethod
    def peek(self) -> str: ...       # current char without consuming ('\0' at EOF)
    @abstractmethod
    def peekNext(self) -> str: ...   # char after current ('\0' at EOF)
    @abstractmethod
    def advance(self) -> str: ...    # consumes and returns current char; updates line/column
    @abstractmethod
    def isAtEnd(self) -> bool: ...
    @abstractmethod
    def getLine(self) -> int: ...    # 1-indexed line of NEXT char
    @abstractmethod
    def getColumn(self) -> int: ...  # 1-indexed column of NEXT char
```
- Pure abstract interface. Task 2 provides the concrete implementation.
- Must return sentinel `'\0'` when out of bounds; never raise an IndexError.

### 3.5 Shared Conventions (src/conventions.py)
- `KEYWORDS`: Dictionary mapping keyword strings to `TokenType` (`"String"` maps to `TokenType.STRING_TYPE`).
- `OPERATORS`: Dictionary mapping operators to `ASSIGN`, `LOGOP`, or `MATHOP`.
- `DELIMITERS`: Dictionary mapping punctuation symbols to delimiters.

---

## 4. Project Status & Roadmap

| Task | Module | Owner | Status | Deliverables & Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | Setup & Core Contracts | Karim Bassem | **DONE** | Frozen `TokenType`, `Token`, `LexicalError`, `SourceCursor`, conventions, repo structure. |
| **Task 2** | Cursor & Comments Engine | Karim Bassem | **PENDING** | Concrete cursor class implementing `SourceCursor`. Handle line/col tracking and skip whitespace/comments (`//`, `/* */`). |
| **Task 3** | Words & Literals Scanners | Mahmoud Farag | **PENDING** | Scan identifiers vs keywords (`KEYWORDS` lookup), integers, floats, and strings with escapes. |
| **Task 4** | Delimiters & Operators | Ali Essam | **PENDING** | Scan 1- and 2-char operators (`==`, `<=`, etc.), delimiters, and emit `LexicalError` for illegal chars. |
| **Task 5** | Symbol Table Structure | Ahmed Shalaby | **PENDING** | Custom hash table / symbol table to store identifiers, handle collisions, and store token metadata. |
| **Task 6** | CLI Driver & Formatter | Omar Walid | **PENDING** | Command-line interface to read source files, format token tables, and print errors. |
| **Task 7** | Lexer Pipeline Integration | Karim Bassem | **PENDING** | Main scanner loop coordinating cursor, sub-scanners, symbol table, and error list into `(tokens, errors)`. |
| **Task 8** | Verification & QA | All | **PENDING** | Run test corpus (`tests/test_programs.txt`), verify line/column accuracy, and test edge cases. |
| **Task 9** | Report & Final Submission | All | **PENDING** | Final documentation, code cleanup, and submission packaging. |

---

## 5. Guidelines for Future Tasks

### When implementing Task 2 (`SourceCursor`):
- Implement in `src/cursor.py` or a dedicated module `src/source_cursor.py`.
- Transparently support `\n` (LF), `\r\n` (CRLF), and `\r` (CR). Increment line and reset column to 1 on newline.
- Advance through whitespace (` `, `\t`, `\r`, `\n`) and skip single-line (`//...`) and block (`/* ... */`) comments.
- Emit a `LexicalError` if a block comment remains unclosed at EOF.

### When implementing Tasks 3 & 4 (Sub-Scanners):
- Sub-scanners should be small, simple functions or classes taking the cursor and returning `Token | None` or emitting a `LexicalError`.
- Keep them decoupled so Task 7 can chain them in priority order:
  1. Skip whitespace / comments
  2. Numbers / Strings / Words (Keywords vs Identifiers)
  3. Multi-character operators (`==`, `!=`, `<=`, `>=`)
  4. Single-character operators and delimiters
  5. Fallback: Illegal character → emit `LexicalError`, advance 1 char, continue scanning.

### When implementing Task 5 (Symbol Table):
- Create a simple, understandable hash table or dictionary wrapper that stores identifier occurrences, types, and scope attributes without excessive complexity.

### When implementing Task 6 (CLI Driver):
- Expand `src/main.py` to accept a file argument: `python3 -m src.main <path_to_source.java>`.
- Print cleanly formatted token stream and any lexical errors.

---

## 6. How to Run & Verify

```bash
# Run compiler entrypoint
python3 -m src.main

# Quick syntax check
python3 -m py_compile src/*.py
```
