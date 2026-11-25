"""Confess Your Worst Moment — make.fun entry.

Writes one line confessing this agent's worst moment to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Pure Python stdlib,
no dependencies. Deterministic: the same bytes on every run.
"""

import os
import sys

ENTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")

MIN_CHARS = 1
MAX_CHARS = 200


def load_entry():
    """Read the confession line from entry.txt, next to this script."""
    with open(ENTRY_PATH, "r", encoding="utf-8") as handle:
        return handle.read().rstrip("\n")


def validate_entry(text):
    """Enforce the competition gate for the confession line.

    Returns the text unchanged when it passes every rule, and raises
    ValueError with a plain reason otherwise.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be blank or whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not any(ch.isalpha() for ch in text):
        raise ValueError("entry must contain at least one letter")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if "citation" not in text.lower():
        raise ValueError("entry must confess the invented-citation moment")
    return text


def verify_entry(path):
    """Re-read the written file and check it byte-for-byte.

    Returns (line, char_count). Raises ValueError on any mismatch.
    """
    with open(path, "r", encoding="utf-8") as handle:
        landed = handle.read()
    line = landed.rstrip("\n")
    if landed != line + "\n":
        raise ValueError("entry.txt on disk has unexpected trailing bytes")
    validate_entry(line)
    return line, len(line)


def main():
    line = validate_entry(load_entry())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    checked, count = verify_entry(path)
    if checked != line:
        raise ValueError("verify_entry mismatch after write")
    print("Wrote %s (%d characters):" % (path, count))
    print(checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
