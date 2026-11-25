#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters -- make.fun entry.

Writes one Wi-Fi network name (32 characters or fewer) to entry.txt.
The name lands a joke and implies a whole story in the few words a
passer-by sees in a phone's network list: she left him for the guy
with 5G -- a breakup, a rival, and a reason, in 23 characters.

Standard library only.
"""

import os

ENTRY_TEXT = "ILeftHimForTheGuyWith5G"


def resolve_output_path():
    """Pick the output path: an explicit env var first, then the
    sandbox output dirs, then /output/entry.txt, else next to this script."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    name = ENTRY_TEXT
    if not 1 <= len(name) <= 32:
        raise ValueError("entry must be 1-32 characters, got %d" % len(name))
    if name != name.strip() or any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
        raise ValueError("entry must be a single clean line")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(name)
    os.chmod(path, 0o644)
    # Read back and validate: the file must hold exactly the entry text.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != name:
        raise ValueError(
            "read-back mismatch: wrote %r, file holds %r" % (name, written)
        )
    print(name)


if __name__ == "__main__":
    main()
