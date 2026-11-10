# Home

## Welcome

This is meant to be a quick solution to a recipe sharing problem. Some imrpovements (hopefully) coming in the future:

- Better cataloging so it's easier to "discover" recipes.
- Impelement (somehow) with [cooklang](https://cooklang.org/) language so that recipes can be interacted with more effectively.
  - This might require turning this into a WASM.

For now, use the tags below to provide some minimally useful recipe selection.

## Authoring

Recipes are written in [Cooklang](https://cooklang.org/) under `cook/` (see `COOKLANG.md` for syntax rules). The site pages in `docs/recipes/` are generated and not committed.

1. Write or edit `cook/<recipe-name>.cook`.
2. Validate: `cd cook && cook doctor`
3. Generate the markdown: `uv run python scripts/build_recipes.py` (uses `templates/recipe.md.jinja`; needs [cookcli](https://github.com/cooklang/cookcli) 0.28.1 on `PATH`, or set `COOK=/path/to/cook`)
4. Preview: `uv run mkdocs serve`

CI runs steps 3 and 4 (as `mkdocs gh-deploy`) on every push to `main`.

## Shopping list

`uv run python scripts/shopping_list.py laap cilantro-lime-rice:2` prints a combined shopping list for the given recipes, one item per line, and copies it to the clipboard. Paste it into a Google Keep checklist note and each line becomes a checkbox. `:N` scales a recipe. Other `cook shopping-list` options, such as `--extra "paper towels"` and `--include-optional`, are passed through.
