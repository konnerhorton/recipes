# Cooklang `.cook` File Reference

This file is a reference for generating valid `.cook` recipe files in the Cooklang format.
Spec source: https://github.com/cooklang/spec

---

## File Structure

A `.cook` file is a plain-text recipe. 
Each file represents one recipe.
The file may optionally begin with a YAML front matter block for metadata, followed by recipe steps written as natural-language paragraphs.

```
---
title: Recipe Name
servings: 4
---

Step one of the recipe with @ingredient{quantity%unit}.

Step two, a new paragraph.
```

---

## Ingredients

Use `@` to mark an ingredient inline within a step.

- **Single-word ingredient** (no braces needed):
  ```
  Add @salt to taste.
  ```

- **Multi-word ingredient** (use `{}` to end the name):
  ```
  Add @ground black pepper{} to taste.
  ```

- **Ingredient with quantity**:
  ```
  Poke holes in @potato{2}.
  ```

- **Ingredient with quantity and unit** (separate with `%`):
  ```
  Place @bacon strips{1%kg} on a baking sheet.
  Glaze with @maple syrup{1/2%tbsp}.
  ```

- **Fixed quantity (does not scale)**  — prefix quantity with `=`:
  ```
  Add @salt{=1%tsp} to taste.
  ```

- **Referencing another recipe file**:
  ```
  Pour over with @./sauces/Hollandaise{150%g}.
  ```

- **Short-hand preparation** (append in parentheses after the ingredient):
  ```
  Mix @onion{1}(peeled and finely chopped) and @garlic{2%cloves}(peeled and minced) into paste.
  ```

---

## Cookware

Use `#` to mark cookware.

- **Single-word cookware** (no braces needed):
  ```
  Place the potatoes into a #pot.
  ```

- **Multi-word cookware** (use `{}` to end the name):
  ```
  Mash with a #potato masher{}.
  ```

---

## Timers

Use `~` to define a timer.

- **Anonymous timer**:
  ```
  Bake for ~{25%minutes}.
  ```

- **Named timer** (apps can use the name in notifications):
  ```
  Boil @eggs{2} for ~eggs{3%minutes}.
  ```

Timers do **not** scale with servings.

---

## Steps

Each paragraph is a step. Separate steps with a blank line.

```
Bring a #pot of water to a boil.

Add @pasta{200%g} and cook for ~{10%minutes}.
```

---

## Comments

- **Line comment** (to end of line):
  ```
  -- Don't burn the roux!
  Stir the @butter{} until melted. -- keep heat low
  ```

- **Block (inline) comment**:
  ```
  Add @milk{4%cup} [- TODO: switch to ml -], stirring constantly.
  ```

---

## Notes

Use `>` at the start of a line to add a note (background info, tips, anecdotes — not part of the cooking steps):

```
> This dish originates from the Emilia-Romagna region of Italy.

Cook @pasta{200%g} according to package directions.
```

---

## Sections

Use `=` to divide a recipe into named sections. The section name and extra `=` signs are optional; any number of `=` signs works.

```
= Dough

Mix @flour{200%g} and @water{100%ml} until smooth.

== Filling ==

Combine @cheese{100%g} and @spinach{50%g}, then season to taste.
```

---

## Metadata (YAML Front Matter)

Place a YAML block between `---` delimiters at the very top of the file.

```yaml
---
title: Spaghetti Carbonara
servings: 4
tags:
  - pasta
  - quick
  - comfort food
source: https://example.org/recipe
author: Jane Doe
time required: 30 minutes
prep time: 10 minutes
cook time: 20 minutes
difficulty: easy
cuisine: Italian
diet: gluten-free
locale: en_GB
introduction: A classic Roman pasta dish made with eggs, cheese, and guanciale.
---
```

### Canonical Metadata Keys

| Key | Purpose | Example |
|-----|---------|---------|
| `title` | Recipe title | `Uzbek Manti` |
| `servings` / `serves` / `yield` | Default serving size (used for scaling) | `4`, `15 cups worth` |
| `source` / `source.name` | Recipe origin (URL or text) | `https://example.org/recipe` |
| `author` / `source.author` | Recipe author | `John Doe` |
| `source.url` | URL when using nested source format | `https://example.org/recipe` |
| `time required` / `time` / `duration` | Total prep + cook time | `1h30m`, `45 minutes` |
| `prep time` / `time.prep` | Preparation time only | `2 hour 30 min` |
| `cook time` / `time.cook` | Cooking time only | `10 minutes` |
| `difficulty` | Recipe difficulty | `easy` |
| `cuisine` | Cuisine type | `French` |
| `diet` | Dietary restriction/guideline | `gluten-free` |
| `course` / `category` | Meal course | `dinner` |
| `tags` | Descriptive tags | `[2022, baking, summer]` |
| `locale` | Language/region (ISO 639 + optional ISO 3166) | `es_VE`, `en_GB`, `fr` |
| `image` / `images` / `picture` / `pictures` | Image URL(s) | `https://example.org/img.jpg` |
| `introduction` / `description` | Additional recipe notes | `A traditional dish...` |

---

## Scaling and Servings

- Set default servings in metadata: `servings: 4`
- If not set, defaults to 1 serving.
- All ingredient quantities are written for the default serving size.
- Ingredients **scale linearly** by default.
- Prefix a quantity with `=` to **fix** it (no scaling): `@salt{=1%tsp}`
- Timers and cookware **never scale**.

```
---
servings: 4
---

Mix @flour{500%g} with @water{300%ml}.
Add @yeast{=1%packet} and let rise for ~{1%hour}.
```

When scaled to 8: flour → 1000g, water → 600ml, yeast stays at 1 packet, timer stays 1 hour.

---

## Images (Convention)

Place image files alongside the `.cook` file using matching names:

```
Baked Potato.cook
Baked Potato.jpg        ← recipe image
Baked Potato.0.jpg     ← image for step 0
Baked Potato.3.jpg     ← image for step 3
```

Supported formats: `.png`, `.jpg`

---

## Complete Example

```cooklang
---
title: Spaghetti Carbonara
servings: 2
time required: 30 minutes
difficulty: easy
cuisine: Italian
tags:
  - pasta
  - quick
---

> Use guanciale if you can find it — pancetta works in a pinch.

= Pasta

Bring a #large pot{} of water to a boil and add @salt{=1%tbsp}. Cook @spaghetti{200%g} for ~pasta{10%minutes} or until al dente.

== Sauce ==

While the pasta cooks, fry @guanciale{100%g}(diced) in a #pan{} over medium heat until crispy. -- don't add oil

Whisk together @egg yolks{3} and @Pecorino Romano{50%g}(finely grated) in a #bowl{}.

Drain the pasta, reserving @pasta water{50%ml}. Remove the pan from heat, add the pasta, and quickly stir in the egg mixture. Add pasta water a little at a time to loosen. [- keep heat OFF to avoid scrambling the eggs -]

Season with @ground black pepper{} and serve immediately.
```

---

## Quick Syntax Reference

| Syntax | Purpose |
|--------|---------|
| `@ingredient{}` | Multi-word ingredient, no quantity |
| `@ingredient{qty}` | Ingredient with quantity |
| `@ingredient{qty%unit}` | Ingredient with quantity and unit |
| `@ingredient{=qty%unit}` | Fixed quantity (won't scale) |
| `@ingredient{qty}(prep)` | Ingredient with preparation note |
| `@./path/Recipe{qty%unit}` | Reference to another recipe |
| `#cookware{}` | Multi-word cookware |
| `~{qty%unit}` | Anonymous timer |
| `~name{qty%unit}` | Named timer |
| `-- text` | Line comment |
| `[- text -]` | Inline block comment |
| `> text` | Note (not a step) |
| `= Section Name` | Section divider |
| blank line | Step separator |