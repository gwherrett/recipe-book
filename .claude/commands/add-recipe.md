Parse the recipe text below and create a properly formatted recipe markdown file in this repository.

## Recipe text

$ARGUMENTS

---

## Your task

1. Read and understand the recipe text above.
2. Extract all metadata and content.
3. Write the file to `recipes/<slug>.md`.

---

## Metadata rules

### Required frontmatter fields

```yaml
title: Human-readable recipe name
slug: lowercase-hyphen-separated  # derived from title
cuisine: <see canonical list>
category: <see canonical list>
health_rating: <0–5 integer>
health_rating_label: <matching label>
```

### Canonical cuisines

African, Asian, Balkan, British, Cantonese, Caribbean, Chinese, Filipino, French, Indian, Italian, Japanese, Mediterranean, Mexican, Middle Eastern, North American, Persian, Southern / Cajun, Spanish, Thai, Vietnamese

Pick the closest match. If the recipe blends two cuisines, choose the dominant one or the most specific fit.

**Cuisine notes:**
- Use **Cantonese** for Cantonese, Hong Kong, and Macau dishes — not Chinese.
- **Asian** is a fallback for pan-Asian dishes that don't fit a more specific cuisine.

**If the recipe's cuisine is not in this list:** stop and ask the user whether to use the closest existing cuisine or add a new one. Do not silently pick a match.

### Canonical categories

Appetizers, Breads & Pastries, Breakfast & Brunch, Dessert, Dressings & Marinades, Drinks, Mains, Pasta, Salads & Sides, Sauces & Condiments, Snacks, Soups & Stocks, Spice Mixes & Pastes

### Health rating scale

| Rating | Label                 | When to use                                      |
|--------|-----------------------|--------------------------------------------------|
| 5      | Very Healthy Everyday | Mostly plants, lean protein, whole grains        |
| 4      | Generally Healthy     | Good everyday choice with modest richness        |
| 3      | Mixed / Context-Dependent | Balanced but may need portion control        |
| 2      | Rich / Heavy          | High fat, sugar, or refined carbs; occasional    |
| 1      | Treat / Indulgent     | Deep fried, very rich desserts, party food       |
| 0      | Unrated               | Cannot be assessed from the information provided |

**Important:** 5 is the healthiest, 1 is the least healthy. The `health_rating` integer and `health_rating_label` must correspond exactly to the same row in the table above.

---

## Body format

Follow this structure, adapting section names to match the source where they differ (e.g. keep "Method" if that's what the source uses; use "Directions" or "Instructions" if unspecified):

```markdown
---
title: Recipe Title
slug: recipe-slug
cuisine: Cuisine
category: Category
health_rating: 3
health_rating_label: Mixed / Context-Dependent
---

# Recipe Title

**Source:** [Source name](URL)  ← omit entirely if no source is in the text

**Prep Time:** X minutes
**Cook Time:** X minutes
**Yield:** X servings

One or two sentences describing what the dish is and what makes it interesting. Omit if nothing meaningful can be inferred.

---

## Ingredients

- ingredient 1
- ingredient 2

### Sub-section (if the recipe has distinct component groups)

- ingredient 3

---

## Instructions

1. **Step name:** Detailed step text.

2. **Step name:** Detailed step text.

---

## Notes   ← include only if the source has notes, tips, variations, storage info, etc.

- Note 1
- Note 2
```

---

## Content guidelines

- **Faithfulness:** Preserve all quantities, ingredients, and instructions exactly as written. Do not add, remove, or substitute anything.
- **Fractions:** Use Unicode fractions — ½ ¼ ¾ ⅓ ⅔ — not decimals or slash notation (1/2).
- **Step headers:** Bold the first phrase of each instruction step when it forms a natural label (e.g. `**Preheat oven:**`). If the source already has bold labels, keep them.
- **Horizontal rules:** Place a `---` rule before `## Ingredients` and before `## Instructions`. Also place one between other major sections if the source separates them visually.
- **Ingredient sub-sections:** Use `### Sub-section Name` when the recipe has clearly distinct component groups (e.g. "For the sauce", "Topping").
- **Extra sections:** Preserve any Notes, Tips, Variations, Storage, Make-Ahead, or Serving Suggestions sections from the original. Use the source's heading name.
- **Source line:** If a URL is present in the text, format it as `**Source:** [Name](URL)`. If only a name/book/show is mentioned, use `**Source:** Name`. If no source info is present, omit the line entirely.
- **Slug:** Derive from the title — lowercase, spaces replaced with hyphens, special characters removed. For "za'atar" use "zaatar", for "Mac & Cheese" use "mac-and-cheese".
- **After writing the file:** Confirm the file path and show the user the frontmatter so they can verify the metadata before committing.
