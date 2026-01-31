import argparse
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

    serve_parser = subparsers.add_parser(
        "serve", help="Serve documentation with custom theme"
    )
    serve_parser.add_argument(
        "--dev-addr",
        type=str,
        help="IP address and port to serve (e.g., 0.0.0.0:8000)",
    )
    subparsers.add_parser("build", help="Build documentation with custom theme")
    subparsers.add_parser("init", help="Create a new project skeleton")

    args = parser.parse_args()

    if args.command == "serve":
        run_serve(args)
    elif args.command == "build":
        run_build()
    elif args.command == "init":
        run_init()
    else:
        parser.print_help()


def get_theme_dir():
    pkg_dir = Path(__file__).parent / "theme"
    local_source = Path("/config/mkdocs-dtinth")
    if (local_source / "pyproject.toml").exists() and (
        local_source / "mkdocs_dtinth" / "theme"
    ).exists():
        return local_source / "mkdocs_dtinth" / "theme"
    return pkg_dir


def run_serve(args):
    cmd = ["mkdocs", "serve"]
    if args.dev_addr:
        cmd.extend(["--dev-addr", args.dev_addr])
    subprocess.run(cmd, check=True)


def run_build():
    subprocess.run(["mkdocs", "build"] + sys.argv[2:], check=True)


def run_init():
    target = Path(".") if Path(".").resolve().name != "mkdocs-dtinth" else Path("..")

    if (target / "mkdocs.yml").exists():
        print("mkdocs.yml already exists in target directory")
        sys.exit(1)

    project_name = get_project_name(target)
    site_url = f"https://docs.dt.in.th/{project_name}/"

    config = {
        "site_name": project_name,
        "site_url": site_url,
        "theme": {"name": "dtinth"},
    }

    with open(target / "mkdocs.yml", "w") as f:
        import yaml

        yaml.dump(config, f, default_flow_style=False)

    docs_dir = target / "docs"
    docs_dir.mkdir(exist_ok=True)

    index_file = docs_dir / "index.md"
    if not index_file.exists():
        index_file.write_text(
            "# Welcome to MkDocs\n\nThis is your new documentation site.\n"
        )

    print(f"Project initialized in {target}")
    print("Run 'mkdocs-dtinth serve' to preview your documentation.")


def get_project_name(target):
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=target,
            capture_output=True,
            text=True,
            check=True,
        )
        remote_url = result.stdout.strip()
        if remote_url.startswith("https://"):
            path = remote_url.replace("https://", "").split("/", 1)[1]
            if path.endswith(".git"):
                path = path[:-4]
            return path
        elif remote_url.startswith("git@"):
            path = remote_url.split(":", 1)[1]
            if path.endswith(".git"):
                path = path[:-4]
            return path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return target.resolve().name
