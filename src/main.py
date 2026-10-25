import argparse
import sys

from .formatter import format_output
from .lexer import tokenize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src", description="Mini Java lexical analyzer")
    parser.add_argument("source", help="Mini Java source file to scan")
    parser.add_argument("-o", "--output", help="write the output to this file instead of the screen")
    parser.add_argument("--strict", action="store_true", help="exit with code 1 if any lexical error is found")
    args = parser.parse_args(argv)  # prints usage and exits with code 2 on bad arguments

    try:
        with open(args.source, encoding="utf-8") as f:
            source = f.read()
    except OSError as e:  # missing file, directory, no permission
        print(f"Error: cannot read '{args.source}': {e.strerror}.", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Error: '{args.source}' is not a UTF-8 text file.", file=sys.stderr)
        return 1

    tokens, errors, table = tokenize(source)
    output = format_output(tokens, errors, table)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
        except OSError as e:
            print(f"Error: cannot write '{args.output}': {e.strerror}.", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(output)

    # Lexical errors are normal output, so exit 0 unless --strict is given
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
