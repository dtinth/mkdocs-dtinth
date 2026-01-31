# mkdocs-dtinth

A reusable MkDocs distribution with dtinth's custom dark theme, designed for use across multiple projects via `uvx`.

## Features

- **Dark Mode Default**: Uses Material theme's "slate" color scheme with purple primary and indigo accent
- **Custom Colors**: Light yellow (`#ffffbb`) link colors and light green (`#d7fc70`) headings
- **Minimal CLI**: Only `serve`, `build`, and `init` commands
- **Config Merging**: Your `mkdocs.yml` settings override theme defaults
- **uvx Support**: Run without installation via `uvx mkdocs-dtinth`

## Quick Start

```bash
# Serve current directory as docs (using uvx)
uvx mkdocs-dtinth serve

# Initialize a new project
uvx mkdocs-dtinth init

# Build for production
uvx mkdocs-dtinth build
```

## Installation

### For Users (via uvx)
```bash
# Run directly without installation
uvx --from git+https://github.com/dtinth/mkdocs-dtinth serve
uvx --from git+https://github.com/dtinth/mkdocs-dtinth init
uvx --from git+https://github.com/dtinth/mkdocs-dtinth build
```

### For Development
```bash
pip install -e /config/mkdocs-dtinth
```

Or with uv:
```bash
uv run --with /config/mkdocs-dtinth mkdocs-dtinth <command>
```

## Theme Customization

The default theme uses:
- **Scheme**: slate (dark mode)
- **Primary color**: purple
- **Accent color**: indigo
- **Link color**: #ffffbb
- **Heading colors**: #d7fc70

### Override Colors in Your Project

Create a `mkdocs.yml` in your project directory:

```yaml
site_name: My Docs
theme:
  palette:
    - scheme: slate
      primary: purple
      accent: indigo
```

Or add custom CSS in `docs/styles.css`:

```css
[data-md-color-scheme="slate"] .md-typeset a {
  color: #ffffbb !important;
}
[data-md-color-scheme="slate"] .md-typeset h1,
[data-md-color-scheme="slate"] .md-typeset h2 {
  color: #d7fc70 !important;
}
```

## Project Structure

```
mkdocs-dtinth/
├── mkdocs_dtinth/
│   ├── __init__.py          # Package root, defines __version__
│   ├── __main__.py          # Entry point for `python -m mkdocs_dtinth`
│   ├── cli.py               # Main CLI logic
│   └── theme/               # Custom theme files
│       ├── mkdocs.yml       # Theme configuration
│       └── overrides/       # Jinja2 template overrides
│           └── main.html
├── pyproject.toml           # Package metadata and dependencies
├── MANIFEST.in              # Non-code files to include
├── README.md                # This file
└── AGENTS.md                # Guidelines for AI agents
```

## Development

See [AGENTS.md](AGENTS.md) for:
- Build, lint, and test commands
- Code style guidelines
- Project conventions
- Lessons learned (common pitfalls)

## References

- [MkDocs Theme Development](https://www.mkdocs.org/user-guide/custom-themes/)
- [Material Customization](https://squidfunk.github.io/mkdocs-material/customization/)
- [Python Packaging](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## License

MIT
