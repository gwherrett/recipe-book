#!/usr/bin/env python3
"""
add_health_fields.py

Adds health-related fields to all recipe markdown files in the `recipes/` folder.

Fields added (if missing):

  health_rating: 0             # 0–5, where 0 = Unrated
  health_rating_label: "Unrated"

Usage:
  - Place this script in the root of your recipe repo (same level as `recipes/`).
  - Run:  python add_health_fields.py
"""

import re
from pathlib import Path
import yaml  # pip install pyyaml


# -------- Configuration --------

RECIPES_DIR = Path("recipes")

DEFAULT_HEALTH_RATING = 0
DEFAULT_HEALTH_LABEL = "Unrated"


# -------- Helpers --------

def parse_markdown_with_yaml(path: Path):
    """
    Parse a markdown file with optional YAML front matter.

    Returns:
        (meta: dict, body: str)
    """
    text = path.read_text(encoding="utf-8")

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            yaml_part = parts[1]
            body = parts[2].lstrip("\n")
            meta = yaml.safe_load(yaml_part) or {}
            return meta, body

    return {}, text


def dump_markdown_with_yaml(meta: dict, body: str) -> str:
    """
    Render YAML + body back to markdown text.
    """
    yaml_part = yaml.safe_dump(meta, sort_keys=False).strip()
    return f"---\n{yaml_part}\n---\n\n{body.lstrip()}"


# -------- Main logic --------

def ensure_health_fields(meta: dict) -> dict:
    """
    Ensure `health_rating` and `health_rating_label` exist.
    """
    if "health_rating" not in meta:
        meta["health_rating"] = DEFAULT_HEALTH_RATING

    if "health_rating_label" not in meta:
        meta["health_rating_label"] = DEFAULT_HEALTH_LABEL

    return meta


def main():
    if not RECIPES_DIR.is_dir():
        raise SystemExit(f"Recipes directory not found: {RECIPES_DIR.resolve()}")

    md_files = sorted(RECIPES_DIR.glob("*.md"))
    if not md_files:
        raise SystemExit(f"No markdown files found in {RECIPES_DIR.resolve()}")

    updated_count = 0

    for path in md_files:
        meta, body = parse_markdown_with_yaml(path)
        if meta is None:
            meta = {}

        before = (meta.get("health_rating"), meta.get("health_rating_label"))
        meta = ensure_health_fields(meta)
        after = (meta.get("health_rating"), meta.get("health_rating_label"))

        if before != after:
            new_text = dump_markdown_with_yaml(meta, body)
            path.write_text(new_text, encoding="utf-8")
            updated_count += 1
            print(f"Updated: {path.name}")

    print(f"\nDone. Updated {updated_count} recipe file(s).")


if __name__ == "__main__":
    main()
