"""Replay merge-only and symlink-to-file type-change secrets reachable through other refs.

Read the workflow's single real gitleaks git command and replay its history-scan options.
Require both planted commits to be found while HEAD stays at their common base, proving
merge diffs, type-change coverage and traversal of other refs with --all.
"""

import os
import re
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


def clean_git_env():
    """Return a copy of os.environ with GIT_* stripped and global/system Git config disabled."""
    env = {
        key: value for key, value in os.environ.items()
        if not key.startswith("GIT_")
    }
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def log_opts_of(tokens):
    """Return --log-opts only for a real gitleaks git command after shell assignments."""
    first = 0
    for token in tokens:
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token):
            break
        first += 1
    command = tokens[first:]
    if len(command) < 2 or command[1] != "git":
        return None
    if command[0] != "gitleaks" and not command[0].endswith("/gitleaks"):
        return None
    args = command[2:]
    for pos, arg in enumerate(args):
        if arg.startswith("--log-opts="):
            return arg[len("--log-opts="):]
        if arg == "--log-opts" and pos + 1 < len(args):
            return args[pos + 1]
    return ""


def logical_lines(source):
    """Yield first physical line numbers and shell lines joined at unescaped backslashes."""
    pending = ""
    first = None
    for number, line in enumerate(source.splitlines(), 1):
        if first is None:
            first = number
        trailing = len(line) - len(line.rstrip("\\"))
        if trailing % 2:
            pending += line[:-1]
        else:
            yield first, pending + line
            pending = ""
            first = None
    if first is not None:
        yield first, pending


def shell_commands(line):
    """Split shell commands at unquoted, unescaped separators, then tokenize each one."""
    quote = None
    escaped = False
    start = 0
    for pos, char in enumerate(line):
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "#" and (pos == start or line[pos - 1].isspace()):
            line = line[:pos]
            break
        elif char in ";&|":
            tokens = shlex.split(line[start:pos], comments=True)
            if tokens:
                yield tokens
            start = pos + 1
    tokens = shlex.split(line[start:], comments=True)
    if tokens:
        yield tokens


def workflow_log_opts(workflow):
    """Extract exactly one real scan's nonempty --log-opts value from a workflow Path.

    Return (log_opts, None) on success, or (None, error) with its first physical line.
    """
    found = []
    for number, line in logical_lines(workflow.read_text(encoding="utf-8")):
        if "gitleaks" not in line:
            continue
        try:
            commands = list(shell_commands(line))
        except ValueError:
            continue
        for tokens in commands:
            value = log_opts_of(tokens)
            if value is not None:
                found.append((number, value))
    if len(found) != 1:
        return None, f"{workflow}: expected one gitleaks git step, found {len(found)}"
    number, value = found[0]
    if not value:
        return None, f"{workflow}:{number}: gitleaks git step sets no --log-opts"
    return value, None


def run_git(repo, env, *args, check=True):
    """Run git *args in repo with env, a fixed replay identity and signing off.

    Return the CompletedProcess; raise CalledProcessError on failure when check is true.
    """
    cmd = [
        "git",
        "-c", "user.name=Replay",
        "-c", "user.email=replay@example.invalid",
        "-c", "commit.gpgsign=false",
        *args,
    ]
    return subprocess.run(
        cmd, cwd=repo, env=env, check=check, capture_output=True, timeout=30,
    )


def require_merge_head(repo, env, result, expected):
    """Require the expected MERGE_HEAD; include merge stdout and stderr on failure."""
    head = run_git(repo, env, "rev-parse", "--verify", "MERGE_HEAD", check=False)
    if head.returncode != 0 or head.stdout.decode("ascii").strip() != expected:
        stdout = result.stdout.decode("utf-8", errors="replace").strip()
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"expected MERGE_HEAD {expected}; stdout: {stdout}; stderr: {stderr}")


def build_type_change(repo, env, base):
    """Commit a symlink, then replace it with a regular file containing a second token."""
    run_git(repo, env, "checkout", "-b", "type-change", base)
    note = repo / "type-change.md"
    note.symlink_to("notes.md")
    run_git(repo, env, "add", "type-change.md")
    run_git(repo, env, "commit", "-m", "symlink")
    note.unlink()
    prefix = "".join(("gh", "p_"))
    suffix = "".join(chr(ord("a") + (idx * 11) % 26) for idx in range(36))
    note.write_text(f"token = {prefix}{suffix}\n", encoding="utf-8")
    run_git(repo, env, "add", "type-change.md")
    run_git(repo, env, "commit", "-m", "replace symlink with regular file")
    return run_git(repo, env, "rev-parse", "HEAD").stdout.decode("ascii").strip()


def build_merge_fixture(repo, env):
    """Build merge-only and type-change secrets on other refs; leave HEAD at their base.

    Return (merge commit SHA, type-change commit SHA).
    """
    template = repo / "empty-template"
    template.mkdir()
    run_git(repo, env, "init", "--quiet", f"--template={template}")
    run_git(repo, env, "checkout", "-b", "main")
    note = repo / "notes.md"
    note.write_text("setting = baseline\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "base")
    base = run_git(repo, env, "rev-parse", "HEAD").stdout.decode("ascii").strip()
    run_git(repo, env, "checkout", "-b", "branch-a")
    note.write_text("setting = branch-a\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "branch-a")
    branch_sha = run_git(repo, env, "rev-parse", "HEAD").stdout.decode("ascii").strip()
    run_git(repo, env, "checkout", "main")
    note.write_text("setting = main-change\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "main")
    main_sha = run_git(repo, env, "rev-parse", "HEAD").stdout.decode("ascii").strip()
    result = run_git(repo, env, "merge", "--no-commit", "branch-a", check=False)
    require_merge_head(repo, env, result, branch_sha)
    prefix = "".join(("gh", "p_"))
    suffix = "".join(chr(ord("A") + (idx * 7) % 26) for idx in range(36))
    note.write_text(f"token = {prefix}{suffix}\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "merge conflict resolution")
    parents = run_git(repo, env, "rev-list", "--parents", "-n", "1", "HEAD")
    commits = parents.stdout.decode("ascii").split()
    if len(commits) != 3 or commits[1:] != [main_sha, branch_sha]:
        raise RuntimeError(f"unexpected resolution commit parents: {commits}")
    merge_sha = commits[0]
    type_sha = build_type_change(repo, env, base)
    run_git(repo, env, "checkout", "-b", "replay-base", base)
    return merge_sha, type_sha


def replay(gitleaks, log_opts):
    """Run gitleaks with and without log_opts against merge and type-change secrets on other refs.

    Return 0 when log_opts detects both planted commits (scan rc 1), or 1 otherwise.
    """
    env = clean_git_env()
    with tempfile.TemporaryDirectory(prefix="secret-scan-") as tmp:
        repo = Path(tmp)
        merge_sha, type_sha = build_merge_fixture(repo, env)
        with_opts = subprocess.run(
            [
                gitleaks, "git", "--verbose", "--redact", "--exit-code", "1",
                f"--log-opts={log_opts}", str(repo),
            ],
            env=env, capture_output=True, text=True, timeout=60,
        )
        without_opts = subprocess.run(
            [gitleaks, "git", "--redact", "--exit-code", "1", str(repo)],
            env=env, capture_output=True, text=True, timeout=60,
        )
    combined = f"{with_opts.stdout}\n{with_opts.stderr}"
    print(
        f"replay: --log-opts={log_opts!r} rc={with_opts.returncode}, "
        f"gitleaks default options rc={without_opts.returncode}"
    )
    if with_opts.returncode != 1 or any(sha not in combined for sha in (merge_sha, type_sha)):
        print(
            f"secret_scan: replay failed (rc={with_opts.returncode}, "
            f"expected merge commit {merge_sha} and type-change commit {type_sha})",
            file=sys.stderr,
        )
        return 1
    print(f"replay: merge commit {merge_sha} found; type-change commit {type_sha} found")
    return 0


def main(argv):
    """Parse argv=[prog, gitleaks, workflow] and replay the workflow gitleaks history scan.

    Return exit status 0 on detection, 1 on workflow or replay failure, or 2 on bad usage.
    """
    if len(argv) != 3:
        print("usage: secret_scan.py <gitleaks> <workflow>", file=sys.stderr)
        return 2
    log_opts, error = workflow_log_opts(Path(argv[2]))
    if error:
        print(f"secret_scan: {error}", file=sys.stderr)
        return 1
    try:
        return replay(argv[1], log_opts)
    except (OSError, RuntimeError, subprocess.SubprocessError) as failure:
        print(f"secret_scan: {failure}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
