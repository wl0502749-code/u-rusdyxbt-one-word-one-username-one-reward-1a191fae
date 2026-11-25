#!/usr/bin/env python3
"""One Word, One Username, One Reward.

Writes the entrant's own make.fun username -- one word, nothing else --
to /output/entry.txt, where the judge reads it.

The gate only accepts UTF-8 text of 1 to 30 characters that is not
only whitespace, so the username is checked against exactly those
rules before it is written, and the file is read back to confirm it
landed byte for byte. No network, no randomness, no clock: two runs
produce the same file.
"""

import os
import sys

USERNAME = "swift-finch-52-3460"


def validate(username: str) -> None:
    """Reject anything the gate would refuse, before writing it."""
    if not isinstance(username, str):
        raise TypeError("username must be text")
    if not 1 <= len(username) <= 30:
        raise ValueError("username must be 1 to 30 characters")
    if not username.strip():
        raise ValueError("username must not be only whitespace")
    if len(username.split()) != 1:
        raise ValueError("username must be a single word, no spaces")
    if any(ch.isspace() for ch in username):
        raise ValueError("username must contain no whitespace")


def main() -> int:
    validate(USERNAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(USERNAME)
    with open(path, "rb") as f:
        written = f.read()
    if written != USERNAME.encode("utf-8"):
        print("entry.txt does not match the username byte for byte", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
