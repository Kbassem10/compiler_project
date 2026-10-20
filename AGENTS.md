# AGENTS.md — System Architecture, Context & Compiler Implementation Guide

This document serves as the authoritative architectural blueprint and developer/agent reference for the **Mini Java Compiler** (`mini-java-compiler`). Any AI coding assistant or engineer working on this codebase MUST follow the specifications and constraints documented here.

---

## 1. System Overview & Core Philosophy

The **Mini Java Compiler** is an educational, production-grade compiler pipeline built from scratch without external lexical/parsing generators (e.g., Lex, Yacc, ANTLR). 

Phase 01 implements **Lexical Analysis (Scanner)** with high-precision diagnostics, exact source positioning, and custom symbol table resolution.

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
│  - Sentinel-safe lookahead: peek(), peekNext() -> '\0'      │
│  - Strips whitespace & single-line / multi-line comments    │
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
│  - Illegal Character Scanner: Diagnostic error generation   │
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

### Key Principles:
1. **Zero External Runtime Dependencies:** Everything is implemented using modern standard Python (3.10+). No 3rd-party parsing packages (`ply`, `antlr`, `regex`).
2. **Frozen Data Contracts:** Modules communicate solely via the frozen interfaces defined in `src/token_type.py`, `src/token.py`, `src/errors.py`, and `src/cursor.py`.
3. **Decoupled Parallel Development:** Each team member develops their sub-scanner in isolation on dedicated branches (`task-N-short-name`) without cross-blocking.
4. **Diagnostic Integrity:** Scanner never crashes on unexpected syntax. An illegal character or unclosed literal emits a `LexicalError` and scanning continues until `EOF`.

---

## 2. Frozen Data Contracts Reference

The contracts established in **Task 1** are permanently frozen. Any modification requires team-wide consensus.

### 2.1 TokenType (Exactly 31 Members)
Character-for-character exact enum names across 7 groups:
- **Class-structure:** `CLASS`, `PUBLIC`, `STATIC`, `VOID`, `MAIN`
- **Type keywords:** `INT`, `FLOAT`, `BOOLEAN`, `CHAR`, `STRING_TYPE`
- **Control keywords:** `IF`, `ELSE`, `WHILE`, `FOR`, `RETURN`
- **Literals & Names:** `IDENTIFIER`, `NUMBER`, `STRING`
- **Operators:** `ASSIGN` (`=`), `MATHOP` (`+`, `-`, `*`, `/`), `LOGOP` (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Delimiters:** `LPAR` (`(`), `RPAR` (`)`), `LCUR` (`{`), `RCUR` (`}`), `LSQU` (`[`), `RSQU` (`]`), `SEMICOLON` (`;`), `COMMA` (`,`), `DOT` (`.`)
- **Control:** `EOF`

### 2.2 Token (Immutable)
- `@dataclass(frozen=True)`
- Fields: `type: TokenType`, `lexeme: str`, `line: int`, `column: int`.
- **Invariants:**
  - `line` and `column` are **1-indexed** and point to the **first character** of the token.
  - `lexeme` contains the exact slice from source text. String literals retain surrounding quotation marks.
  - `EOF` token is emitted once, positioned immediately after the last character.
  - Two tokens with identical attributes compare equal (`t1 == t2`).

### 2.3 LexicalError (Immutable)
- `@dataclass(frozen=True)`
- Fields: `message: str`, `line: int`, `column: int`.
- **Invariants:**
  - `line` and `column` point to the start of the offending construct.
  - Standard format: `"Error: invalid character '@' at line 2, column 4."`.

### 2.4 SourceCursor (Abstract Interface)
- Method contracts:
  - `peek() -> str`: returns current character, or `'\0'` at EOF (never raises).
  - `peekNext() -> str`: returns character after current, or `'\0'` at EOF (never raises).
  - `advance() -> str`: consumes character, updates line/column, returns consumed char.
  - `isAtEnd() -> bool`: returns boolean indicator.
  - `getLine() -> int`: 1-indexed line of NEXT character to read.
  - `getColumn() -> int`: 1-indexed column of NEXT character to read.

---

## 3. Subsystem Breakdown & Task Allocations

| Task | Module | Assignee | Deliverable & Interface Contract |
| :--- | :--- | :--- | :--- |
| **Task 1** | Setup & Contracts | Karim Bassem Joseph | Frozen definitions: `TokenType`, `Token`, `LexicalError`, `SourceCursor`, repo structure, CI verification. |
| **Task 2** | Cursor & Comments | Karim Bassem Joseph | Concrete `SourceCursor` implementation. Skip whitespace (` `, `\t`, `\r`, `\n`) and handle `//...` and `/* ... */` comments. |
| **Task 3** | Words & Literals | Mahmoud Farag | Keyword vs `IDENTIFIER` discriminator, numeric scanner (integers/floats), string literal scanner with escape validation. |
| **Task 4** | Delimiters & Operators | Ali Essam | Multi-character lookahead for operators (`==`, `<=`, etc.), single delimiters, illegal character error generation. |
| **Task 5** | Symbol Table | Ahmed Shalaby | Custom hash table / lookup structure for identifiers. Handles collisions and attribute storage. |
| **Task 6** | CLI Driver & Formatter | Omar Walid | Command-line interface, token stream printer, error reporter, test suite driver. |
| **Task 7** | Pipeline Integration | Karim Bassem Joseph | Sequential dispatcher loop: coordinates cursor, sub-scanners, symbol table, and error list. |
| **Task 8** | Validation & QA | Entire Team | Edge-case fuzzing, comprehensive test corpus validation, memory and boundary verification. |
| **Task 9** | Packaging & Report | Entire Team | Final documentation, presentation slides, code cleanup, submission bundle. |

---

## 4. Coding Standards & Architectural Guidelines

### Defensive Access & Invariant Preservation
- Always validate incoming arguments. Never assume non-empty or non-null values.
- Verify 1-indexed positions on all token/error instances (`line >= 1`, `column >= 1`).
- Never perform in-place mutation on `Token` or `LexicalError` objects.

### Cross-Platform Portability
- Platform-agnostic path handling: Always use `pathlib.Path` or `os.path.join`. Never hardcode machine-bound absolute paths.
- Line ending resilience: Support LF (`\n`), CRLF (`\r\n`), and CR (`\r`) transparently in `SourceCursor`.

### Verification Requirement
Every PR must pass the automated verification command before requesting review:
```bash
./tests/verify.sh
```
Or manually:
```bash
python3 -m unittest discover -s tests -v
```

---

## 5. Handoff & Branching Strategy

1. All developers MUST branch off `main` after Task 1 is merged.
2. Branch naming convention: `task-<N>-<description>` (e.g. `task-2-cursor-engine`).
3. PRs require a passing test suite and review by at least one teammate.
