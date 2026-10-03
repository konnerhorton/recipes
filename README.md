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
