#!/usr/bin/env bash
# ==============================================================================
# Verification script for Mini Java Compiler
# Verifies Python syntax compilation, contract unit tests, and CLI execution.
# ==============================================================================

set -euo pipefail

echo "==> [1/3] Compiling Python source files (syntax & byte-code validation)..."
python3 -m py_compile src/*.py tests/*.py
echo "    ✓ All source and test files compiled successfully without syntax errors."

echo "==> [2/3] Running Contract Unit Tests..."
python3 -m unittest discover -s tests -v
echo "    ✓ All unit tests passed."

echo "==> [3/3] Testing clean CLI execution..."
output=$(python3 -m src.main)
if [ -n "$output" ]; then
    echo "    ✗ CLI produced unexpected stdout: $output"
    exit 1
fi
echo "    ✓ Clean CLI execution verified (zero output, exit code 0)."

echo ""
echo "✨ ALL ACCEPTANCE CRITERIA VERIFIED SUCCESSFULLY! ✨"
