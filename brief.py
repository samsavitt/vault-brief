#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

BRIDGE_BASE = Path(
    os.environ.get(
        "VAULT_BRIDGE_BASE",
        "~/Documents/vaults/jarvis-one/projects/sandbox-projects",
    )
).expanduser()


def make_bridge_path(name):
    return BRIDGE_BASE / name


HEADINGS = ["## Current goal", "## Next action", "## Open questions"]


def extract_log_entries(text, n=3):
    entries = []
    for line in text.splitlines():
        if line.startswith("## "):
            entries.append(line[3:].strip())
            if len(entries) == n:
                break
    return entries


def extract_section(text, heading):
    pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python brief.py <project-name>", file=sys.stderr)
        sys.exit(1)

    bridge_path = make_bridge_path(sys.argv[1])
    snapshot = bridge_path / "context-snapshot.md"
    log_file = bridge_path / "log.md"

    if not snapshot.exists():
        print(f"Error: context-snapshot.md not found in {bridge_path}", file=sys.stderr)
        sys.exit(1)

    if not log_file.exists():
        print(f"Error: log.md not found in {bridge_path}", file=sys.stderr)
        sys.exit(1)

    text = snapshot.read_text()

    missing = []
    sections = {}
    for heading in HEADINGS:
        content = extract_section(text, heading)
        if content is None:
            missing.append(heading)
        else:
            sections[heading] = content

    if missing:
        for h in missing:
            print(f"Error: required heading not found: {h}", file=sys.stderr)
        sys.exit(1)

    for heading, content in sections.items():
        label = heading.lstrip("# ").upper()
        print(label)
        print(content)
        print()

    log_text = log_file.read_text()
    entries = extract_log_entries(log_text)
    print("LOG (LAST 3)")
    for entry in entries:
        print(entry)
    print()


if __name__ == "__main__":
    main()
