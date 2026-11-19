"""Isolated Git fixture repositories shared by the gate tests in this directory."""

import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]


def isolated_repository(test, prefix):
    """Create an empty Git repository under ROOT/.workingdir that test cleans up.

    Return (repo, env): the repository path, and an environment with every GIT_ variable
    removed and global and system Git configuration ignored, for every later git call.
    """
    state = ROOT / ".workingdir"
    state.mkdir(exist_ok=True)
    fixture = tempfile.TemporaryDirectory(prefix=prefix, dir=state)
    test.addCleanup(fixture.cleanup)
    repo = Path(fixture.name)
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    template = repo / "empty-template"
    template.mkdir()
    subprocess.run(
        ["git", "init", "--quiet", f"--template={template}"], cwd=repo, env=env,
        check=True, capture_output=True, timeout=10,
    )
    return repo, env
