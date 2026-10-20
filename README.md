# Mini Java Compiler — Phase 01: Lexical Analysis

A robust, modular lexical analyzer for the Mini Java programming language, developed from scratch without external lexical libraries for **CSCI415 - Compiler Design (Fall 2026)**.

---

## 1. Repository Structure

```
mini-java-compiler/
├── src/                # Lexer source modules (one file per component)
│   ├── __init__.py     # Contract exports
│   ├── __main__.py     # Module execution entrypoint (`python -m src`)
│   ├── main.py         # Application entrypoint & CLI driver placeholder
│   ├── token_type.py   # TokenType enum (exactly 31 members)
│   ├── token.py        # Immutable Token data contract
│   ├── errors.py       # Immutable LexicalError data contract
│   ├── cursor.py       # Abstract SourceCursor interface
│   └── conventions.py  # Frozen shared keywords, operators & delimiter tables
├── tests/              # Test corpus, expected outputs & verification suite
│   ├── __init__.py
│   ├── test_contracts.py  # Comprehensive contract unit tests
│   ├── test_programs.txt  # Input sample programs corpus
│   └── verify.sh          # Full project verification script
├── docs/               # Technical contracts & architectural design notes
│   ├── contracts.md    # Detailed frozen contract specification
│   └── design_notes.md # Component architecture & data flow
├── AGENTS.md           # Authoritative AI & developer architectural guide
├── README.md           # Build, run, and contribution guidelines
└── .gitignore
```

---

## 2. Quickstart: Build & Run from Clean Checkout

### Prerequisites
- Python 3.10+ (Standard Library only; zero 3rd-party dependencies required for Phase 01).

### Build & Syntax Validation
Verify that all source modules compile without syntax errors:
```bash
python3 -m py_compile src/*.py tests/*.py
```

### Execution (Task 1 Placeholder)
Running the empty project executes cleanly with zero output and exits code 0:
```bash
python3 -m src.main
```
Or via module execution:
```bash
python3 -m src
```

### Running Test Suite
Execute all contract verification tests:
```bash
python3 -m unittest discover -s tests -v
```

### One-Command Verification
Run the automated verification script:
```bash
./tests/verify.sh
```

---

## 3. Git Workflow & Contribution Rules

To enable parallel execution across all 5 teammates without merge conflicts, adhere strictly to these rules:

1. **Protected `main` Branch:**
   - Direct pushes to `main` are strictly forbidden.
   - All shared contracts in `src/token_type.py`, `src/token.py`, `src/errors.py`, and `src/cursor.py` are **FROZEN**.
2. **Branch Naming Standard:**
   - Every contributor develops on an isolated feature branch using the format:
     `task-N-short-name`
     (e.g., `task-2-cursor-comments`, `task-3-word-scanners`, `task-4-delimiters`, `task-5-symbol-table`, `task-6-cli-driver`).
3. **Pull Request (PR) Policy:**
   - Every PR requires at least **one peer code review and approval** from another teammate before merging into `main`.
   - CI / local verification (`./tests/verify.sh`) must pass with zero errors.
   - Any proposed change to frozen contracts requires a team-wide message and consensus before opening a PR.

---

## 4. Core Data Contracts Overview

### `TokenType` (Exactly 31 Members)
- **Class-structure keywords (5):** `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `MAIN`
- **Type keywords (5):** `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`
- **Control keywords (5):** `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`
- **Literals & names (3):** `IDENTIFIER`, `NUMBER`, `STRING`
- **Operators (3):** `ASSIGN` (`=`), `MATHOP` (`+`, `-`, `*`, `/`), `LOGOP` (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Delimiters (9):** `LPAR` (`(`), `RPAR` (`)`), `LCUR` (`{`), `RCUR` (`}`), `LSQU` (`[`), `RSQU` (`]`), `SEMICOLON` (`;`), `COMMA` (`,`), `DOT` (`.`)
- **Control (1):** `EOF`

### `Token` (Immutable)
```python
Token(type: TokenType, lexeme: str, line: int, column: int)
```
- Line and column are **1-indexed** (pointing to the first character of the lexeme).
- String literals preserve original quotes in `lexeme`.
- Immutability enforced via `@dataclass(frozen=True)`.
- Value equality: `t1 == t2` evaluates `True` when all 4 fields match.

### `LexicalError` (Immutable)
```python
LexicalError(message: str, line: int, column: int)
```
- Emitted on illegal characters or malformed tokens; lexical scanning continues.

### `SourceCursor` (Abstract Interface)
```python
class SourceCursor(ABC):
    def peek(self) -> str: ...       # Returns char or '\0' at EOF (never throws)
    def peekNext(self) -> str: ...   # Returns char or '\0' at EOF (never throws)
    def advance(self) -> str: ...    # Consumes char, advances line/column
    def isAtEnd(self) -> bool: ...
    def getLine(self) -> int: ...    # 1-indexed line of NEXT char
    def getColumn(self) -> int: ...  # 1-indexed column of NEXT char
```

---

## 5. Team Roles & Milestones

| Task | Owner | Module / Responsibility | Deadline |
| :--- | :--- | :--- | :--- |
| **Task 1** | Karim Bassem Joseph | Repository Setup & Shared Core Contracts | Oct 21, 2026 |
| **Task 2** | Karim Bassem Joseph | SourceCursor Implementation & Comment/Whitespace Engine | Oct 23, 2026 |
| **Task 3** | Mahmoud Farag | Word, Number & String Literal Sub-Scanners | Oct 23, 2026 |
| **Task 4** | Ali Essam | Delimiters, Operators & Illegal Character Scanner | Oct 23, 2026 |
| **Task 5** | Ahmed Shalaby | Custom Symbol Table Data Structure | Oct 23, 2026 |
| **Task 6** | Omar Walid | CLI Driver, Formatter & Comprehensive Test Suite | Oct 24, 2026 |
| **Task 7** | Karim Bassem Joseph | Sequential Lexer Pipeline Integration | Oct 26, 2026 |
| **Task 8** | All Teammates | Test Suite Validation & Bug Squashing | Oct 27, 2026 |
| **Task 9** | All Teammates | Phase 01 Report & Submission Packaging | Oct 28, 2026 |
