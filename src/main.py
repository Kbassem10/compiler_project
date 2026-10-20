"""Mini Java Compiler entrypoint placeholder.

Task 1 requirement: Empty project builds and runs with the documented command
(prints nothing, exits 0). Task 6 will flesh out the full CLI driver.
"""

import sys


def main(argv: list[str] | None = None) -> int:
    """CLI driver entrypoint."""
    if argv is None:
        argv = sys.argv[1:]
    # With no arguments or placeholder state: exit 0 cleanly printing nothing.
    return 0


if __name__ == "__main__":
    sys.exit(main())
