#!/usr/bin/env python3
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml")
    sys.exit(1)

# Flat folder: recipe-book/recipes/*.md
RECIPE_ROOT = Path("recipes")

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Updated canonical rating labels
RATING_LABELS = {
    0: "Unrated",
    1: "Indulgence",
    2: "High in Fat/Sugar/Salt",
    3: "Manage portion size",
    4: "Healthy",
    5: "Eat Everyday",
}


def load_front_matter(text: str):
    """Extract YAML front matter and body."""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None, text
    fm_text = m.group(1)
    content = text[m.end():]
    fm = yaml.safe_load(fm_text) or {}
    return fm, content


def dump_front_matter(fm, content: str) -> str:
    """Reassemble YAML + markdown body."""
    fm_text = yaml.safe_dump(fm, sort_keys=False).strip()
    return f"---\n{fm_text}\n---\n\n{content.lstrip()}"


def iter_recipe_files():
    """Yield all recipe markdown files in flat folder."""
    for path in RECIPE_ROOT.glob("*.md"):
        name = path.name.lower()
        if name.startswith("index") or name.startswith("readme"):
            continue
        yield path


def print_scale():
    """Print the full health rating system."""
    print("Health Rating System (5-Point)")
    print("=====================================")
    print("5 = Eat Everyday              (Light, plant-forward, or very wholesome)")
    print("4 = Healthy                   (Good everyday choice)")
    print("3 = Manage portion size       (Balanced but energy-dense; watch servings)")
    print("2 = High in Fat/Sugar/Salt    (Rich, salty, or sugary; occasional)")
    print("1 = Indulgence                (Desserts, deep-fried, very rich)")
    print("0 = Unrated                   (Not evaluated yet)")
    print("")


def prompt_rating(fm, path: Path):
    """Prompt user to update a recipe's health rating."""

    title = fm.get("title", path.stem)
    current_rating = fm.get("health_rating", 0)
    current_label = fm.get("health_rating_label", "Unrated")

    print("\n" + "=" * 60)
    print(f"File:   {path}")
    print(f"Title:  {title}")
    print(f"Current: rating={current_rating} label='{current_label}'")
    print("-" * 60)
    print_scale()
    print("Enter a number 0–5, 's' to skip, or Enter to keep current value.")

    while True:
        resp = input("New rating [0–5 / s / Enter]: ").strip().lower()

        if resp == "":
            return current_rating, current_label  # keep existing
        if resp == "s":
            return current_rating, current_label  # skip

        if resp in {"0", "1", "2", "3", "4", "5"}:
            rating = int(resp)
            label = RATING_LABELS[rating]
            return rating, label

        print("Invalid input. Please enter 0–5, 's', or just press Enter.")


def main():
    """Main interactive review loop."""
    only_unrated = "--only-unrated" in sys.argv

    for path in iter_recipe_files():
        text = path.read_text(encoding="utf-8")
        fm, content = load_front_matter(text)

        if fm is None:
            print(f"Skipping {path} (no YAML front matter)")
            continue

        rating = fm.get("health_rating", 0)
        if only_unrated and rating != 0:
            continue

        new_rating, new_label = prompt_rating(fm, path)

        # Nothing changed
        if (
            new_rating == fm.get("health_rating", 0)
            and new_label == fm.get("health_rating_label", "Unrated")
        ):
            continue

        # Update front matter
        fm["health_rating"] = new_rating
        fm["health_rating_label"] = new_label

        # Rewrite file
        new_text = dump_front_matter(fm, content)
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated {path} → rating {new_rating} ({new_label})")

    print("\nDone reviewing health ratings.")
    print("Commit your changes and push to GitHub to trigger index regeneration.")


if __name__ == "__main__":
    main()
