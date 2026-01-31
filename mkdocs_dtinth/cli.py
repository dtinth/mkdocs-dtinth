import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="mkdocs-dtinth")
    parser.add_argument(
        "--version",
        action="version",
        version=f"mkdocs-dtinth {__import__('mkdocs_dtinth').__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("serve", help="Serve documentation with custom theme")
    subparsers.add_parser("build", help="Build documentation with custom theme")
    init_parser = subparsers.add_parser("init", help="Create a new project skeleton")

    args = parser.parse_args()

    if args.command == "serve":
        run_serve()
    elif args.command == "build":
        run_build()
    elif args.command == "init":
        run_init()
    else:
        parser.print_help()


def get_theme_dir():
    pkg_dir = Path(__file__).parent
    local_source = Path("/config/mkdocs-dtinth")
    if (local_source / "pyproject.toml").exists() and (
        local_source / "mkdocs_dtinth" / "theme"
    ).exists():
        return local_source / "mkdocs_dtinth" / "theme"
    return pkg_dir / "theme"


def merge_mkdocs_yml():
    user_yml = Path("mkdocs.yml")
    theme_yml = get_theme_dir() / "mkdocs.yml"

    import yaml

    if theme_yml.exists():
        with open(theme_yml) as f:
            theme_config = yaml.safe_load(f) or {}
    else:
        theme_config = {}

    if user_yml.exists():
        with open(user_yml) as f:
            user_config = yaml.safe_load(f) or {}
    else:
        user_config = {}

    if "theme" in user_config:
        theme_config["theme"].update(user_config["theme"])
    theme_config.update(user_config)

    return theme_config


def write_merged_config(config):
    with open("mkdocs.yml", "w") as f:
        import yaml

        yaml.dump(config, f, default_flow_style=False)


def run_serve():
    config = merge_mkdocs_yml()
    config["theme"]["custom_dir"] = str(get_theme_dir() / "overrides")
    write_merged_config(config)
    subprocess.run(["mkdocs", "serve"] + sys.argv[2:], check=True)


def run_build():
    config = merge_mkdocs_yml()
    config["theme"]["custom_dir"] = str(get_theme_dir() / "overrides")
    write_merged_config(config)
    subprocess.run(["mkdocs", "build"] + sys.argv[2:], check=True)


def run_init():
    target = Path(".") if Path(".").resolve().name != "mkdocs-dtinth" else Path("..")

    if (target / "mkdocs.yml").exists():
        print("mkdocs.yml already exists in target directory")
        sys.exit(1)

    shutil.copy(get_theme_dir() / "mkdocs.yml", target / "mkdocs.yml")

    docs_dir = target / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "index.md").write_text(
        "# Welcome to MkDocs\n\nThis is your new documentation site.\n"
    )

    print(f"Project initialized in {target}")
    print("Run 'mkdocs-dtinth serve' to preview your documentation.")
