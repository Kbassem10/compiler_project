import difflib
import sys
from pathlib import Path

# Add project root to sys.path so it runs directly or with -m
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.formatter import format_output
from src.lexer import tokenize

PROGRAMS = ROOT / "tests" / "test_programs.txt"
EXPECTED_DIR = ROOT / "tests" / "expected"
MARKER = "### TEST "


def split_cases(text: str) -> list[tuple[str, str, str]]:
    """Split the corpus into (number, label, program) cases."""
    cases = []
    for line in text.splitlines():  # splitlines() handles \n, \r\n and \r
        if line.startswith(MARKER):
            number, label = line[len(MARKER):].split(":", 1)
            cases.append((number.strip(), label.strip(), []))
        elif cases:  # text before the first marker is ignored
            cases[-1][2].append(line)
    return [(number, label, "\n".join(body)) for number, label, body in cases]


def run_case(program: str) -> str:
    tokens, errors, table = tokenize(program)
    return format_output(tokens, errors, table)


def main() -> int:
    # --write-missing creates expected files for new cases (review them by hand!)
    write_missing = "--write-missing" in sys.argv
    cases = split_cases(PROGRAMS.read_text(encoding="utf-8"))
    failed = 0

    for number, label, program in cases:
        actual = run_case(program)
        expected_file = EXPECTED_DIR / f"test_{number}.out"

        if not expected_file.exists():
            if write_missing:
                EXPECTED_DIR.mkdir(exist_ok=True)
                expected_file.write_text(actual, encoding="utf-8")
                print(f"NEW  TEST {number}: {label} -> wrote {expected_file.name}")
            else:
                failed += 1
                print(f"FAIL TEST {number}: {label} (missing {expected_file.name})")
            continue

        # Only trailing whitespace at the end of the file is ignored
        expected = expected_file.read_text(encoding="utf-8").rstrip()
        if expected == actual.rstrip():
            print(f"PASS TEST {number}: {label}")
        else:
            failed += 1
            print(f"FAIL TEST {number}: {label}")
            diff = difflib.unified_diff(
                expected.splitlines(), actual.rstrip().splitlines(),
                "expected", "actual", lineterm="",
            )
            print("\n".join(diff))

    print(f"\n{len(cases) - failed}/{len(cases)} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
