# recipe-scaling: scale a recipe's quantities live in the browser

## Intent

### Goal
On any recipe page, a reader can pick a scale (for example ½×, 1×, 2×, 3×) and every scalable quantity on the page updates in place, in both the ingredient list and the steps. No page reload, no server. The site still deploys for free to GitHub Pages from the existing CI workflow.

### Why
- Cooking a half or double batch currently means doing the arithmetic by hand, on every quantity, while cooking.
- The README already lists "interact with recipes more effectively" via Cooklang as a goal. Cooklang's scaling rules are the most direct payoff of the migration to `.cook` files.
- Evidence gathered while drafting (cookcli 0.28.1, `cook report`):
  - The template only sees each quantity as a pre-formatted string (`0.5 cup`). `ing.quantity.value` and `.unit` are undefined, and the scalable/fixed flag isn't exposed.
  - Fractions come out as decimals: `{1/2%cup}` renders as `0.5 cup`.
  - `cook report recipe.cook:N` scales the whole recipe at build time. It scales ingredient-list *and* step quantities, and it leaves `=` fixed quantities alone (`@salt{=1%tsp}` stayed `1 tsp` at ×2).
- Only 9 of ~50 recipes have `servings` (TODO.md §1), and `makes`/`serves` are free text (`~20 muffins`, `4 3-oz portions`). So a plain multiplier works on every recipe; "number of servings" works on only a few.

### Constraints
- **Static hosting only:** GitHub Pages via `mkdocs gh-deploy` in `.github/workflows/ci.yml`. No server, no paid service.
- **No new toolchain in CI:** no npm or JS bundler. Any JS is a hand-written file served through MkDocs `extra_javascript`.
- **Pages work without JS:** they show the original 1× recipe, as today.
- **Cooklang scaling rules hold:** quantities scale linearly; `=` fixed quantities, timers and cookware don't scale; quantity-less or text quantities ("to taste") are unchanged.
- **Same cookcli:** stay on cookcli 0.28.1 (TODO.md "Tooling"). Upgrading is a separate unit.
- **Works with mkdocs-material**, including its instant navigation if that's turned on later.

### Out of scope
- **Unit conversion** (16 tbsp → 1 cup, imperial ↔ metric). That's a possible later unit.
- **Amounts in plain prose** that aren't marked up as Cooklang, e.g. "using 7.5g salt" in `adana-lamb-kebab`. They're already tracked in TODO.md §3.
- **Scaling sub-recipes on their own pages:** a linked sub-recipe opens at 1×. Carrying the scale over via the URL is a possible follow-up.
- **Remembering the chosen scale** across pages or visits.
- **Scaling the free-text `makes` / `serves` lines.**
- **Filling in the missing `servings` values** (TODO.md §1).

### SPEC sections touched
- There is no `SPEC.md` yet. The repo predates this process, so the current code and README serve as the baseline. 🟡 Proposed: don't write a product spec for this one feature. Revisit if more interactive features follow.
- Files expected to change: `templates/recipe.md.jinja`, `scripts/build_recipes.py`, `mkdocs.yml` (JS and any needed Markdown extensions), a new `docs/js/` script, README "Authoring" section.

### Decisions (intent review, 2026-10-29)
1 is decided; 2–5 are proposed. Please confirm or change them.

1. **Scale with cookcli at build time; the page swaps only the quantities.** The build runs `cook report recipe.cook:N` once per scale. Every quantity in the ingredient list and the steps is wrapped in a span, so each scale's output has the same spans in the same order. The build script lines the spans up across the scales and writes the 1× page with the other scales' amounts stored on each span, e.g. `<span class="qty" data-scales="250 g|500 g|1000 g|1500 g">500 g</span>`. A small JS toggle swaps each span's text. The page keeps one visible copy of the recipe, so site search, copy/paste and printing work as today, and each page grows by well under 1 KB. Measured on the current build: a recipe page is about 34 KB, or about 6 KB compressed, and the recipe content is about 2 KB of that. If the span counts differ between scales, the build fails for that recipe rather than mislabelling quantities. (Decided 2026-10-29.)
   - *Rejected: embed a full hidden copy of the ingredients and steps per scale.* It costs only about 1–2 KB compressed per page, but search would index every copy (duplicate hits with scaled amounts), and copy/paste and printing would need extra handling.
   - *Rejected: tag each quantity with its number and scale in JS.* That would allow any scale (e.g. 1.5×), but the template can't tell fixed from scalable quantities, and the JS would have to parse cookcli's formatted strings, including combined entries like `0.25 cup, 3 tbsp`.
2. 🟡 **Scale is a multiplier, not a target serving count.** It works on all recipes, not just the 9 with `servings`. Where `servings` exists, the "Serves N" line updates too (Serves 4 → Serves 8 at 2×).
3. 🟡 **Fixed set of scales: ½×, 1×, 2×, 3×.** Each scale adds one cookcli run per recipe at build time and one more value per quantity on the page. Adding a scale later means changing one list in the build script.
4. 🟡 **Show friendly fractions where they read better** (0.5 cup → ½ cup, 0.33 → ⅓). The details go in the spec, since the decimal output from cookcli is already a known issue (see the cookcli evidence under Why).
5. 🟡 **Keep the work file out of the published site.** `docs/` is MkDocs' source folder, so `docs/work/` would be published as pages. Add `exclude_docs: work/` to `mkdocs.yml` in the intent commit.
