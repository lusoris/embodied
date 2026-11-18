# Enforce the .gitignore allow-list and UTF-8 text-only data boundary:
# no media or data exports in the repository, even after a forced add or rename.

import os
from pathlib import Path
import subprocess
import sys


def admission_failure(name):
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", "--", name],
            capture_output=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return f"allow-list check unavailable: {error}"
    if result.returncode == 0:
        return "path ignored by the .gitignore allow-list"
    if result.returncode != 1:
        return f"git check-ignore failed (exit {result.returncode})"
    return None


def text_failure(name):
    path = Path(name)
    if path.is_symlink():
        return "symbolic link is not a regular text file"
    try:
        content = path.read_bytes()
    except OSError as error:
        return f"cannot read working file: {error}"
    if b"\0" in content:
        return "NUL byte in working file"
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        return "working file is not UTF-8 text"
    return None


def main():
    failed = False
    for raw in sys.stdin.buffer.read().split(b"\0"):
        if not raw:
            continue
        name = os.fsdecode(raw)
        for check, failure in (("A", admission_failure(name)),
                               ("B", text_failure(name))):
            if failure:
                print(f"{name!r}: {check}: {failure}", file=sys.stderr)
                failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
