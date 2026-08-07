#!/usr/bin/env python3
"""Validate every data/tasks/*.json file against the required task schema.
No external dependencies -- hand-rolled checks so CI needs nothing but python3."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
TASKS_DIR = os.path.join(DATA_DIR, "tasks")

REQUIRED_FIELDS = {
    "id": int,
    "slug": str,
    "category": str,
    "task": str,
    "trigger": str,
    "priority": str,
    "difficulty": int,
    "mode": str,
    "time": str,
    "cost": str,
    "steps": list,
    "videoTitle": str,
    "videoUrl": str,
    "verified": bool,
}
VALID_PRIORITIES = {"Safety-Critical", "Preventive", "Cosmetic", "Upgrade"}
VALID_MODES = {"DIY", "Pro", "DIY or Pro"}


def validate_file(path, fname):
    errs = []
    try:
        with open(path, encoding="utf-8") as f:
            t = json.load(f)
    except json.JSONDecodeError as e:
        return [f"{fname}: invalid JSON ({e})"]

    for field, ftype in REQUIRED_FIELDS.items():
        if field not in t:
            errs.append(f"{fname}: missing field '{field}'")
            continue
        if not isinstance(t[field], ftype):
            errs.append(f"{fname}: field '{field}' should be {ftype.__name__}, got {type(t[field]).__name__}")

    if "slug" in t and t["slug"] != fname[:-5]:
        errs.append(f"{fname}: slug '{t.get('slug')}' does not match filename")

    if "priority" in t and t["priority"] not in VALID_PRIORITIES:
        errs.append(f"{fname}: priority '{t['priority']}' not in {VALID_PRIORITIES}")

    if "mode" in t and t["mode"] not in VALID_MODES:
        errs.append(f"{fname}: mode '{t['mode']}' not in {VALID_MODES}")

    if "difficulty" in t and isinstance(t["difficulty"], int) and not (1 <= t["difficulty"] <= 5):
        errs.append(f"{fname}: difficulty {t['difficulty']} out of range 1-5")

    if "steps" in t and isinstance(t["steps"], list):
        if len(t["steps"]) == 0:
            errs.append(f"{fname}: steps list is empty")
        elif not all(isinstance(s, str) and s.strip() for s in t["steps"]):
            errs.append(f"{fname}: steps must all be non-empty strings")

    return errs


def main():
    errors = []
    seen_ids = {}
    seen_slugs = {}

    files = sorted(f for f in os.listdir(TASKS_DIR) if f.endswith(".json"))
    if not files:
        print("ERROR: no task files found in", TASKS_DIR)
        sys.exit(1)

    for fname in files:
        path = os.path.join(TASKS_DIR, fname)
        file_errs = validate_file(path, fname)
        errors.extend(file_errs)
        if not file_errs:
            with open(path, encoding="utf-8") as f:
                t = json.load(f)
            seen_ids.setdefault(t["id"], []).append(fname)
            seen_slugs.setdefault(t["slug"], []).append(fname)

    for tid, fnames in seen_ids.items():
        if len(fnames) > 1:
            errors.append(f"duplicate id {tid} used in: {fnames}")
    for slug, fnames in seen_slugs.items():
        if len(fnames) > 1:
            errors.append(f"duplicate slug '{slug}' used in: {fnames}")

    # categories.json must exist and be well-formed
    cat_path = os.path.join(DATA_DIR, "categories.json")
    if not os.path.isfile(cat_path):
        errors.append("categories.json is missing")
    else:
        with open(cat_path, encoding="utf-8") as f:
            cats = json.load(f)
        for name, meta in cats.items():
            if "code" not in meta or "blurb" not in meta:
                errors.append(f"category '{name}' missing 'code' or 'blurb'")

    if errors:
        print(f"FOUND {len(errors)} SCHEMA ERROR(S):")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"OK: {len(files)} task files valid.")


if __name__ == "__main__":
    main()
