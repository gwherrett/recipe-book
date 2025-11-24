#!/usr/bin/env python3
"""
generate_indexes.py

Scans the `recipes/` folder and regenerates:

- Recipe-Index-flat.md        (alphabetical)
- Recipe-Index-canonical.md   (by cuisine)
- Recipe-Index-category.md    (by category)
- Recipe-Index-health.md      (by health_rating)

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
HEALTH_INDEX = Path("Recipe-Index-health.md")

# Canonical health rating labels
RATING_LABELS = {
    0: "Unrated                   (Not evaluated yet)",
    1: "Indulgence                (Desserts, deep-fried, very rich)",
    2: "High in Fat/Sugar/Salt    (Rich, salty, or sugary; occasional)",
    3: "Manage portion size       (Balanced but energy-dense; watch servings)",
    4: "Healthy                   (Good everyday choice)",
    5: "Eat More                  (Light, plant-forward, or very wholesome)",
}


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

        raw_rating = meta.get("health_rating", 0)
        label_from_file = meta.get("health_rating_label")

        # Normalize rating to int 0–5
        try:
            health_rating = int(raw_rating)
        except (TypeError, ValueError):
            health_rating = 0
        if health_rating < 0 or health_rating > 5:
            health_rating = 0

        health_label = label_from_file or RATING_LABELS.get(health_rating, "Unrated")

        entries.append(
            {
                "title": title,
                "cuisine": cuisine,
                "category": category,
                "rel_path": rel_path,
                "health_rating": health_rating,
                "health_label": health_label,
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

    # 4) By health rating
    by_health = defaultdict(list)
    for e in entries:
        rating = e["health_rating"]
        by_health[rating].append(e)

    # Highest rating first: 5 → 0
    health_keys = sorted(by_health.keys(), reverse=True)

    health_lines = ["# Recipe Index (By Health Rating)", ""]
    health_lines.append("## Health Ratings")
    health_lines.append("")
    for rating in health_keys:
        label = RATING_LABELS.get(rating, "Unrated")
        heading_text = f"{rating} – {label}"
        anchor = anchor_from_text(heading_text)
        health_lines.append(f"- [{heading_text}](#{anchor})")
    health_lines.append("")

    for rating in health_keys:
        label = RATING_LABELS.get(rating, "Unrated")
        heading_text = f"{rating} – {label}"
        anchor = anchor_from_text(heading_text)
        health_lines.append(f"## {heading_text}")
        health_lines.append("")
        for e in sorted(by_health[rating], key=lambda x: x["title"].lower()):
            health_lines.append(f'- [{e["title"]}]({e["rel_path"]})')
        health_lines.append("")

    HEALTH_INDEX.write_text("\n".join(health_lines) + "\n", encoding="utf-8")

    print("Indexes regenerated:")
    print(f"  - {FLAT_INDEX}")
    print(f"  - {CUISINE_INDEX}")
    print(f"  - {CATEGORY_INDEX}")
    print(f"  - {HEALTH_INDEX}")


if __name__ == "__main__":
    main()
