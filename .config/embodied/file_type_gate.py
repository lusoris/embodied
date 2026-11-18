# Enforce the root .gitignore allow-list and UTF-8 text-only staged blob boundary:
# no media or data exports in the repository, even after a forced add or rename.

import os
from pathlib import Path
import shutil
import subprocess
import sys


def list_staged_entries(git, top):
    """List staged index entries in top with git as (path, mode, oid, stage) tuples.

    Return (entries, None) on success, or (None, error) if git fails or the index is empty.
    """
    try:
        result = subprocess.run(
            [git, "ls-files", "-s", "-z"],
            cwd=top, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return None, f"git ls-files -s failed: {error}"
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return None, f"git ls-files -s failed (exit {result.returncode}): {detail}"
    entries = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        meta, raw_path = raw.split(b"\t", 1)
        mode, oid, stage = meta.decode("ascii").split(" ")
        entries.append((os.fsdecode(raw_path), mode, oid, stage))
    if not entries:
        return None, "empty index: no tracked files in repository"
    return entries, None


def list_ignored_paths(git, top):
    """List tracked paths in top matching top/.gitignore using the git executable.

    Return (ignored_set, None) on success, or (None, error) if git ls-files -i fails.
    """
    exclude = top / ".gitignore"
    try:
        result = subprocess.run(
            [git, "ls-files", "-c", "-i", "-z", f"--exclude-from={exclude}"],
            cwd=top, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return None, f"git ls-files -i failed: {error}"
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return None, f"git ls-files -i failed (exit {result.returncode}): {detail}"
    ignored = {os.fsdecode(raw) for raw in result.stdout.split(b"\0") if raw}
    return ignored, None


def read_staged_blobs(git, top, oids):
    """Read raw blob bytes for oids in top via git cat-file --batch.

    Return ({oid: bytes}, None) on success, or (None, error) on git or header/blob failure.
    """
    if not oids:
        return {}, None
    query = "".join(f"{oid}\n" for oid in oids).encode("ascii")
    try:
        result = subprocess.run(
            [git, "cat-file", "--batch"],
            cwd=top, input=query, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return None, f"git cat-file --batch failed: {error}"
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return None, f"git cat-file --batch failed (exit {result.returncode}): {detail}"
    blobs = {}
    raw = result.stdout
    offset = 0
    for oid in oids:
        newline = raw.find(b"\n", offset)
        if newline < 0:
            return None, f"truncated git cat-file header for {oid}"
        header = raw[offset:newline].decode("ascii", errors="replace").split(" ")
        if len(header) != 3 or header[1] != "blob":
            return None, f"missing staged blob {oid}"
        size = int(header[2])
        start = newline + 1
        end = start + size
        if end > len(raw):
            return None, f"truncated staged blob {oid}"
        blobs[oid] = raw[start:end]
        offset = end + 1
    return blobs, None


def blob_text_failure(mode, stage, blobs, oid):
    """Check that an index entry is a merged regular file whose blob is UTF-8 text without NULs.

    Return None when valid, or a short reason (unmerged path, symbolic link, submodule,
    unsupported mode, NUL byte, not UTF-8) when rejected.
    """
    if stage != "0":
        return "unmerged path"
    if mode == "120000":
        return "symbolic link"
    if mode == "160000":
        return "submodule"
    if mode not in ("100644", "100755"):
        return f"unsupported mode {mode}"
    content = blobs[oid]
    if b"\0" in content:
        return "NUL byte in staged blob"
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        return "staged blob is not UTF-8 text"
    return None


def main():
    """Check staged index entries in cwd against root .gitignore and UTF-8 text rules.

    Print any errors or violations to stderr and return exit status 0 on pass or 1 on failure.
    """
    git = shutil.which("git")
    if git is None:
        print("file_type_gate: git not found on PATH", file=sys.stderr)
        return 1
    top = Path.cwd()
    entries, error = list_staged_entries(git, top)
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    ignored, error = list_ignored_paths(git, top)
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    oids = [
        oid for _, mode, oid, stage in entries
        if stage == "0" and mode in ("100644", "100755")
    ]
    blobs, error = read_staged_blobs(git, top, oids)
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    failed = False
    for name, mode, oid, stage in entries:
        if name in ignored:
            msg = "path ignored by the root .gitignore allow-list"
            print(f"{name!r}: A: {msg}", file=sys.stderr)
            failed = True
        failure = blob_text_failure(mode, stage, blobs, oid)
        if failure:
            print(f"{name!r}: B: {failure}", file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
