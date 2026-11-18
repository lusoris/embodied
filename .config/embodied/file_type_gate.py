# Enforce the root .gitignore allow-list and UTF-8 text-only staged blob boundary:
# no media or data exports in the repository, even after a forced add or rename.

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def list_staged_entries(git, top, env):
    """List staged index entries in top with git as (path, mode, oid, stage) tuples.

    Return (entries, None) on success, or (None, error) if git fails or the index is empty.
    """
    try:
        result = subprocess.run(
            [git, "ls-files", "-s", "-z"],
            cwd=top, env=env, capture_output=True, timeout=30,
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


def list_ignored_paths(git, top, env, exclude):
    """List tracked paths in top matching the staged policy in exclude using git.

    Return (ignored_set, None) on success, or (None, error) if git ls-files -i fails.
    """
    try:
        result = subprocess.run(
            [git, "ls-files", "-c", "-i", "-z", f"--exclude-from={exclude}"],
            cwd=top, env=env, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return None, f"git ls-files -i failed: {error}"
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        return None, f"git ls-files -i failed (exit {result.returncode}): {detail}"
    ignored = {os.fsdecode(raw) for raw in result.stdout.split(b"\0") if raw}
    return ignored, None


def read_staged_blobs(git, top, oids, env):
    """Read raw blob bytes for oids in top via git --no-replace-objects cat-file --batch.

    Return ({oid: bytes}, None) on success, or (None, error) on git or header/blob failure.
    """
    if not oids:
        return {}, None
    query = "".join(f"{oid}\n" for oid in oids).encode("ascii")
    try:
        result = subprocess.run(
            [git, "--no-replace-objects", "cat-file", "--batch"],
            cwd=top, env=env, input=query, capture_output=True, timeout=30,
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


def checkout_context(git):
    """Resolve this checkout with a scrubbed Git environment; reject inherited redirections.

    Return (top, env, None), or (None, None, reason) on resolution or isolation failure.
    """
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") or key == "GIT_INDEX_FILE"}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    cwd = Path.cwd()
    try:
        result = subprocess.run(
            [git, "rev-parse", "--absolute-git-dir", "--show-toplevel"],
            cwd=cwd, env=env, capture_output=True, timeout=30,
        )
        if result.returncode != 0:
            return None, None, f"git rev-parse failed: {os.fsdecode(result.stderr).strip()}"
        git_dir, top = (Path(os.fsdecode(line)).resolve()
                        for line in result.stdout.splitlines())
        for key, expected in (("GIT_DIR", git_dir), ("GIT_WORK_TREE", top)):
            if key in os.environ and (cwd / os.environ[key]).resolve() != expected:
                return None, None, f"{key} resolves outside this checkout: expected {expected}"
        if "GIT_INDEX_FILE" in env:
            index = (cwd / env["GIT_INDEX_FILE"]).resolve()
            if not index.is_relative_to(git_dir) or index == git_dir:
                reason = "GIT_INDEX_FILE must resolve inside this checkout's git directory"
                return None, None, reason
            env["GIT_INDEX_FILE"] = str(index)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return None, None, f"checkout resolution failed: {error}"
    return top, env, None


def staged_admission(git, top, env):
    """Read staged policy and compare index snapshots around the ignored-path lookup.

    Return (entries, ignored, None), or (None, None, reason) on failure.
    """
    entries, error = list_staged_entries(git, top, env)
    if error:
        return None, None, error
    policy = [entry for entry in entries if entry[0] == ".gitignore"]
    if len(policy) != 1 or policy[0][1] != "100644" or policy[0][3] != "0":
        return None, None, "staged .gitignore must exist at stage 0 with mode 100644"
    oid = policy[0][2]
    blobs, error = read_staged_blobs(git, top, [oid], env)
    if error:
        return None, None, error
    with tempfile.TemporaryDirectory(prefix="file-type-policy-") as tmp:
        exclude = Path(tmp) / ".gitignore"
        exclude.write_bytes(blobs[oid])
        ignored, error = list_ignored_paths(git, top, env, exclude)
    after, snapshot_error = list_staged_entries(git, top, env)
    if snapshot_error or entries != after:
        return None, None, "index changed while the gate ran; rerun"
    if error:
        return None, None, error
    return entries, ignored, None


def check_entries(git, top, env, entries, ignored):
    """Report path failures, then read and check content only for admitted entries."""
    admitted = []
    failed = False
    for entry in entries:
        name = entry[0]
        if name in ignored:
            msg = "path ignored by the root .gitignore allow-list"
            print(f"{name!r}: A: {msg}", file=sys.stderr)
            failed = True
        else:
            admitted.append(entry)
    oids = [oid for _, mode, oid, stage in admitted
            if stage == "0" and mode in ("100644", "100755")]
    blobs, error = read_staged_blobs(git, top, oids, env)
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    for name, mode, oid, stage in admitted:
        failure = blob_text_failure(mode, stage, blobs, oid)
        if failure:
            print(f"{name!r}: B: {failure}", file=sys.stderr)
            failed = True
    return int(failed)


def main():
    """Check this checkout's staged root policy and admitted UTF-8 text blobs.

    Print any errors or violations to stderr and return 0 on pass or 1 on failure.
    """
    git = shutil.which("git")
    if git is None:
        print("file_type_gate: git not found on PATH", file=sys.stderr)
        return 1
    top, env, error = checkout_context(git)
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    try:
        entries, ignored, error = staged_admission(git, top, env)
    except (OSError, subprocess.SubprocessError) as failure:
        error = f"staged admission failed: {failure}"
    if error:
        print(f"file_type_gate: {error}", file=sys.stderr)
        return 1
    return check_entries(git, top, env, entries, ignored)


if __name__ == "__main__":
    raise SystemExit(main())
