#!/usr/bin/env python3
import html
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


def resolve_bridge_path(arg):
    p = Path(arg).expanduser()
    if p.is_absolute():
        return p
    return BRIDGE_BASE / arg



HEADINGS = ["## Current goal", "## Next action", "## Open questions"]


def extract_log_entries(text, n=3):
    entries = []
    for line in text.splitlines():
        if line.startswith("## "):
            entries.append(line[3:].strip())
            if len(entries) == n:
                break
    return entries


def content_to_html(text):
    lines = text.splitlines()
    list_items = [line[2:] for line in lines if line.startswith("- ")]
    non_list = [line for line in lines if line and not line.startswith("- ")]
    if list_items and not non_list:
        items = "".join(f"<li>{html.escape(item)}</li>" for item in list_items)
        return f"<ul>{items}</ul>"
    return f"<p>{html.escape(text)}</p>"


def format_html(name, sections, entries):
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        f"  <title>vault-brief: {html.escape(name)}</title>",
        "</head>",
        "<body>",
        f"<h1>vault-brief: {html.escape(name)}</h1>",
    ]
    for heading, content in sections.items():
        label = heading.lstrip("# ")
        parts.append(f"<h2>{html.escape(label)}</h2>")
        parts.append(content_to_html(content))
    parts.append("<h2>Recent log</h2>")
    items = "".join(f"<li>{html.escape(e)}</li>" for e in entries)
    parts.append(f"<ul>{items}</ul>")
    parts += ["</body>", "</html>"]
    return "\n".join(parts)


def format_markdown(name, sections, entries):
    lines = [f"# vault-brief: {name}", ""]
    for heading, content in sections.items():
        label = heading.lstrip("# ")
        lines.append(f"## {label}")
        lines.append(content)
        lines.append("")
    lines.append("## Recent log")
    for entry in entries:
        lines.append(f"- {entry}")
    lines.append("")
    return "\n".join(lines)


def format_plain(sections, entries):
    lines = []
    for heading, content in sections.items():
        label = heading.lstrip("# ").upper()
        lines.append(label)
        lines.append(content)
        lines.append("")
    lines.append("---")
    lines.append("LOG (LAST 3)")
    for entry in entries:
        lines.append(entry)
    lines.append("")
    return "\n".join(lines)


def extract_section(text, heading):
    pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def main():
    args = sys.argv[1:]
    html_mode = "--html" in args
    markdown = "--markdown" in args
    if html_mode and markdown:
        print("Error: --html and --markdown cannot be used together.", file=sys.stderr)
        sys.exit(1)
    args = [a for a in args if a not in ("--html", "--markdown")]
    if len(args) != 1:
        print("Usage: python brief.py <project-name> [--markdown] [--html]", file=sys.stderr)
        print("       python brief.py /full/path/to/bridge [--markdown] [--html]", file=sys.stderr)
        sys.exit(1)

    bridge_path = resolve_bridge_path(args[0])

    if not bridge_path.is_dir():
        print(f"Error: bridge directory not found: {bridge_path}", file=sys.stderr)
        sys.exit(1)

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

    log_text = log_file.read_text()
    entries = extract_log_entries(log_text)

    if html_mode:
        out = Path("brief.html")
        out.write_text(format_html(bridge_path.name, sections, entries))
        print(f"Wrote {out}")
    elif markdown:
        print(format_markdown(bridge_path.name, sections, entries))
    else:
        print(format_plain(sections, entries), end="")


if __name__ == "__main__":
    main()
