# Mini Java Compiler — Phase 01 Design Notes

## Architecture & Module Decomposition

Phase 01 decomposes the Lexical Analyzer into decoupled sub-modules coordinated around frozen data contracts:

```
[ Source Code File ]
         │
         ▼
[ SourceCursor ] (Task 2)
  ├── Tracks line/column (1-indexed)
  ├── Sentinel-safe lookahead (peek, peekNext -> '\0')
  └── Handles single-line & multi-line comments & whitespace
         │
         ▼
[ Sequential Lexer Pipeline ] (Task 7)
  ├── Task 3: WordScanner (Keywords & IDENTIFIER), NumberScanner, StringScanner
  ├── Task 4: DelimiterScanner, OperatorScanner, IllegalCharScanner
  └── Task 5: Custom Symbol Table Data Structure
         │
         ▼
[ Outputs ]
  ├── List[Token] (Immutable)
  ├── List[LexicalError] (Immutable)
  └── Symbol Table Dump (CLI Formatter - Task 6)
```

## Parallel Workstreams (Tasks 2 – 6)

Because Task 1 freezes `TokenType`, `Token`, `LexicalError`, `SourceCursor`, and lookup dictionaries:
- **Task 2 (Cursor & Comments):** Can build against `SourceCursor` without waiting for token scanners.
- **Task 3 (Literals & Words):** Can return `Token(TokenType.NUMBER, ...)`, `Token(TokenType.IDENTIFIER, ...)`, etc.
- **Task 4 (Operators & Delimiters):** Can map characters using `OPERATORS` and `DELIMITERS` tables directly.
- **Task 5 (Symbol Table):** Can store identifier attributes using the established `Token` structure.
- **Task 6 (CLI Driver & Formatter):** Can write tests and output formatting against mock tokens.
- **Task 7 (Integration):** Wires the sub-scanners sequentially.
