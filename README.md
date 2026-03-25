# mkdocs-dtinth

A reusable MkDocs distribution with dtinth's custom dark theme, designed for use across multiple projects via `uvx`.

## Commands

```bash
# Run directly from GitHub
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth build

# Install dependencies
uv sync

# Develop and test commands locally
uv run mkdocs-dtinth init    # Initialize a new project
uv run mkdocs-dtinth serve   # Serve current directory as docs (or Cmd+Shift+B)
uv run mkdocs-dtinth build   # Build for production

# Install as global command
uv tool install -e . --reinstall

# Use the commands in other projects
mkdocs-dtinth init
mkdocs-dtinth serve
```

## License

MIT
