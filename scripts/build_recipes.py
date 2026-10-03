"""Generate docs/recipes/*.md from cook/*.cook using cookcli's report command.

Usage: uv run python scripts/build_recipes.py
Set COOK to override the cookcli binary (default: `cook` on PATH).
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COOK_DIR = ROOT / "cook"
OUT_DIR = ROOT / "docs" / "recipes"
TEMPLATE = ROOT / "templates" / "recipe.md.jinja"
COOK = os.environ.get("COOK", "cook")


def render(recipe: Path) -> str:
    result = subprocess.run(
        [COOK, "report", "-t", str(TEMPLATE), "-b", str(COOK_DIR), str(recipe)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.rstrip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    recipes = sorted(COOK_DIR.glob("*.cook"))
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
