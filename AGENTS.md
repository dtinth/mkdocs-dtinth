# Agent Guidelines for mkdocs-dtinth

This document provides guidelines for AI agents working on the mkdocs-dtinth project.

## Build, Lint, and Test Commands

### Install Development Dependencies
```bash
pip install -e /config/mkdocs-dtinth
uv run --with /config/mkdocs-dtinth <command>
```

### Run the CLI
```bash
uv run --with /config/mkdocs-dtinth mkdocs-dtinth --help
uv run --with /config/mkdocs-dtinth mkdocs-dtinth serve
uv run --with /config/mkdocs-dtinth mkdocs-dtinth build
uv run --with /config/mkdocs-dtinth mkdocs-dtinth init
```

### Test the Theme
```bash
cd /tmp && rm -rf test_project && mkdir test_project && cd test_project
uv run --with /config/mkdocs-dtinth mkdocs-dtinth init
uv run --with /config/mkdocs-dtinth mkdocs-dtinth serve
```

### Build the Package
```bash
pip install build
python -m build
```

### Run a Specific Test (when tests exist)
```bash
pytest tests/test_cli.py -v
pytest tests/ -k "test_name" -v
```

### Type Checking (when enabled)
```bash
mypy mkdocs_dtinth/
```

### Linting (when enabled)
```bash
ruff check mkdocs_dtinth/
```

## Code Style Guidelines

### General Principles
- Keep code minimal and focused (per PRD: "Minimal surface area")
- Write clear, self-documenting code
- Follow the principle of least surprise

### Imports
- Use absolute imports: `from pathlib import Path`
- Group imports in this order: standard library, third-party, local
- Put all imports at the top of the file (except where lazy loading is intentional)
- Example:
  ```python
  import argparse
  import shutil
  import subprocess
  import sys
  from pathlib import Path
  ```

### Formatting
- Use 4 spaces for indentation (Python standard)
- Keep line length to 100 characters maximum
- Use blank lines to separate logical sections (2 blank lines between top-level definitions)
- No comments unless explaining non-obvious logic (per project convention)

### Types
- This project currently uses Python 3.8+ but does not require type hints
- When adding type hints, use:
  - Built-in types (`str`, `int`, `list`)
  - `typing` module for generics (`List`, `Dict`, `Optional`)
  - `pathlib.Path` for file paths
- Example with type hints:
  ```python
  from pathlib import Path
  from typing import Optional

  def get_theme_dir() -> Path:
      """Return the theme directory path."""
      pkg_dir = Path(__file__).parent
      return pkg_dir / "theme"
  ```

### Naming Conventions
- **Files**: lowercase with underscores (`cli.py`, `main_html`)
- **Functions**: snake_case (`run_serve`, `merge_mkdocs_yml`)
- **Variables**: snake_case (`user_config`, `theme_dir`)
- **Constants**: UPPER_SNAKE_CASE for true constants
- **Classes**: PascalCase (not currently used, but follow if added)

### Error Handling
- Use `sys.exit(1)` for CLI errors with messages
- Let exceptions propagate for unexpected errors
- Use `subprocess.run(..., check=True)` to catch command failures
- Validate inputs early and exit with clear messages
- Example:
  ```python
  if not config_file.exists():
      print("Error: config file not found")
      sys.exit(1)
  ```

### Project Structure
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
├── PRD.md                   # Product requirements
├── README.md                # User-facing documentation
└── AGENTS.md                # This file
```

### CLI Design
- Use `argparse` for CLI argument parsing
- Follow this pattern for subcommands:
  ```python
  parser = argparse.ArgumentParser(prog="mkdocs-dtinth")
  subparsers = parser.add_subparsers(dest="command")
  subparsers.add_parser("serve", help="Serve docs")
  ```
- Provide `--version` flag
- Pass through unknown arguments to underlying tools

### Theme Customization
- Theme config goes in `mkdocs_dtinth/theme/mkdocs.yml`
- Template overrides go in `mkdocs_dtinth/theme/overrides/`
- Use Material theme's CSS variables for styling
- Use `{% extends "base.html" %}` and override Jinja2 blocks
- Example block override:
  ```jinja2
  {% block styles %}
  {{ super() }}
  <style>...</style>
  {% endblock %}
  ```

### Configuration Merging
- Theme config is merged with user's `mkdocs.yml`
- User config takes precedence for theme settings
- Use YAML for configuration files
- Example merge pattern:
  ```python
  if "theme" in user_config:
      theme_config["theme"].update(user_config["theme"])
  theme_config.update(user_config)
  ```

### Git Workflow
- Commit message style: "Verb: description" (e.g., "Add dark mode support")
- Keep commits focused and atomic
- Update PRD.md when success criteria are met

### Testing
- When adding tests, put them in `tests/` directory
- Use `pytest` as the test runner
- Test file naming: `test_<module>.py`
- Example test:
  ```python
  def test_init_creates_docs_directory(tmp_path, monkeypatch):
      monkeypatch.chdir(tmp_path)
      run_init()
      assert (tmp_path / "docs").exists()
  ```

### Dependencies
- Add dependencies to `pyproject.toml` under `dependencies`
- Use minimal dependency set (mkdocs, pyyaml, mkdocs-material)
- Pin minimum versions where compatibility matters

### Documentation
- Update README.md for user-facing changes
- Update PRD.md when success criteria change
- Document new commands in help text
- Use docstrings for non-obvious functions

### Known Issues / Gotchas
- The `get_theme_dir()` function checks for `/config/mkdocs-dtinth` as the local source directory - this is intentional for development
- Theme files must be included via MANIFEST.in for package distribution
- The CLI merges user config with theme config, so user settings override theme defaults

## Lessons Learned (Hard-Won Knowledge)

### Configuration Merging Pitfalls

**Problem**: The initial config merge logic was broken. Theme config values were being lost because user config completely overwrote theme config instead of properly merging.

**Wrong approach**:
```python
theme_config.update(user_config)  # This loses all theme palette settings!
```

**Correct approach**:
```python
if "theme" in user_config:
    theme_config["theme"].update(user_config["theme"])
theme_config.update(user_config)
```

This preserves theme settings while still allowing user overrides at the top level.

### Color Scheme Naming

**Problem**: Using `scheme: dark` didn't work - the theme appeared in light mode.

**Root cause**: MkDocs Material theme only defines `slate` as a valid dark mode scheme name, not `dark`. The Material CSS only has `[data-md-color-scheme=slate]` selectors.

**Solution**: Always use `scheme: slate` for dark mode:
```yaml
palette:
  - scheme: slate
    primary: purple
    accent: indigo
```

### Local Development vs Installed Package

**Problem**: `uv run --with /config/mkdocs-dtinth` builds from source and installs to a temp directory. The package was picking up the installed version in `site-packages` instead of the local source.

**Solution**: The `get_theme_dir()` function detects if running from local source:
```python
def get_theme_dir():
    pkg_dir = Path(__file__).parent
    local_source = Path("/config/mkdocs-dtinth")
    if (local_source / "pyproject.toml").exists() and (
        local_source / "mkdocs_dtinth" / "theme"
    ).exists():
        return local_source / "mkdocs_dtinth" / "theme"
    return pkg_dir / "theme"
```

### CSS Customization Specificity

**Problem**: Custom CSS in the template override wasn't overriding Material theme's styles.

**Root cause**: Material theme uses very specific CSS selectors with high specificity.

**Solution**: Use highly specific selectors with `!important`:
```jinja2
{% block styles %}
{{ super() }}
<style>
[data-md-color-scheme="slate"][data-md-color-primary="purple"][data-md-color-accent="indigo"] .md-typeset a {
  color: #ffffbb !important;
}
</style>
{% endblock %}
```

Alternatively, override CSS variables at the html level:
```css
html[data-md-color-scheme="slate"] {
  --md-typeset-a-color: #ffffbb !important;
}
```

### Caching Issues

**Problem**: Changes weren't reflected immediately when testing.

**Solutions**:
1. Clear uv cache: `uv cache clean --force`
2. Clear browser/playwright cache: `playwright-cli close && playwright-cli open <url>`
3. Delete generated config: `rm /path/to/project/mkdocs.yml`
4. Delete temp files: `rm -rf /path/to/project/.mkdocs /path/to/project/site`

### extra_css Configuration

**Problem**: Using `extra_css: [styles.css]` in mkdocs.yml required the CSS file to be in the docs directory to be served correctly.

**Solutions**:
1. Put CSS in `docs/styles.css` and reference it as `extra_css: [styles.css]`
2. OR use Jinja2 template overrides with `{% block styles %}` (more reliable)

### YAML Import Location

**Problem**: Importing yaml at module level caused issues during initial setup.

**Solution**: Import yaml inside functions where it's needed:
```python
def merge_mkdocs_yml():
    user_yml = Path("mkdocs.yml")
    # ...
    import yaml  # Import here, not at top
```

### MkDocs Material JS Override Behavior

**Problem**: Even with correct theme config, Material's JavaScript was overriding the color scheme based on system `prefers-color-scheme` preference.

**Root cause**: Material includes JS that detects system preference and switches colors accordingly.

**Solution**: The issue only manifests when testing with playwright which may report light mode preference. In real browsers with dark mode preference, the slate scheme will display correctly.

### Package Data Inclusion

**Problem**: Theme files weren't included when the package was built/installed.

**Solution**: Use both MANIFEST.in and pyproject.toml package-data:
```ini
# MANIFEST.in
include mkdocs_dtinth/theme/**
```

```toml
# pyproject.toml
[tool.setuptools.package-data]
mkdocs_dtinth = ["theme/**/*"]
```

### Testing Theme Changes

**Key commands for testing theme changes**:
```bash
# Clear everything and start fresh
uv cache clean --force
cd /tmp && rm -rf test_project && mkdir test_project && cd test_project
uv run --with /config/mkdocs-dtinth mkdocs-dtinth init

# Start server
cd /tmp/test_project && tmux new-session -d -s test && tmux send-keys -t test 'uv run --with /config/mkdocs-dtinth mkdocs-dtinth serve' Enter
sleep 15

# Test with playwright (fresh browser)
playwright-cli close && playwright-cli open http://127.0.0.1:8000/
playwright-cli eval "document.body.getAttribute('data-md-color-scheme')"
playwright-cli eval "getComputedStyle(document.querySelector('h1')).color"
```

### Debugging Tips

1. **Check generated HTML**: `curl -s http://127.0.0.1:8000/ | grep "data-md-color"`
2. **Check CSS variables**: `playwright-cli eval "getComputedStyle(document.documentElement).getPropertyValue('--md-typeset-a-color')"`
3. **Check served CSS**: `curl -s http://127.0.0.1:8000/stylesheet.css` (if using extra_css)
4. **Check MkDocs config**: `cat /path/to/project/mkdocs.yml`
5. **Check server logs**: `tmux capture-pane -t <session> -p`
