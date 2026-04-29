import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import brief as brief_module

SCRIPT = Path(__file__).parent / "brief.py"

LOG_CONTENT = """\
# Log

---

## 2026-04-28 v0 shipped | brief.py done.

## 2026-04-27 setup | Scaffolded bridge.

## 2026-04-26 kickoff | Project started.

## 2026-04-25 old | Ancient entry.
"""


def test_extract_log_entries_returns_first_three():
    entries = brief_module.extract_log_entries(LOG_CONTENT)
    assert entries == [
        "2026-04-28 v0 shipped | brief.py done.",
        "2026-04-27 setup | Scaffolded bridge.",
        "2026-04-26 kickoff | Project started.",
    ]


def test_extract_log_entries_fewer_than_n():
    text = "## 2026-04-28 only entry\n"
    entries = brief_module.extract_log_entries(text)
    assert entries == ["2026-04-28 only entry"]


def test_extract_log_entries_empty():
    entries = brief_module.extract_log_entries("")
    assert entries == []


def test_resolve_bridge_path_constructs_from_name():
    p = brief_module.resolve_bridge_path("my-project")
    assert p.name == "my-project"
    assert "sandbox-projects" in str(p)


def test_resolve_bridge_path_absolute_bypasses_base(tmp_path):
    p = brief_module.resolve_bridge_path(str(tmp_path))
    assert p == tmp_path


def run(tmp_path, name, *flags):
    env = {**os.environ, "VAULT_BRIDGE_BASE": str(tmp_path)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), name, *flags],
        capture_output=True,
        text=True,
        env=env,
    )


def run_path(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
    )


def make_bridge(tmp_path, name, snapshot_content, log_content=None):
    bridge = tmp_path / name
    bridge.mkdir()
    (bridge / "context-snapshot.md").write_text(snapshot_content)
    if log_content is not None:
        (bridge / "log.md").write_text(log_content)
    return tmp_path, name


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

FULL_LOG = """\
## 2026-04-28 v0 shipped | brief.py done.

## 2026-04-27 setup | Scaffolded bridge.

## 2026-04-26 kickoff | Old entry.
"""


def test_all_sections_present(tmp_path):
    make_bridge(tmp_path, "proj", FULL_SNAPSHOT, FULL_LOG)
    result = run(tmp_path, "proj")
    assert result.returncode == 0
    assert "CURRENT GOAL" in result.stdout
    assert "Build something useful." in result.stdout
    assert "NEXT ACTION" in result.stdout
    assert "Write the tests." in result.stdout
    assert "OPEN QUESTIONS" in result.stdout
    assert "Is this enough?" in result.stdout
    assert "LOG" in result.stdout
    assert "v0 shipped" in result.stdout
    assert "setup" in result.stdout
    assert "kickoff" in result.stdout


def test_missing_heading_exits_nonzero(tmp_path):
    make_bridge(tmp_path, "proj", MISSING_HEADING, FULL_LOG)
    result = run(tmp_path, "proj")
    assert result.returncode != 0
    assert "## Open questions" in result.stderr


def test_missing_snapshot_exits_nonzero(tmp_path):
    (tmp_path / "proj").mkdir()
    result = run(tmp_path, "proj")
    assert result.returncode != 0
    assert "context-snapshot.md not found" in result.stderr


def test_missing_log_exits_nonzero(tmp_path):
    make_bridge(tmp_path, "proj", FULL_SNAPSHOT)
    result = run(tmp_path, "proj")
    assert result.returncode != 0
    assert "log.md not found" in result.stderr


def test_full_path_arg(tmp_path):
    bridge = tmp_path / "proj"
    bridge.mkdir()
    (bridge / "context-snapshot.md").write_text(FULL_SNAPSHOT)
    (bridge / "log.md").write_text(FULL_LOG)
    result = run_path(bridge)
    assert result.returncode == 0
    assert "CURRENT GOAL" in result.stdout
    assert "Build something useful." in result.stdout
    assert "LOG" in result.stdout


def test_missing_bridge_dir_exits_nonzero(tmp_path):
    result = run_path(tmp_path / "nonexistent")
    assert result.returncode != 0
    assert "bridge directory not found" in result.stderr


def test_markdown_output(tmp_path):
    make_bridge(tmp_path, "proj", FULL_SNAPSHOT, FULL_LOG)
    result = run(tmp_path, "proj", "--markdown")
    assert result.returncode == 0
    assert "# vault-brief: proj" in result.stdout
    assert "## Current goal" in result.stdout
    assert "## Next action" in result.stdout
    assert "## Open questions" in result.stdout
    assert "## Recent log" in result.stdout
    assert "- 2026-04-28" in result.stdout
    assert "v0 shipped" in result.stdout
    assert "CURRENT GOAL" not in result.stdout


def test_no_args_exits_nonzero():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Usage:" in result.stderr
    assert "/full/path/to/bridge" in result.stderr
    assert "[--markdown]" in result.stderr
