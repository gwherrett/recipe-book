## Project Structure
recipe-book/
  recipes/
    *.md                        # Each recipe, with YAML metadata
  generate_indexes.py           # Script to auto-build three index files
  add_health_fields.py          # Script to add missing health rating fields
  Recipe-Index-flat.md          # Alphabetical index
  Recipe-Index-canonical.md     # Sorted by cuisine
  Recipe-Index-category.md      # Sorted by category
  .github/
    workflows/
      generate-indexes.yml      # GitHub Action to auto-regenerate indexes
  README.md

All recipes live in the recipes/ folder in flattened form:
recipes/<slug>.md
Each file contains YAML front matter followed by Markdown content.

## YAML Metadata Format

Every recipe includes consistent fields for title, slug, cuisine, category, and health-rating metadata.

Example:

---
title: "Adobo Sauce"
slug: adobo-sauce
cuisine: Mexican
category: Sauces & Condiments
health_rating: 4
health_rating_label: "Generally Healthy"
---

### Required fields

| Field                 | Type   | Description                                                  |
| --------------------- | ------ | ------------------------------------------------------------ |
| `title`               | string | Human-readable recipe name                                   |
| `slug`                | string | Lowercase, URL-safe file name                                |
| `cuisine`             | string | Normalized cuisine (e.g., Italian, Middle Eastern, Southern) |
| `category`            | string | One of the canonical categories                              |
| `health_rating`       | int    | 0–5 scale                                                    |
| `health_rating_label` | string | Readable rating label                                        |

### Health Rating System (5-Point)

Each recipe has a numeric rating and a human-friendly description:

| Rating | Label                     | Meaning                                   |
| ------ | ------------------------- | ----------------------------------------- |
| **5**  | Very Healthy Everyday     | Mostly plants, lean protein, whole grains |
| **4**  | Generally Healthy         | Good everyday choice with modest richness |
| **3**  | Mixed / Context-Dependent | Balanced but may need portion control     |
| **2**  | Rich / Heavy              | High fat/sugar/refined carbs; occasional  |
| **1**  | Treat / Indulgent         | Deep fried, dessert, very rich            |
| **0**  | Unrated                   | Not evaluated yet                         |

## Automatic Index Generation (GitHub Action)

Whenever you:
- Add a new recipe
- Modify an existing recipe
- Update metadata

…GitHub will automatically regenerate:
- Recipe-Index-flat.md
- Recipe-Index-canonical.md (by cuisine)
- Recipe-Index-category.md (by category)

### How it works

A GitHub Action lives at:
.github/workflows/generate-indexes.yml
It 
1. Detects changes to any recipes/*.md
2. Runs generate_indexes.py
3. Commits the updated index files back to the repository

This ensures your indexes are always up to date without any manual work.

## Local Development Tools
### Generate indexes manually

If you want to regenerate indexes locally:

pip install pyyaml
python generate_indexes.py

## Add missing health rating fields

To ensure all recipes have the correct health metadata:

python add_health_fields.py

### Adding a New Recipe
1. Create a new file under recipes/:
recipes/my-new-recipe.md
2. Include a YAML block at the top:
---
title: "My New Recipe"
slug: my-new-recipe
cuisine: Italian
category: Mains
health_rating: 0
health_rating_label: "Unrated"
---
3.  Commit & Push 
git add recipes/my-new-recipe.md
git commit -m "Add new recipe: My New Recipe"
git push

GitHub Actions will automatically regenerate all index files.

## Contributing
This is a personal project, but future contributors could follow:
- Consistent slug naming
- Correct categories & cuisines
- Proper YAML metadata
- Reasonable health ratings

### License
Personal use; not currently intended for public distribution.
