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
| **Task 2** | Cursor & Comments Engine | Karim Bassem | **DONE** | Concrete `FileCursor` / `StringCursor` implementing `SourceCursor`. 1-indexed coordinates, CRLF handling, whitespace & comment skipping (`//`, `/* */`), and unclosed comment diagnostic. |
| **Task 3** | Words & Literals Scanners | Mahmoud Farag | **DONE** | `src/scanners.py`: `scan_word_or_number_or_string()` dispatches to `scan_word`, `scan_number_or_invalid_id`, `scan_string`. Returns `Token`, `LexicalError`, or `None` (no match). |
| **Task 4** | Delimiters & Operators | Ali Essam | **DONE** | `src/scanner_delimiters.py` — `scan_operator_or_delimiter(cursor)` returns `Token \| LexicalError`. Matches 2-char ops (`==`, `!=`, `<=`, `>=`) before 1-char ops, then delimiters, fallback emits `LexicalError` for illegal chars and advances past them. |
| **Task 5** | Symbol Table Structure | Ahmed Shalaby | **DONE** | `src/symbol_table.py`: `SymbolTable` (101 buckets, polynomial hash with multiplier 31, separate chaining). `insert(token, type=None, scope=None)` adds a new `SymbolEntry` or appends `(line, column)` to an existing one; `lookup(name)`, `entries()` (first-seen order), `len()`. |
| **Task 6** | CLI Driver & Formatter | Omar Walid | **DONE** | `src/main.py`: `main(argv)` CLI (`python -m src <file> [-o out] [--strict]`), file errors print one line and exit 1, lexical errors exit 0 (1 with `--strict`). `src/formatter.py`: `format_token`, `format_symbol_table`, `format_output(tokens, errors, table)` merges tokens and errors by `(line, column)` so errors print inline, then a `Symbol Table` section. `tests/test_programs.txt` (16 `### TEST NN: label` cases), `tests/expected/test_NN.out`, `tests/verify.py` (PASS/FAIL + unified diff), `tests/test_task6.py`. |
| **Task 7** | Lexer Pipeline Integration | Karim Bassem | **DONE** | `src/lexer.py`: `Lexer(source, on_token=None, on_error=None)` coordinates `SourceCursor`, comments/whitespace skipping, sub-scanners (`scan_word`, `scan_number_or_invalid_id`, `scan_string`, `scan_operator_or_delimiter`), and `SymbolTable`. `getNextToken()` (and alias `get_next_token()`) implements the main dispatch loop with panic-mode recovery; `tokenize()` consumes full input into `(tokens, errors, symbol_table)`. `tests/test_task7.py`. |
| **Task 8** | Verification & QA | Mahmoud Farag | **DONE** | Marked Completed in Notion. `docs/test_report.md` was committed empty; the test results (16/16 golden cases, LF = CRLF, 10,000-line file in ~0.1 s, Task 8 matrix probes) are summarised in the report's Testing section. |
| **Task 9** | Report & Final Submission | Omar Walid | **DONE** | `report.pdf` (2 A4 pages: token specs, error handling & recovery, challenges, testing & limitations), generated from `docs/report.html`. Submission zip `phase01-submission.zip` = `src/`, `tests/`, `README.md`, `report.pdf`, built with `git archive` (see Section 6). Code frozen at `3065ffd`. Still needs a teammate's clean-build check and proofreading. |

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

### Output format (Task 6, done):
- One line per token: `Lexeme: <val>, Token: <TYPE>`; EOF prints as `Lexeme: EOF, Token: EOF`.
- Errors print their `message` on their own line at their source position.
- After the token stream: a blank line, `Symbol Table`, then `Index: N, Name: x, Occurrences: line:col, ...` (or `(empty)`).

### Adding a test case (Task 8):
1. Append `### TEST NN: label` and the program to `tests/test_programs.txt` (line numbers restart at 1 inside each case).
2. Run `python tests/verify.py --write-missing` to create `tests/expected/test_NN.out`.
3. Review that file by hand (someone other than the author), then commit both.

---

## 6. How to Run & Verify

Use `python` (not `python3`) on Windows.

```bash
# Run the lexer on a file (prints tokens, inline errors, then the symbol table)
python -m src path/to/program.java
python -m src program.java -o result.txt   # write to a file
python -m src program.java --strict        # exit 1 if lexical errors were found

# Quick syntax check
python -m py_compile src/*.py

# Tests (plain scripts, no pytest)
python -X utf8 tests/test_task2.py
python -X utf8 -m tests.test_task3
python -X utf8 tests/test_task5.py
python -X utf8 tests/test_task6.py
python -X utf8 tests/test_task7.py

# Golden-output check of every case in tests/test_programs.txt
python tests/verify.py

# Rebuild report.pdf after editing docs/report.html (needs LibreOffice; must stay 2 pages)
soffice --headless --convert-to pdf:writer_web_pdf_Export --outdir . docs/report.html

# Build the submission zip from the latest commit (tracked files only)
git archive --format=zip --prefix=phase01-submission/ -o phase01-submission.zip HEAD src tests README.md report.pdf
```

---

## 7. Gotchas

- **No pytest:** tests are plain scripts using `assert` + `print`. Run them as shown in Section 6.
- **Windows console:** `-X utf8` is required, or the ✅ prints raise `UnicodeEncodeError`.
- **`test_task3.py` must run with `-m`:** running it as a file path fails with `ModuleNotFoundError: No module named 'src'`.
- **`StringCursor` is an alias:** `StringCursor = FileCursor` in `src/cursor.py`. `test_task3.py` defines its own mock with the same name.
- **Hash multiplier must differ from the table size:** with size 31 and multiplier 31, `h * 31 % 31 == 0`, so the hash only sees the last letter (`count`, `limit`, `result` all collide). The default size is 101 for this reason.
- **Spec alignment done in Task 6:** the unclosed block comment message is now `Error: unclosed comment starting at line L, column C.` (as in the PDF), and `scan_string` stops at the end of the line, so an unclosed string no longer swallows the rest of the file.
- **`true` / `false` are still `IDENTIFIER`:** the PDF says they should be literal tokens, but the frozen `TokenType` has no member for them. Team decision needed.
- **Report must match the code:** after any code change, re-run the sample and error example in `docs/report.html`, re-export `report.pdf`, and check it is still 2 pages (`pdfinfo report.pdf`). LibreOffice ignores CSS table borders, so tables use the HTML `border` attribute.
- **`git archive` only packs committed files:** commit `report.pdf` before building the zip.
- **`tests/test_programs.txt` starts with `### TEST` markers:** running the CLI on the whole file reports `#` as illegal characters; use `tests/verify.py`, which splits it into cases.
- **Task 3 goes beyond the frozen contract (confirm with the team):** `scan_string` accepts single-quoted `'...'` as `STRING`, and `scan_number_or_invalid_id` emits an "invalid identifier" `LexicalError` for inputs like `1name`.
