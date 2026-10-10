#!/usr/bin/env python3
"""Check an agent-state folder so it syncs cleanly across machines.

Usage: lint_state.py STATE_DIR [--host NAME]

STATE_DIR holds `<skill>/<context>.md` files shared by every machine and
`hosts/<hostname>.md` files, each written only by its own machine.

- Shared files contain no absolute paths (/home, /mnt, /Users, /tmp, /srv,
  /data, /opt, /scratch) and no path-encoded Claude memory folders
  (~/.claude/projects/...). They name machine-specific places as `{name}`.
- Every `{name}` a shared file uses is defined in the Locations table of
  this machine's host file (`--host`, default: the short hostname). A
  missing definition is reported, so the host file gets the entry.
Exits 1 if any check fails.
"""
import argparse
import re
import socket
import sys
from pathlib import Path

ABSOLUTE = re.compile(r"(?<![\w.~{}-])/(home|mnt|Users|tmp|srv|data|opt|scratch)/[\w.-]+")
MEMORY_DIR = re.compile(r"~/\.claude/projects/[\w.-]+")
PLACEHOLDER = re.compile(r"\{([\w-]+)(?::[^}]*)?\}")
DEFINED = re.compile(r"^\|\s*`\{([\w-]+)(?::[^}]*)?\}`\s*\|", re.M)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("state_dir", type=Path)
    parser.add_argument("--host", default=socket.gethostname().split(".")[0])
    args = parser.parse_args()
    host_file = args.state_dir / "hosts" / f"{args.host}.md"
    defined = set(DEFINED.findall(host_file.read_text())) if host_file.is_file() else set()
    errors = []
    if not host_file.is_file():
        errors.append(f"{host_file}: missing; create it with a Locations table for this machine")
    for path in sorted(args.state_dir.rglob("*.md")):
        rel = path.relative_to(args.state_dir)
        if rel.parts[0] == "hosts":
            continue
        for n, line in enumerate(path.read_text().splitlines(), 1):
            for m in ABSOLUTE.finditer(line):
                errors.append(f"{rel}:{n}: absolute path {m.group(0)!r}; name it as a {{location}} in the host file")
            for m in MEMORY_DIR.finditer(line):
                errors.append(f"{rel}:{n}: machine-specific memory folder {m.group(0)!r}; use {{memory:<repo>}}")
            for m in PLACEHOLDER.finditer(line):
                if host_file.is_file() and m.group(1) not in defined:
                    errors.append(f"{rel}:{n}: {{{m.group(1)}}} is not defined in {host_file.name}")
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s)" if errors else "state ok", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
