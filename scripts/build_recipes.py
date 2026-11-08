"""Generate docs/recipes/*.md from cook/*.cook using cookcli's report command.

Usage: uv run python scripts/build_recipes.py
Set COOK to override the cookcli binary (default: `cook` on PATH).
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COOK_DIR = ROOT / "cook"
OUT_DIR = ROOT / "docs" / "recipes"
TEMPLATE = ROOT / "templates" / "recipe.md.jinja"
COOK = os.environ.get("COOK", "cook")


def optional_indices(recipe: Path) -> list[int]:
    """Indices into the recipe's ingredients that are marked optional (`@?name{}`).

    `cook report` doesn't expose the optional modifier to templates, but
    `cook recipe -f json` does, in the same ingredient order.
    """
    result = subprocess.run(
        [COOK, "recipe", "-f", "json", str(recipe)],
        capture_output=True,
        text=True,
        cwd=COOK_DIR,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    ingredients = json.loads(result.stdout)["ingredients"]
    return [i for i, ing in enumerate(ingredients) if "OPT" in ing.get("modifiers", "")]


def render(recipe: Path) -> str:
    # Hand per-recipe data to the template through a throwaway datastore;
    # the template reads it with db("optional.indices").
    with tempfile.TemporaryDirectory() as datastore:
        (Path(datastore) / "optional.yml").write_text(
            f"indices: {json.dumps(optional_indices(recipe))}\n"
        )
        result = subprocess.run(
            [COOK, "report", "-t", str(TEMPLATE), "-d", datastore,
             "-b", str(COOK_DIR), str(recipe)],
            capture_output=True,
            text=True,
        )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.rstrip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Files starting with "_" (e.g. _template.cook) are not recipes.
    recipes = sorted(r for r in COOK_DIR.glob("*.cook") if not r.name.startswith("_"))
    failures = []
    for recipe in recipes:
        try:
            (OUT_DIR / f"{recipe.stem}.md").write_text(render(recipe))
        except RuntimeError as err:
            failures.append(recipe.name)
            print(f"FAILED {recipe.name}\n{err}", file=sys.stderr)

    # Remove pages whose .cook source was deleted or renamed.
    stems = {r.stem for r in recipes}
    for page in OUT_DIR.glob("*.md"):
        if page.stem not in stems:
            page.unlink()
            print(f"removed stale {page.relative_to(ROOT)}")

    print(f"built {len(recipes) - len(failures)}/{len(recipes)} recipes")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
