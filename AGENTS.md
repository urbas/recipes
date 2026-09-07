# Development

Use `mkdocs serve -a 10.1.0.1:28000` to show the rendered web page.

# Nix environment

This repo uses a Nix flake (`flake.nix`) with direnv always active. Assume all
tools are in PATH. If a CLI tool or Python package is missing, add it to
`flake.nix` and use `nix develop --command` to use it.

# Pre-commit hooks

This repo uses `prek` to manage pre-commit hooks (configured in
`.pre-commit-config.yaml`). If the hooks are not installed, install them with
`prek install`.

If a commit fails because a pre-commit hook cannot resolve a dependency recently
added to `flake.nix`, run:
`nix develop --command bash -c 'git add -A && git commit -m "..."'`

# Git

- Assume the working directory is the repo root; no need to use `git -C`.
- When force-pushing, prefer `--force-with-lease` over `--force`.
- Use simple single-line commit messages.
