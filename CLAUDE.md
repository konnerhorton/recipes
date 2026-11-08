# Notes for Claude

## Recipe front matter: `yield`

Follow the Cooklang docs (`COOKLANG.md`), not the parser, for `yield`: it may carry a unit, written as `yield: 2%cups`.

cookcli (checked on 0.39.0) only accepts a bare number for `servings` / `serves` / `yield`. Anything else, including the docs' own `15 cups worth` example, raises `Unsupported value for key: 'yield'`. That is only a warning: the value is kept as text and still displayed. Don't "fix" these warnings by stripping units. The assumption is that the parser will catch up with the docs (tracked in `TODO.md`).
