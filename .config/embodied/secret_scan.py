"""Replay a merge-introduced secret against the workflow's own gitleaks history-scan options.

The workflow runs gitleaks directly; this replay reads that step's --log-opts value from the
workflow file, so the options it proves are the options CI scans with. It fails unless the
workflow holds exactly one gitleaks git step and that step's options find a secret that only
a merge commit's conflict resolution introduced.
"""

import os
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
    """Return the --log-opts value of a `<path>/gitleaks git ...` command, or None."""
    for idx in range(len(tokens) - 1):
        program = tokens[idx]
        if not (program == "gitleaks" or program.endswith("/gitleaks")):
            continue
        if tokens[idx + 1] != "git":
            continue
        args = tokens[idx + 2:]
        for pos, arg in enumerate(args):
            if arg.startswith("--log-opts="):
                return arg[len("--log-opts="):]
            if arg == "--log-opts" and pos + 1 < len(args):
                return args[pos + 1]
        return ""
    return None


def workflow_log_opts(workflow):
    """Extract the gitleaks git --log-opts value from the workflow Path.

    Return (log_opts, None) when exactly one non-empty option is found, or (None, error).
    """
    found = []
    for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
        if "gitleaks" not in line:
            continue
        try:
            tokens = shlex.split(line, comments=True)
        except ValueError:
            continue
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


def build_merge_fixture(repo, env):
    """Initialize a Git fixture in repo with env and commit a merge-only secret token.

    Return the resulting merge commit SHA string.
    """
    template = repo / "empty-template"
    template.mkdir()
    run_git(repo, env, "init", "--quiet", f"--template={template}")
    run_git(repo, env, "checkout", "-b", "main")
    note = repo / "notes.md"
    note.write_text("setting = baseline\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "base")
    run_git(repo, env, "checkout", "-b", "branch-a")
    note.write_text("setting = branch-a\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "branch-a")
    run_git(repo, env, "checkout", "main")
    note.write_text("setting = main-change\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "main")
    run_git(repo, env, "merge", "--no-commit", "branch-a", check=False)
    prefix = "".join(("gh", "p_"))
    suffix = "".join(chr(ord("A") + (idx * 7) % 26) for idx in range(36))
    note.write_text(f"token = {prefix}{suffix}\n", encoding="utf-8")
    run_git(repo, env, "add", "notes.md")
    run_git(repo, env, "commit", "-m", "merge conflict resolution")
    head = run_git(repo, env, "rev-parse", "HEAD")
    return head.stdout.decode("ascii").strip()


def replay(gitleaks, log_opts):
    """Run gitleaks with and without log_opts against a temporary merge-secret fixture.

    Return exit status 0 when log_opts detects the merge commit (rc 1), or 1 otherwise.
    """
    env = clean_git_env()
    with tempfile.TemporaryDirectory(prefix="secret-scan-") as tmp:
        repo = Path(tmp)
        merge_sha = build_merge_fixture(repo, env)
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
    if with_opts.returncode != 1 or merge_sha not in combined:
        print(
            f"secret_scan: replay failed (rc={with_opts.returncode}, "
            f"expected merge commit {merge_sha})",
            file=sys.stderr,
        )
        return 1
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
    return replay(argv[1], log_opts)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
