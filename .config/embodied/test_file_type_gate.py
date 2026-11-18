"""Replay the repository's file admission and text boundary in isolated Git fixtures."""

import contextlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import file_type_gate as gate


ROOT = Path(__file__).resolve().parents[2]
GATE = Path(".config/embodied/file_type_gate.py")


class FileTypeGateTests(unittest.TestCase):
    def setUp(self):
        """Create an isolated temporary Git fixture with root .gitignore and the gate script."""
        state = ROOT / ".workingdir"
        state.mkdir(exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix="file-type-", dir=state)
        self.addCleanup(self.fixture.cleanup)
        self.repo = Path(self.fixture.name)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env["GIT_CONFIG_GLOBAL"] = os.devnull
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        template = self.repo / "empty-template"
        template.mkdir()
        self.git("init", "--quiet", f"--template={template}")
        shutil.copyfile(ROOT / ".gitignore", self.repo / ".gitignore")
        self.git("add", "--force", "--", ".gitignore")
        (self.repo / GATE).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / GATE, self.repo / GATE)

    def git(self, *args):
        """Run git with *args in the fixture repository and return stdout bytes."""
        return subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, check=True,
            capture_output=True, timeout=10,
        ).stdout

    def run_gate(self, env=None):
        """Run the copied gate in the fixture repo (fixture env unless env is given); return it."""
        return subprocess.run(
            [sys.executable, "-I", str(GATE)],
            cwd=self.repo,
            env=self.env if env is None else env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=30,
        )

    def check_file(self, name, content):
        """Write content bytes to name, force-stage it, and return the run_gate result."""
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        self.git("add", "--force", "--", name)
        return self.run_gate()

    def test_forced_add_fails_allow_list(self):
        """Verify force-staged disallowed paths fail with exit 1 and an A: allow-list error."""
        for name in ("photo.JPG", "export.json"):
            with self.subTest(path=name):
                result = self.check_file(name, b"plain text\n")
                self.assertEqual(result.returncode, 1)
                self.assertIn(f"{name!r}: A:", result.stderr.decode())

    def test_renamed_binary_fails_text_check(self):
        """Verify binary or non-UTF-8 content staged as .md fails with exit 1 and a B: error."""
        for content in (b"\x89PNG\r\n\x1a\n\x00", b"text\x00", b"\xff"):
            with self.subTest(content=content):
                result = self.check_file("scan.md", content)
                self.assertEqual(result.returncode, 1)
                self.assertIn("'scan.md': B:", result.stderr.decode())
                self.assertNotIn("'scan.md': A:", result.stderr.decode())

    def test_plain_markdown_passes(self):
        """Verify staged UTF-8 Markdown files (with spaces) pass with exit 0 and empty stderr."""
        for name in ("notes.md", "notes with spaces.md"):
            with self.subTest(path=name):
                result = self.check_file(name, "Plain UTF-8 text: café.\n".encode())
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, b"")

    @unittest.skipIf(os.name == "nt", "Windows NTFS forbids newline characters in filenames")
    def test_newline_filename_passes(self):
        """Verify a staged UTF-8 Markdown filename containing a newline passes with exit 0."""
        result = self.check_file("notes\nline.md", "Plain UTF-8 text: café.\n".encode())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")

    def test_removing_default_deny_admits_forced_files(self):
        """Verify removing the '*' rule from .gitignore admits forced files with exit 0."""
        ignore = self.repo / ".gitignore"
        rules = ignore.read_text(encoding="utf-8").splitlines(keepends=True)
        self.assertEqual(sum(line.strip() == "*" for line in rules), 1)
        ignore.write_text("".join(line for line in rules if line.strip() != "*"),
                          encoding="utf-8")
        self.git("add", "--force", "--", ".gitignore")
        for name in ("photo.JPG", "export.json"):
            with self.subTest(path=name):
                result = self.check_file(name, b"plain text\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(b": A:", result.stderr)

    def test_nested_gitignore_cannot_widen_root_allow_list(self):
        """Verify a nested .gitignore cannot widen root rules; expect exit 1 and an A: error."""
        docs = self.repo / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / ".gitignore").write_text("!*.csv\n!.gitignore\n", encoding="utf-8")
        (docs / "data.csv").write_text("col1,col2\n1,2\n", encoding="utf-8")
        self.git("add", "--force", "--", "docs/.gitignore", "docs/data.csv")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        stderr = result.stderr.decode("utf-8", errors="replace")
        self.assertIn(
            "'docs/data.csv': A: path ignored by the root .gitignore allow-list",
            stderr,
        )

    def test_staged_text_with_unstaged_binary_working_copy_passes(self):
        """Verify staged UTF-8 text passes with exit 0 despite an unstaged binary working copy."""
        (self.repo / "notes.md").write_bytes(b"Plain UTF-8 text.\n")
        self.git("add", "--force", "--", "notes.md")
        (self.repo / "notes.md").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")

    def test_staged_binary_with_plain_working_copy_fails_text_check(self):
        """Verify staged binary fails with exit 1 and B: NUL error despite a plain worktree."""
        (self.repo / "scan.md").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
        self.git("add", "--force", "--", "scan.md")
        (self.repo / "scan.md").write_bytes(b"Plain UTF-8 text.\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        stderr = result.stderr.decode("utf-8", errors="replace")
        self.assertIn("'scan.md': B: NUL byte in staged blob", stderr)

    def test_git_failure_exits_nonzero_with_reason(self):
        """Verify a nonexistent inherited Git directory is rejected with a reason."""
        (self.repo / "notes.md").write_bytes(b"Plain UTF-8 text.\n")
        self.git("add", "--force", "--", "notes.md")
        broken_env = dict(self.env)
        broken_env["GIT_DIR"] = str(self.repo / "missing-git-dir")
        result = self.run_gate(env=broken_env)
        self.assertEqual(result.returncode, 1)
        self.assertIn("GIT_DIR", result.stderr.decode("utf-8", errors="replace"))

    def test_empty_index_exits_nonzero(self):
        """Verify an empty index exits 1 and reports 'empty index' on stderr."""
        self.git("rm", "--cached", "--", ".gitignore")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("empty index", result.stderr.decode("utf-8", errors="replace"))

    def test_unstaged_policy_cannot_admit_media(self):
        """Reject force-staged media despite an unstaged root policy exception."""
        with (self.repo / ".gitignore").open("a", encoding="utf-8") as policy:
            policy.write("!*.jpg\n")
        result = self.check_file("photo.jpg", b"plain text\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"'photo.jpg': A:", result.stderr)

    def test_foreign_git_directory_is_rejected(self):
        """Reject an inherited GIT_DIR naming a second fixture checkout."""
        sibling = self.repo / "sibling"
        sibling.mkdir()
        subprocess.run(
            ["git", "init", "--quiet", f"--template={self.repo / 'empty-template'}", str(sibling)],
            env=self.env, check=True, capture_output=True, timeout=10,
        )
        result = self.run_gate(env={**self.env, "GIT_DIR": str(sibling / ".git")})
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"GIT_DIR", result.stderr)

    def test_foreign_work_tree_is_rejected(self):
        """Reject a GIT_WORK_TREE that redirects paths away from this checkout."""
        result = self.run_gate(env={**self.env, "GIT_WORK_TREE": str(self.repo / "other")})
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"GIT_WORK_TREE", result.stderr)

    def test_external_index_is_rejected(self):
        """Reject an inherited index outside this checkout's Git directory."""
        index = self.repo / "outside-index"
        shutil.copyfile(self.repo / ".git/index", index)
        result = self.run_gate(env={**self.env, "GIT_INDEX_FILE": str(index)})
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"GIT_INDEX_FILE", result.stderr)

    def test_hook_index_inside_git_directory_passes(self):
        """Allow a hook's temporary index inside this checkout's Git directory."""
        index = self.repo / ".git/hook-index"
        shutil.copyfile(self.repo / ".git/index", index)
        result = self.run_gate(env={**self.env, "GIT_INDEX_FILE": str(index)})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_replacement_ref_cannot_hide_binary_blob(self):
        """Judge original staged bytes even if a replacement ref supplies text."""
        (self.repo / "scan.md").write_bytes(b"binary\0")
        self.git("add", "--force", "--", "scan.md")
        binary = self.git("rev-parse", ":scan.md").decode().strip()
        (self.repo / "safe.md").write_bytes(b"plain text\n")
        safe = self.git("hash-object", "-w", "safe.md").decode().strip()
        self.git("replace", binary, safe)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"'scan.md': B: NUL", result.stderr)

    def test_index_change_fails_closed(self):
        """Reject an index change between the admission list and ignored-path lookup."""
        original = gate.list_ignored_paths

        def change_index(*args):
            """Stage another file after the first snapshot, then run the real lookup."""
            (self.repo / "late.md").write_text("late\n", encoding="utf-8")
            self.git("add", "--force", "--", "late.md")
            return original(*args)

        errors = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(gate.Path, "cwd", return_value=self.repo), \
                mock.patch.object(gate, "list_ignored_paths", side_effect=change_index), \
                contextlib.redirect_stderr(errors):
            self.assertEqual(gate.main(), 1)
        self.assertIn("index changed while the gate ran; rerun", errors.getvalue())

    def test_rejected_path_is_not_read_as_blob(self):
        """Report admission failures first and skip content reads for rejected paths."""
        (self.repo / "photo.jpg").write_bytes(b"binary\0")
        self.git("add", "--force", "--", "photo.jpg")
        oid = self.git("rev-parse", ":photo.jpg").decode().strip()
        errors = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(gate.Path, "cwd", return_value=self.repo), \
                mock.patch.object(gate, "read_staged_blobs",
                                  wraps=gate.read_staged_blobs) as read, \
                contextlib.redirect_stderr(errors):
            self.assertEqual(gate.main(), 1)
        self.assertIn("'photo.jpg': A:", errors.getvalue())
        self.assertNotIn("'photo.jpg': B:", errors.getvalue())
        self.assertTrue(all(oid not in call.args[2] for call in read.call_args_list))

    def test_missing_staged_policy_fails_closed(self):
        """Require a stage-zero root policy even when a working-tree policy exists."""
        self.git("rm", "--cached", "--", ".gitignore")
        result = self.check_file("notes.md", b"plain text\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"staged .gitignore", result.stderr)

    def test_executable_staged_policy_fails_closed(self):
        """Require mode 100644 for the staged root policy."""
        self.git("update-index", "--chmod=+x", ".gitignore")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"100644", result.stderr)


if __name__ == "__main__":
    unittest.main()
