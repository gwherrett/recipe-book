#!/usr/bin/env python3
"""
generate_indexes.py

Scans the `recipes/` folder and regenerates:

- Recipe-Index-flat.md        (alphabetical)
- Recipe-Index-canonical.md   (by cuisine)
- Recipe-Index-category.md    (by category)

Run locally with:
    python generate_indexes.py
"""

from pathlib import Path
from collections import defaultdict
import re
import yaml  # pip install pyyaml

RECIPE_DIR = Path("recipes")
FLAT_INDEX = Path("Recipe-Index-flat.md")
CUISINE_INDEX = Path("Recipe-Index-canonical.md")
CATEGORY_INDEX = Path("Recipe-Index-category.md")


def parse_markdown_with_yaml(path: Path):
    """Return (meta: dict, body: str) for a markdown file with YAML front matter."""
    text = path.read_text(encoding="utf-8")

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            yaml_part = parts[1]
            body = parts[2].lstrip("\n")
            meta = yaml.safe_load(yaml_part) or {}
            return meta, body

    return {}, text


def anchor_from_text(text: str) -> str:
    """Make a GitHub-style anchor from a heading text."""
    anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return anchor


def main():
    if not RECIPE_DIR.is_dir():
        raise SystemExit(f"recipes directory not found at {RECIPE_DIR.resolve()}")

    entries = []

    for md_path in sorted(RECIPE_DIR.glob("*.md")):
        meta, body = parse_markdown_with_yaml(md_path)
        title = meta.get("title") or md_path.stem
        cuisine = meta.get("cuisine")
        category = meta.get("category")
        rel_path = f"recipes/{md_path.name}"

        entries.append(
            {
                "title": title,
                "cuisine": cuisine,
                "category": category,
                "rel_path": rel_path,
            }
        )

    # 1) Flat index (alphabetical)
    flat_lines = ["# Recipe Index (Flat — Alphabetical)", ""]
    for e in sorted(entries, key=lambda x: x["title"].lower()):
        flat_lines.append(f'- [{e["title"]}]({e["rel_path"]})')

    FLAT_INDEX.write_text("\n".join(flat_lines) + "\n", encoding="utf-8")

    # 2) By cuisine
    by_cuisine = defaultdict(list)
    for e in entries:
        cuisine = e["cuisine"] or "Unassigned"
        by_cuisine[cuisine].append(e)

    cuisine_keys = sorted(by_cuisine.keys(), key=lambda x: x.lower())

    cuisine_lines = ["# Recipe Index (By Cuisine)", ""]
    cuisine_lines.append("## Cuisines")
    cuisine_lines.append("")
    for c in cuisine_keys:
        anchor = anchor_from_text(c)
        cuisine_lines.append(f"- [{c}](#{anchor})")
    cuisine_lines.append("")

    for c in cuisine_keys:
        anchor = anchor_from_text(c)
        cuisine_lines.append(f"## {c}")
        cuisine_lines.append("")
        for e in sorted(by_cuisine[c], key=lambda x: x["title"].lower()):
            cuisine_lines.append(f'- [{e["title"]}]({e["rel_path"]})')
        cuisine_lines.append("")

    CUISINE_INDEX.write_text("\n".join(cuisine_lines) + "\n", encoding="utf-8")

    # 3) By category
    by_category = defaultdict(list)
    for e in entries:
        cat = e["category"] or "Uncategorized"
        by_category[cat].append(e)

    cat_keys = sorted(by_category.keys(), key=lambda x: x.lower())

    cat_lines = ["# Recipe Index (By Category)", ""]
    cat_lines.append("## Categories")
    cat_lines.append("")
    for cat in cat_keys:
        anchor = anchor_from_text(cat)
        cat_lines.append(f"- [{cat}](#{anchor})")
    cat_lines.append("")

    for cat in cat_keys:
        anchor = anchor_from_text(cat)
        cat_lines.append(f"## {cat}")
        cat_lines.append("")
        for e in sorted(by_category[cat], key=lambda x: x["title"].lower()):
            cat_lines.append(f'- [{e["title"]}]({e["rel_path"]})')
        cat_lines.append("")

    CATEGORY_INDEX.write_text("\n".join(cat_lines) + "\n", encoding="utf-8")

    print("Indexes regenerated:")
    print(f"  - {FLAT_INDEX}")
    print(f"  - {CUISINE_INDEX}")
    print(f"  - {CATEGORY_INDEX}")


if __name__ == "__main__":
    main()
