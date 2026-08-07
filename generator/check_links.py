#!/usr/bin/env python3
"""Walk dist/, find every internal href/src, and verify it resolves to a real file."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT, "dist")

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def resolve(path_from_root_of_page, link):
    if link.startswith(("http://", "https://", "mailto:", "data:", "#")):
        return None  # external / non-file, skip
    # normalize
    base_dir = os.path.dirname(path_from_root_of_page)
    target = os.path.normpath(os.path.join(base_dir, link))
    return target


def main():
    errors = []
    html_files = []
    for dirpath, _, filenames in os.walk(DIST_DIR):
        for fn in filenames:
            if fn.endswith(".html"):
                html_files.append(os.path.join(dirpath, fn))

    for html_file in html_files:
        rel_page = os.path.relpath(html_file, DIST_DIR)
        with open(html_file, encoding="utf-8") as f:
            content = f.read()
        for link in LINK_RE.findall(content):
            target = resolve(rel_page, link)
            if target is None:
                continue
            # directory-style link -> expect index.html inside
            candidate_file = os.path.join(DIST_DIR, target)
            candidate_index = os.path.join(DIST_DIR, target, "index.html")
            if os.path.isfile(candidate_file) or os.path.isfile(candidate_index) or os.path.isdir(os.path.join(DIST_DIR, target)):
                continue
            errors.append(f"{rel_page}: broken link -> {link} (resolved: {target})")

    if errors:
        print(f"FOUND {len(errors)} BROKEN LINK(S):")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"OK: checked {len(html_files)} pages, no broken internal links.")


if __name__ == "__main__":
    main()
