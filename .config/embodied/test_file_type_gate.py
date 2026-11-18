"""Replay the repository's file admission and text boundary in isolated Git fixtures."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
GATE = Path(".config/embodied/file_type_gate.py")


class FileTypeGateTests(unittest.TestCase):
    def setUp(self):
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
        (self.repo / GATE).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / GATE, self.repo / GATE)

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, check=True,
            capture_output=True, timeout=10,
        ).stdout

    def run_gate(self, env=None, stdin_data=b""):
        return subprocess.run(
            [sys.executable, "-I", str(GATE)],
            cwd=self.repo,
            env=self.env if env is None else env,
            input=stdin_data,
            capture_output=True,
            timeout=30,
        )

    def check_file(self, name, content):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        self.git("add", "--force", "--", name)
        return self.run_gate()

    def test_forced_add_fails_allow_list(self):
        for name in ("photo.JPG", "export.json"):
            with self.subTest(path=name):
                result = self.check_file(name, b"plain text\n")
                self.assertEqual(result.returncode, 1)
                self.assertIn(f"{name!r}: A:", result.stderr.decode())

    def test_renamed_binary_fails_text_check(self):
        for content in (b"\x89PNG\r\n\x1a\n\x00", b"text\x00", b"\xff"):
            with self.subTest(content=content):
                result = self.check_file("scan.md", content)
                self.assertEqual(result.returncode, 1)
                self.assertIn("'scan.md': B:", result.stderr.decode())
                self.assertNotIn("'scan.md': A:", result.stderr.decode())

    def test_plain_markdown_passes(self):
        for name in ("notes.md", "notes with spaces.md"):
            with self.subTest(path=name):
                result = self.check_file(name, "Plain UTF-8 text: café.\n".encode())
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, b"")

    @unittest.skipIf(os.name == "nt", "Windows NTFS forbids newline characters in filenames")
    def test_newline_filename_passes(self):
        result = self.check_file("notes\nline.md", "Plain UTF-8 text: café.\n".encode())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")

    def test_removing_default_deny_admits_forced_files(self):
        ignore = self.repo / ".gitignore"
        rules = ignore.read_text(encoding="utf-8").splitlines(keepends=True)
        self.assertEqual(sum(line.strip() == "*" for line in rules), 1)
        ignore.write_text("".join(line for line in rules if line.strip() != "*"),
                          encoding="utf-8")
        for name in ("photo.JPG", "export.json"):
            with self.subTest(path=name):
                result = self.check_file(name, b"plain text\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(b": A:", result.stderr)

    def test_a_nested_gitignore_cannot_widen_root_allow_list(self):
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

    def test_b_staged_text_with_unstaged_binary_working_copy_passes(self):
        (self.repo / "notes.md").write_bytes(b"Plain UTF-8 text.\n")
        self.git("add", "--force", "--", "notes.md")
        (self.repo / "notes.md").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
        result = self.run_gate(stdin_data=b"notes.md\0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")

    def test_c_staged_binary_with_plain_working_copy_fails_b(self):
        (self.repo / "scan.md").write_bytes(b"\x89PNG\r\n\x1a\n\x00")
        self.git("add", "--force", "--", "scan.md")
        (self.repo / "scan.md").write_bytes(b"Plain UTF-8 text.\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        stderr = result.stderr.decode("utf-8", errors="replace")
        self.assertIn("'scan.md': B: NUL byte in staged blob", stderr)

    def test_d_git_failure_exits_nonzero_with_reason(self):
        (self.repo / "notes.md").write_bytes(b"Plain UTF-8 text.\n")
        self.git("add", "--force", "--", "notes.md")
        broken_env = dict(self.env)
        broken_env["GIT_DIR"] = str(self.repo / "missing-git-dir")
        result = self.run_gate(env=broken_env)
        self.assertEqual(result.returncode, 1)
        self.assertIn("git ls-files -s failed", result.stderr.decode("utf-8", errors="replace"))

    def test_e_empty_index_exits_nonzero(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("empty index", result.stderr.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    unittest.main()
