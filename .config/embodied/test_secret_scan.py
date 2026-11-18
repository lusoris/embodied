"""Check scan commands, merge/other-ref/type-change fixtures and the application-code claim."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import secret_scan


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/docs.yml"
OPTIONS = "--full-history --all --diff-filter=uxdb -m"


class WorkflowLogOptsTests(unittest.TestCase):
    def setUp(self):
        """Create temporary workflow files inside private repository state."""
        state = ROOT / ".workingdir"
        state.mkdir(exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix="workflow-", dir=state)
        self.addCleanup(self.fixture.cleanup)
        self.workflow = Path(self.fixture.name) / "docs.yml"

    def parse(self, source):
        """Write source as a temporary workflow and return its scan options and error."""
        self.workflow.write_text(source, encoding="utf-8")
        return secret_scan.workflow_log_opts(self.workflow)

    def test_real_workflow_has_one_scan(self):
        """Extract exactly the options declared by the real documentation workflow."""
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(f'--log-opts="{OPTIONS}"', source)
        self.assertEqual(self.parse(source), (OPTIONS, None))

    def test_echo_does_not_add_scan(self):
        """Ignore scan-shaped words passed as arguments to echo."""
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertEqual(self.parse(source + "\necho gitleaks git --log-opts=x\n"),
                         (OPTIONS, None))

    def test_backslash_wrapped_scan(self):
        """Join a shell continuation before extracting a real scan's options."""
        source = f'gitleaks git \\\n  --log-opts="{OPTIONS}" .\n'
        self.assertEqual(self.parse(source), (OPTIONS, None))

    def test_wrapped_error_uses_first_line(self):
        """Report the first physical line of a scan missing its log options."""
        sources = (("\ngitleaks \\\n git .\n", 2), ("\\\n" + "gitleaks git .\n", 1))
        for source, number in sources:
            with self.subTest(source=source):
                value, error = self.parse(source)
                self.assertIsNone(value)
                self.assertIn(f":{number}: gitleaks git step sets no --log-opts", error)

    def test_replay_command_is_not_scan(self):
        """Reject a workflow containing only the Python replay invocation."""
        value, error = self.parse(
            'python3 -I .config/embodied/secret_scan.py "/tmp/gitleaks" docs.yml\n'
        )
        self.assertIsNone(value)
        self.assertIn("found 0", error)

    def test_two_real_scans_are_rejected(self):
        """Reject ambiguous scan options across two real commands."""
        value, error = self.parse(
            "gitleaks git --log-opts=x\n/opt/gitleaks git --log-opts=y\n"
        )
        self.assertIsNone(value)
        self.assertIn("found 2", error)

    def test_shell_separators_and_assignments(self):
        """Recognize command boundaries and skip leading shell assignments."""
        for separator in (";", "&&", "||", "|", "&"):
            with self.subTest(separator=separator):
                source = f'echo ready {separator} LABEL=scan /opt/gitleaks git --log-opts=x'
                self.assertEqual(self.parse(source), ("x", None))
                value, error = self.parse(
                    f'gitleaks git --log-opts=x {separator} gitleaks git --log-opts=y'
                )
                self.assertIsNone(value)
                self.assertIn("found 2", error)

    def test_quoted_or_escaped_separator_is_not_command_boundary(self):
        """Ignore scan-shaped echo arguments after quoted or escaped separators."""
        for separator in ('";"', "'&&'", r"\|", '"&"'):
            with self.subTest(separator=separator):
                value, error = self.parse(f'echo {separator} gitleaks git --log-opts=x')
                self.assertIsNone(value)
                self.assertIn("found 0", error)

    def test_escaped_backslash_does_not_join(self):
        """Keep a line ending in two backslashes separate from the next command."""
        source = "echo ignored " + "\\" * 2 + "\ngitleaks git --log-opts=x\n"
        self.assertEqual(self.parse(source), ("x", None))


class MergeFixtureTests(unittest.TestCase):
    def setUp(self):
        """Create an isolated replay repository without requiring gitleaks."""
        state = ROOT / ".workingdir"
        state.mkdir(exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix="merge-", dir=state)
        self.addCleanup(self.fixture.cleanup)
        self.repo = Path(self.fixture.name)
        self.env = secret_scan.clean_git_env()

    def test_merge_and_type_change_live_only_on_other_refs(self):
        """Prove both planted commits are outside HEAD and the type-change has status T."""
        merge_sha, type_sha = secret_scan.build_merge_fixture(self.repo, self.env)
        current = secret_scan.run_git(self.repo, self.env, "rev-list", "HEAD").stdout.split()
        all_refs = secret_scan.run_git(self.repo, self.env, "rev-list", "--all").stdout.split()
        for sha in (merge_sha, type_sha):
            self.assertNotIn(sha.encode(), current)
            self.assertIn(sha.encode(), all_refs)
        parents = secret_scan.run_git(
            self.repo, self.env, "rev-list", "--parents", "-n", "1", merge_sha
        ).stdout.split()
        self.assertEqual(len(parents), 3)
        change = secret_scan.run_git(
            self.repo, self.env, "diff-tree", "--no-commit-id", "--name-status", "-r", type_sha
        ).stdout
        self.assertIn(b"T\t", change)

    def test_missing_merge_head_reports_merge_output(self):
        """Reject a failed merge without MERGE_HEAD and preserve its diagnostic output."""
        original = secret_scan.run_git

        def fail_merge(repo, env, *args, **kwargs):
            """Simulate a merge failure that never starts a merge."""
            if args[0] == "merge":
                return subprocess.CompletedProcess(args, 128, b"planted stdout", b"planted stderr")
            return original(repo, env, *args, **kwargs)

        with mock.patch.object(secret_scan, "run_git", side_effect=fail_merge):
            with self.assertRaisesRegex(RuntimeError, "planted stdout.*planted stderr"):
                secret_scan.build_merge_fixture(self.repo, self.env)

    def test_wrong_merge_head_is_rejected(self):
        """Reject MERGE_HEAD when it differs from branch-a's expected commit."""
        original = secret_scan.run_git

        def wrong_merge_head(repo, env, *args, **kwargs):
            """Run a real merge but replace MERGE_HEAD with its first parent's SHA."""
            result = original(repo, env, *args, **kwargs)
            if args[0] == "merge":
                head = original(repo, env, "rev-parse", "HEAD").stdout
                (repo / ".git/MERGE_HEAD").write_bytes(head)
            return result

        with mock.patch.object(secret_scan, "run_git", side_effect=wrong_merge_head):
            with self.assertRaisesRegex(RuntimeError, "MERGE_HEAD"):
                secret_scan.build_merge_fixture(self.repo, self.env)

    def test_wrong_resolution_parents_are_rejected(self):
        """Reject a resolution commit unless it has exactly the two expected parents."""
        original = secret_scan.run_git

        def wrong_parents(repo, env, *args, **kwargs):
            """Replace the parent read-back with a planted single-parent result."""
            if args[:2] == ("rev-list", "--parents"):
                return subprocess.CompletedProcess(args, 0, b"head parent\n", b"")
            return original(repo, env, *args, **kwargs)

        with mock.patch.object(secret_scan, "run_git", side_effect=wrong_parents):
            with self.assertRaisesRegex(RuntimeError, "parents"):
                secret_scan.build_merge_fixture(self.repo, self.env)


class DocumentationScopeTests(unittest.TestCase):
    def test_application_code_claim_is_scoped(self):
        """Keep the architecture claim specific to application code and acknowledge checks."""
        concept = " ".join((ROOT / "docs/MASTER_CONCEPT.md").read_text(encoding="utf-8").split())
        self.assertFalse("no code exists in this repository yet" in concept)
        self.assertIn("no application code exists in this repository yet", concept)
        self.assertIn("documentation and the checks that guard it", concept)


if __name__ == "__main__":
    unittest.main()
