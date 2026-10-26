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
│   ├── cursor.py       # SourceCursor interface & FileCursor / StringCursor
│   ├── conventions.py  # Keywords, operators, and delimiters maps
│   ├── scanners.py     # Task 3 word, number & string sub-scanners
│   ├── scanner_delimiters.py # Task 4 operators, delimiters & illegal chars
│   ├── symbol_table.py # Task 5 hash-table symbol table (chaining)
│   ├── lexer.py        # Main scanning loop: tokenize(source)
│   ├── formatter.py    # Task 6 output formatter (tokens, errors, symbol table)
│   ├── main.py         # Task 6 CLI entry point
│   └── __main__.py     # Lets the package run with `python -m src`
├── tests/
│   ├── test_programs.txt # Labelled test programs (### TEST NN: label)
│   ├── expected/         # Expected output for each test (test_NN.out)
│   ├── verify.py         # Runs every test program and diffs against expected/
│   ├── test_task2.py     # Task 2 cursor & comments test suite
│   ├── test_task3.py     # Task 3 scanners test suite
│   ├── test_task5.py     # Task 5 symbol table test suite
│   ├── test_task6.py     # Task 6 CLI & formatter test suite
│   └── test_task7.py     # Task 7 lexer pipeline integration test suite
├── docs/               # Documentation & notes
├── README.md
└── AGENTS.md
```

---

## How to Run

Make sure you have Python 3.10+ installed (on Windows use `python`, not `python3`):

```bash
# Scan a Mini Java file
python -m src path/to/program.java
python -m src program.java -o result.txt   # save the output to a file
python -m src program.java --strict        # exit code 1 if lexical errors were found

# Run tests (-X utf8 is needed on Windows consoles)
python -X utf8 tests/test_task2.py
python -X utf8 -m tests.test_task3
python -X utf8 tests/test_task5.py
python -X utf8 tests/test_task6.py
python -X utf8 tests/test_task7.py

# Check every program in tests/test_programs.txt against tests/expected/
python tests/verify.py
```

Example output:

```
Lexeme: int, Token: INT
Lexeme: x, Token: IDENTIFIER
Lexeme: =, Token: ASSIGN
Lexeme: 10, Token: NUMBER
Error: invalid character '@' at line 1, column 12.
Lexeme: 5, Token: NUMBER
Lexeme: ;, Token: SEMICOLON
Lexeme: EOF, Token: EOF

Symbol Table
Index: 0, Name: x, Occurrences: 1:5
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
- **Task 2:** Cursor & Comments (Karim) - *Done*
- **Task 3:** Words, Numbers & Strings (Mahmoud) - *Done*
- **Task 4:** Delimiters & Operators (Ali) - *Done*
- **Task 5:** Symbol Table (Ahmed) - *Done*
- **Task 6:** CLI Driver & Formatter (Omar) - *Done*
- **Task 7:** Pipeline Integration (Karim)
- **Task 8:** Testing & Bug Fixing (All)
- **Task 9:** Final Report & Presentation (All)
