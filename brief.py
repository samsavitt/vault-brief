#!/usr/bin/env python3
import re
import sys
from pathlib import Path

HEADINGS = ["## Current goal", "## Next action", "## Open questions"]


def extract_section(text, heading):
    pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python brief.py <path-to-bridge-folder>", file=sys.stderr)
        sys.exit(1)

    bridge_path = Path(sys.argv[1]).expanduser()
    snapshot = bridge_path / "context-snapshot.md"

    if not snapshot.exists():
        print(f"Error: context-snapshot.md not found in {bridge_path}", file=sys.stderr)
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


if __name__ == "__main__":
    main()
