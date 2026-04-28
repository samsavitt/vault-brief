import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "brief.py"


def run(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
    )


def make_snapshot(tmp_path, content):
    f = tmp_path / "context-snapshot.md"
    f.write_text(content)
    return tmp_path


FULL_SNAPSHOT = """\
## Current goal
Build something useful.

## Next action
Write the tests.

## Open questions
- Is this enough?
- Should we add more?
"""

MISSING_HEADING = """\
## Current goal
Build something useful.

## Next action
Write the tests.
"""


def test_all_headings_present(tmp_path):
    make_snapshot(tmp_path, FULL_SNAPSHOT)
    result = run(tmp_path)
    assert result.returncode == 0
    assert "CURRENT GOAL" in result.stdout
    assert "Build something useful." in result.stdout
    assert "NEXT ACTION" in result.stdout
    assert "Write the tests." in result.stdout
    assert "OPEN QUESTIONS" in result.stdout
    assert "Is this enough?" in result.stdout


def test_missing_heading_exits_nonzero(tmp_path):
    make_snapshot(tmp_path, MISSING_HEADING)
    result = run(tmp_path)
    assert result.returncode != 0
    assert "## Open questions" in result.stderr


def test_missing_snapshot_exits_nonzero(tmp_path):
    result = run(tmp_path)
    assert result.returncode != 0
    assert "context-snapshot.md not found" in result.stderr


def test_no_args_exits_nonzero():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Usage:" in result.stderr
