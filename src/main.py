"""DocuGen entry point for running the lexer on a sample Python file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lexer.lexer import tokenize


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DocuGen lexer on a Python file")
    parser.add_argument(
        "path",
        nargs="?",
        default="tests/sample.py",
        help="Path to Python source file (default: tests/sample.py)",
    )
    args = parser.parse_args()

    source_path = Path(args.path)
    if not source_path.exists():
        print(f"File not found: {source_path}", file=sys.stderr)
        return 1

    source_code = source_path.read_text(encoding="utf-8")
    tokens, errors = tokenize(source_code)

    for token in tokens:
        print(
            f"{token.type:<16} value={token.value!r} line={token.lineno} column={token.column}"
        )

    if errors:
        print("\nLexical errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
