# Mini Java Compiler (Phase 01: Lexical Analysis)

CSCI415 - Compiler Design project. A lexical analyzer (scanner) built from scratch for Mini Java.

---

## Project Structure

```
compiler_project/
├── src/
│   ├── token_type.py   # Enum of all 31 token types
│   ├── token.py        # Token class (type, lexeme, line, column)
│   ├── errors.py       # LexicalError class (message, line, column)
│   ├── cursor.py       # SourceCursor abstract interface
│   ├── conventions.py  # Keywords, operators, and delimiters maps
│   └── main.py         # Entry point (prints nothing, exits 0)
├── tests/
│   └── test_programs.txt # Sample input programs
├── docs/               # Documentation & notes
├── README.md
└── AGENTS.md
```

---

## How to Run

Make sure you have Python 3.10+ installed:

```bash
# Run empty project
python3 -m src.main
```

---

## Core Contracts (Frozen)

### 1. `TokenType` (31 Members)
- **Class keywords:** `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `MAIN`
- **Type keywords:** `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`
- **Control keywords:** `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`
- **Literals & names:** `IDENTIFIER`, `NUMBER`, `STRING`
- **Operators:** `ASSIGN` (`=`), `MATHOP` (`+`, `-`, `*`, `/`), `LOGOP` (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Delimiters:** `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT`
- **Control:** `EOF`

### 2. `Token`
Immutable token object containing:
- `type`: `TokenType`
- `lexeme`: exact raw string from source
- `line`: 1-indexed line of the first character
- `column`: 1-indexed column of the first character

### 3. `LexicalError`
Immutable error diagnostic containing:
- `message`: error description string
- `line`: 1-indexed line of offending character
- `column`: 1-indexed column of offending character

### 4. `SourceCursor`
Abstract interface to traverse the source code character by character:
- `peek()`: look at current char (returns `'\0'` at EOF)
- `peekNext()`: look at next char (returns `'\0'` at EOF)
- `advance()`: consume and return current char
- `isAtEnd()`: returns boolean
- `getLine()`: current 1-indexed line
- `getColumn()`: current 1-indexed column

---

## Branch & Collaboration Rules

- `main` branch is protected.
- Each teammate works on their branch: `task-N-short-name` (e.g. `task-2-cursor`).
- Pull requests need at least 1 teammate review before merge.

---

## Team Tasks

- **Task 1:** Setup & Contracts (Karim) - *Done*
- **Task 2:** Cursor & Comments (Karim)
- **Task 3:** Words, Numbers & Strings (Mahmoud)
- **Task 4:** Delimiters & Operators (Ali)
- **Task 5:** Symbol Table (Ahmed)
- **Task 6:** CLI Driver & Formatter (Omar)
- **Task 7:** Pipeline Integration (Karim)
- **Task 8:** Testing & Bug Fixing (All)
- **Task 9:** Final Report & Presentation (All)
