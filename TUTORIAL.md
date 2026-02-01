# Getting Started with mkdocs-dtinth

This tutorial walks you through creating documentation for your project using **mkdocs-dtinth**, a custom MkDocs distribution with dtinth's dark theme.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed on your system
- A project with a git repository (optional, but recommended for auto-detection)

## Installation Options

Since mkdocs-dtinth is not published to PyPI, you have several ways to use it:

### Option 1: Run directly from GitHub (Recommended for one-time use)

```bash
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth init
```

### Option 2: Install the tool locally

```bash
# Install from GitHub
uv tool install git+https://github.com/dtinth/mkdocs-dtinth

# Now you can use the bare command
mkdocs-dtinth init
mkdocs-dtinth serve
```

### Option 3: Run from local source (for development)

```bash
# Clone the repo
git clone https://github.com/dtinth/mkdocs-dtinth.git
cd mkdocs-dtinth

# Install in editable mode
uv pip install -e .

# Or run without installing
uv run mkdocs-dtinth init
```

## Quick Start

### Step 1: Initialize Your Documentation

Navigate to your project directory and run the init command:

```bash
cd /path/to/your-project

# If you installed the tool locally:
mkdocs-dtinth init

# Or run directly from GitHub:
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth init
```

**What this does:**
- Creates `mkdocs.yml` with your project name (auto-detected from git remote)
- Creates a `docs/` directory
- Creates a starter `docs/index.md` file

**Example output:**
```
Project initialized in .
Run 'mkdocs-dtinth serve' to preview your documentation.
```

**Generated `mkdocs.yml`:**
```yaml
site_name: dtinth/foo
site_url: https://docs.dt.in.th/dtinth/foo/
theme:
  name: dtinth
```

**Generated `docs/index.md`:**
```markdown
# Welcome to MkDocs

This is your new documentation site.
```

### Step 2: Start the Development Server

Run the development server to preview your documentation locally:

```bash
# If installed locally:
mkdocs-dtinth serve

# Or run from GitHub:
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth serve
```

**What you'll see:**
```
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.21 seconds
INFO    -  [08:30:15] Serving on http://127.0.0.1:8000/dtinth/foo/
```

**Access your docs:**
- Open http://127.0.0.1:8000/your-project-name/ in your browser
- You'll see the dtinth dark theme with Arimo font

### Step 3: Make Changes (Hot Reload)

Edit your documentation files and see changes instantly:

```bash
# Edit the main page
vim docs/index.md
```

**Example content:**
```markdown
# Welcome to the Foo Project

This is documentation for the **Foo** project.

## Getting Started

To get started with Foo, follow these steps:

1. Install the package
2. Configure your settings
3. Run the application

## Code Example

```python
import foo

foo.run()
```
```

**Hot reload in action:**
- Save the file
- The dev server automatically rebuilds (you'll see "INFO - Building documentation..." in the terminal)
- Refresh your browser to see the updated content
- No need to restart the server!

### Step 4: Add More Pages

Create additional documentation pages:

```bash
# Create installation guide
vim docs/installation.md
```

```markdown
# Installation

## Requirements

- Python 3.8+
- pip

## Install

```bash
pip install foo
```
```

**Navigation is automatic:** MkDocs automatically adds pages to the navigation based on your file structure.

### Step 5: Build for Production

When you're ready to deploy, build the static site:

```bash
# If installed locally:
mkdocs-dtinth build

# Or run from GitHub:
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth build
```

**What this does:**
- Generates static HTML files in the `site/` directory
- Includes all CSS, JavaScript, and assets
- Ready to be deployed to any static hosting

**Output location:**
- Built files are in `./site/`
- Main entry point: `./site/index.html`
- Static assets: `./site/assets/`

**Example output:**
```
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /path/to/your-project/site
INFO    -  Documentation built in 0.23 seconds
```

**Built site structure:**
```
site/
├── index.html              # Main page
├── 404.html               # Error page
├── sitemap.xml            # SEO sitemap
├── sitemap.xml.gz         # Compressed sitemap
├── assets/                # CSS, JS, images
│   ├── stylesheets/
│   ├── javascripts/
│   └── images/
└── search/                # Search index
```

## Theme Features

Your documentation automatically uses dtinth's custom theme with:

### Colors
- **Background:** #090807 (very dark)
- **Text:** #e9e8e7 (light gray)
- **Links:** #ffffbb (light yellow)
- **Headings:** #d7fc70 (lime green)
- **Code blocks:** #252423 (dark gray)

### Typography
- **Font:** Arimo (Google Font)
- **Code:** Arimo Mono

### Dark Mode
- Theme is permanently in dark mode (no toggle)
- Optimized for readability with high contrast

## Project Structure

After initialization, your project will have:

```
your-project/
├── docs/                   # Documentation source files
│   └── index.md           # Main page
├── site/                   # Built output (generated)
├── mkdocs.yml             # Configuration file
└── .git/                  # Git repository (optional)
```

## Customization

### Changing the Site Name

Edit `mkdocs.yml`:

```yaml
site_name: My Awesome Project
site_url: https://docs.example.com/my-project/
theme:
  name: dtinth
```

### Adding Navigation

Edit `mkdocs.yml` to define your navigation structure:

```yaml
site_name: My Project
nav:
  - Home: index.md
  - Installation: installation.md
  - Usage: usage.md
  - API: api.md
theme:
  name: dtinth
```

### Adding Extra CSS

Create `docs/stylesheets/extra.css`:

```css
/* Your custom styles */
```

Then add to `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/extra.css
```

## Deployment

The built `site/` directory can be deployed to any static hosting:

- **GitHub Pages:** Push `site/` to `gh-pages` branch
- **Netlify:** Drag and drop the `site/` folder
- **Vercel:** Connect your repo and set output directory to `site/`
- **Cloudflare Pages:** Upload `site/` directory
- **S3/CloudFront:** Sync `site/` to your bucket

### GitHub Pages Example

```bash
# Build the site
mkdocs-dtinth build

# Or with uvx:
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth build

# Switch to gh-pages branch
git checkout --orphan gh-pages

# Copy site content to root
cp -r site/* .

# Commit and push
git add .
git commit -m "Deploy docs"
git push origin gh-pages
```

## Troubleshooting

### Port Already in Use

If you see "Address already in use" error:

```bash
# Kill existing process on port 8000
fuser -k 8000/tcp

# Or use a different port
mkdocs-dtinth serve --dev-addr 127.0.0.1:8001

# Or with uvx:
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth serve --dev-addr 127.0.0.1:8001
```

### Theme Not Applied

If the theme looks wrong (colors not applied):

```bash
# Clear uv cache to ensure latest theme version
uv cache clean --force

# Rebuild
mkdocs-dtinth build
```

### Changes Not Showing

If your edits don't appear:

1. Check that you saved the file
2. Look for rebuild messages in the terminal
3. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
4. Restart the dev server if needed

## Complete Workflow Example

Here's a complete example from start to finish (assuming you installed the tool locally):

```bash
# 1. Navigate to your project
cd ~/projects/my-awesome-project

# 2. Initialize docs
mkdocs-dtinth init

# 3. Start dev server (in one terminal)
mkdocs-dtinth serve

# 4. In another terminal, edit docs
vim docs/index.md
vim docs/installation.md
vim docs/usage.md

# 5. View changes at http://127.0.0.1:8000/my-awesome-project/

# 6. Build for production
mkdocs-dtinth build

# 7. Deploy the site/ directory
rsync -av site/ server:/var/www/docs/
```

If you prefer not to install locally, replace all `mkdocs-dtinth` commands with:
```bash
uvx --from git+https://github.com/dtinth/mkdocs-dtinth mkdocs-dtinth <command>
```

## Tips

- Use `tmux` or `screen` to keep the dev server running in the background
- The dev server auto-rebuilds on file changes - no need to restart
- Write documentation in Markdown - it's simple and portable
- Use code blocks with language identifiers for syntax highlighting
- Add images to `docs/` directory and reference them with relative paths

## Next Steps

- Read the [MkDocs documentation](https://www.mkdocs.org/) for more features
- Explore [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) (the base theme)
- Check out the [Markdown guide](https://www.markdownguide.org/) for syntax help
