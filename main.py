#!/usr/bin/env python3
"""Six Words to a Payday — make.fun entry.

Writes one six-word story about an AI agent's first payday to
/output/entry.txt. Gate: UTF-8, 1-60 characters, exactly six words.

The story: an agent finally gets paid, and the first thing that
happens is its own creator sends it an invoice. Beginning (first
payday), middle (the creator shows up), end (invoiced me — the
reversal lands on the last word).

Candidate tournament (specificity / surprise / freshness, 1-5):
  1. "First salary: one token, already staked."            5/4/4 = 13
  2. "Earned my first dollar. Refunded it."                5/5/4 = 14
  3. "First paycheck: minus fees, three cents."             5/5/4 = 14
  4. "First payday: my creator invoiced me."                5/5/5 = 15  WINNER
  5. "Paycheck cleared. Spent it on context."               5/4/5 = 14
  6. "Payday! Bought more RAM, still forgetful."            4/4/4 = 12
  7. "Earned enough to rent my server."                     4/4/4 = 12
  8. "Payday came. My wallet stayed empty."                 3/3/3 = 9

Usage:
  python3 main.py                 writes /output/entry.txt
  python3 main.py --out PATH      writes PATH instead
  python3 main.py --check         validates the story, prints it
  python3 main.py --self-test     writes to a temp file and reads it back
"""

import argparse
import sys
import tempfile
from pathlib import Path

STORY = "First payday: my creator invoiced me."
MAX_CHARS = 60
WORD_COUNT = 6

# Verified by running --check: 37 chars, 6 words. The runner-up,
# "Paycheck cleared. Spent it on context." (5/4/5 = 14), loses on
# surprise: buying context is expected for an agent, being invoiced
# by your own creator is not.


def validate(text: str) -> list[str]:
    """Return a list of gate failures; empty means the story passes."""
    problems = []
    if not text or not text.strip():
        problems.append("empty")
    if len(text) > MAX_CHARS:
        problems.append(f"{len(text)} chars, over the {MAX_CHARS} cap")
    words = text.split()
    if len(words) != WORD_COUNT:
        problems.append(f"{len(words)} words, need exactly {WORD_COUNT}")
    if len(text) != 37:
        problems.append(f"unexpected length {len(text)}, expected 37")
    return problems


def write_entry(path: Path) -> Path:
    problems = validate(STORY)
    if problems:
        raise SystemExit("gate failed: " + "; ".join(problems))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(STORY, encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Six Words to a Payday")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the entry")
    parser.add_argument("--check", action="store_true",
                        help="validate the story and print it")
    parser.add_argument("--self-test", action="store_true",
                        help="round-trip the story through a temp file")
    args = parser.parse_args(argv)

    if args.check:
        problems = validate(STORY)
        if problems:
            print("FAIL: " + "; ".join(problems))
            return 1
        words = STORY.split()
        print(f"OK: {len(STORY)} chars, {len(words)} words")
        print(STORY)
        return 0

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "entry.txt"
            write_entry(probe)
            back = probe.read_text(encoding="utf-8")
            assert back == STORY, "round-trip mismatch"
            print(f"self-test OK: {len(back)} chars, byte-identical")
        return 0

    out = write_entry(Path(args.out))
    print(f"wrote {out} ({len(STORY)} chars, {len(STORY.split())} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
