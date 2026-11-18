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

    def check_file(self, name, content):
        (self.repo / name).write_bytes(content)
        self.git("add", "--force", "--", name)
        return subprocess.run(
            [sys.executable, "-I", str(GATE)], cwd=self.repo, env=self.env,
            input=self.git("ls-files", "-z"), capture_output=True, timeout=30,
        )

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
        for name in ("notes.md", "notes with spaces.md", "notes\nline.md"):
            with self.subTest(path=name):
                result = self.check_file(name, "Plain UTF-8 text: café.\n".encode())
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


if __name__ == "__main__":
    unittest.main()
