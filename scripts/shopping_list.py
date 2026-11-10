"""Print a shopping list for some recipes, one item per line, and copy it to the clipboard.

Pasted into a Google Keep checklist note, each line becomes its own checkbox.

Usage:
    uv run python scripts/shopping_list.py laap cilantro-lime-rice:2
    uv run python scripts/shopping_list.py fruit-pie --extra "paper towels"

Recipes are names under cook/ (".cook" optional); ":N" scales one, as in cookcli.
Any other option (e.g. --extra, --include-optional, --pantry) is passed through
to `cook shopping-list`. Set COOK to override the cookcli binary.
"""

import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COOK_DIR = ROOT / "cook"
COOK = os.environ.get("COOK", "cook")


def fmt_number(x: float) -> str:
    """350.0 -> "350", 0.5 -> "1/2", 2.25 -> "2 1/4", 0.3333 -> "1/3"."""
    frac = Fraction(x).limit_denominator(8)
    if abs(float(frac) - x) > 1e-3:
        return f"{x:.2f}".rstrip("0").rstrip(".")
    whole, rest = divmod(frac, 1)
    if not rest:
        return str(whole)
    return f"{whole} {rest}" if whole else str(rest)


def fmt_value(value: dict) -> str:
    inner = value.get("value")
    if value.get("type") == "number" and isinstance(inner, dict):
        if isinstance(inner.get("value"), (int, float)):
            return fmt_number(inner["value"])
        # Ranges aren't used by any recipe yet; this is a best guess at the shape.
        if inner.get("type") == "range":
            r = inner["value"]
            return f"{fmt_number(r['start'])}-{fmt_number(r['end'])}"
    if isinstance(inner, (str, int, float)):
        return str(inner)
    return json.dumps(inner)  # unknown shape: show it rather than drop it


def fmt_item(item: dict) -> str:
    amounts = [
        " ".join(filter(None, [fmt_value(q["value"]), q.get("unit")]))
        for q in item["quantity"]
    ]
    return f"{item['name']}: {', '.join(amounts)}" if amounts else item["name"]


def copy_to_clipboard(text: str) -> str | None:
    for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["pbcopy"]):
        if shutil.which(cmd[0]):
            # xclip stays running to serve the clipboard; detach it from our stdout
            # so piping this script's output doesn't wait on it.
            done = subprocess.run(
                cmd,
                input=text,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if done.returncode == 0:
                return cmd[0]
    return None


def resolve(arg: str) -> str:
    """Make a recipe given as a path (e.g. cook/laap.cook:2) absolute, since cook runs from cook/."""
    path, sep, scale = arg.rpartition(":") if ":" in arg else (arg, "", "")
    if not arg.startswith("-") and Path(path).is_file():
        return str(Path(path).resolve()) + sep + scale
    return arg


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    argv = [resolve(a) for a in argv]
    result = subprocess.run(
        [COOK, "shopping-list", "--plain", "-f", "json", *argv],
        capture_output=True,
        text=True,
        cwd=COOK_DIR,
    )
    # Pass cookcli's warnings through (e.g. a sub-recipe that couldn't be scaled),
    # minus the one about aisles, which --plain makes irrelevant.
    for line in result.stderr.splitlines():
        if "no aisle configuration" not in line:
            print(line, file=sys.stderr)
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr, end="")
        return result.returncode

    text = "\n".join(fmt_item(item) for item in json.loads(result.stdout))
    print(text)
    tool = copy_to_clipboard(text)
    print(
        f"\n(copied to clipboard via {tool})"
        if tool
        else "\n(no clipboard tool found; copy the list above)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
