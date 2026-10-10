#!/usr/bin/env python3
"""Check agent skills for size, structure and private details.

Usage: lint_skills.py SKILLS_DIR [--public --denylist FILE]

SKILLS_DIR holds one folder per skill. For each skill it checks:
- SKILL.md exists, has frontmatter with `name` equal to the folder name and a
  `description`;
- SKILL.md is at most MAX_MAIN_LINES lines and MAX_MAIN_WORDS words;
- each other .md file is at most MAX_REF_WORDS words;
- layout: only SKILL.md, a license file and the folders references/,
  scripts/ and assets/ at the top level; references/ holds .md files;
- every relative markdown link in any .md file resolves, and SKILL.md links
  every file in references/;
- with --public: no file contains an absolute home or mount path or a
  denylisted term, and the denylist must exist.

The denylist is a text file with one term per line (case-insensitive; `#`
starts a comment). It names private projects, hosts and people, so it lives
outside any public repo. Exits 1 if any check fails.
"""
import argparse
import re
import sys
from pathlib import Path

MAX_MAIN_LINES = 100
MAX_MAIN_WORDS = 1200
MAX_REF_WORDS = 2000
ALLOWED_DIRS = {"references", "scripts", "assets"}
LICENSE = re.compile(r"LICEN[CS]E(\.\w+)?$", re.I)
PRIVATE_PATH = re.compile(r"(/home/[\w.-]+|/Users/[\w.-]+|/mnt/[\w.-]+)")
LOCAL_LINK = re.compile(r"\]\(([\w./-]+)\)")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip()
    return fields


def load_denylist(path):
    terms = []
    for line in Path(path).read_text().splitlines():
        term = line.split("#", 1)[0].strip()
        if term:
            terms.append(term)
    return terms


def check_skill(skill, public, denylist):
    errors = []
    main = skill / "SKILL.md"
    if not main.is_file():
        return [f"{skill.name}: no SKILL.md"]
    text = main.read_text()
    fields = frontmatter(text)
    if fields is None:
        errors.append(f"{main}: missing frontmatter")
    else:
        if fields.get("name") != skill.name:
            errors.append(f"{main}: frontmatter name {fields.get('name')!r} != folder {skill.name!r}")
        if not fields.get("description"):
            errors.append(f"{main}: missing description")
    lines, words = len(text.splitlines()), len(text.split())
    if lines > MAX_MAIN_LINES or words > MAX_MAIN_WORDS:
        errors.append(
            f"{main}: {lines} lines, {words} words (limit {MAX_MAIN_LINES} lines, "
            f"{MAX_MAIN_WORDS} words); cut, then move step-specific material to reference files"
        )
    for entry in sorted(skill.iterdir()):
        if entry.name.startswith(".") or entry.name == "SKILL.md" or LICENSE.match(entry.name):
            continue
        if entry.is_dir() and entry.name in ALLOWED_DIRS:
            continue
        if entry.is_dir():
            hint = "rename it to references/, scripts/ or assets/"
        else:
            hint = "move it into " + ("references/" if entry.suffix == ".md" else "scripts/ or assets/")
        errors.append(f"{entry}: not allowed next to SKILL.md; {hint}")
    refs = skill / "references"
    if refs.is_dir():
        linked = {(skill / m.group(1)).resolve() for m in LOCAL_LINK.finditer(text)}
        for ref in sorted(refs.rglob("*")):
            if ref.is_file() and ref.suffix != ".md":
                errors.append(f"{ref}: references/ holds .md docs; move it to scripts/ or assets/")
            elif ref.is_file() and ref.resolve() not in linked:
                errors.append(f"{ref}: not linked from SKILL.md, so it is never read")
    for doc in sorted(skill.rglob("*.md")):
        for m in LOCAL_LINK.finditer(doc.read_text()):
            if not (doc.parent / m.group(1)).exists():
                errors.append(f"{doc}: links to {m.group(1)}, which does not exist")
    for path in sorted(skill.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        try:
            body = path.read_text()
        except UnicodeDecodeError:
            continue
        if path.suffix == ".md" and path != main and len(body.split()) > MAX_REF_WORDS:
            errors.append(f"{path}: {len(body.split())} words (reference limit {MAX_REF_WORDS})")
        if not public:
            continue
        for n, line in enumerate(body.splitlines(), 1):
            for m in PRIVATE_PATH.finditer(line):
                errors.append(f"{path}:{n}: private path {m.group(0)!r}")
            low = line.lower()
            for term in denylist:
                if term.lower() in low:
                    errors.append(f"{path}:{n}: denylisted term {term!r}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("skills_dir", type=Path)
    parser.add_argument("--denylist", type=Path)
    parser.add_argument("--public", action="store_true", help="also check for private details")
    args = parser.parse_args()
    denylist = []
    if args.public:
        if not (args.denylist and args.denylist.is_file()):
            print(f"--public needs a denylist file; {args.denylist} not found", file=sys.stderr)
            return 1
        denylist = load_denylist(args.denylist)
    errors = []
    for skill in sorted(p for p in args.skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        errors += check_skill(skill, args.public, denylist)
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s)" if errors else "skills ok", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
