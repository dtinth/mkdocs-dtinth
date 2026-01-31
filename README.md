# mkdocs-dtinth

A reusable MkDocs distribution with dtinth's custom dark theme, designed for use across multiple projects via `uvx`.

## Usage

```bash
# Run directly without installation
uvx mkdocs-dtinth init    # Initialize a new project
uvx mkdocs-dtinth serve   # Serve current directory as docs
uvx mkdocs-dtinth build   # Build for production
```

Or install from GitHub:

```bash
uvx --from git+https://github.com/dtinth/mkdocs-dtinth init
```

## Development

```bash
pip install -e /config/mkdocs-dtinth
```

See [AGENTS.md](AGENTS.md) for build commands and guidelines.

## License

MIT
