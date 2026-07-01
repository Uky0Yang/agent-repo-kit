from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

from . import __version__
from .generator import CreateOptions, available_templates, create_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-repo-kit",
        description="Scaffold launch-ready, AI-agent-friendly open-source repositories.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List available templates.")
    list_parser.set_defaults(func=handle_list)

    create_parser = subparsers.add_parser("create", help="Create a new repository scaffold.")
    create_parser.add_argument("name", help="Project directory and display name.")
    create_parser.add_argument("--template", choices=sorted(available_templates()), default="python-cli")
    create_parser.add_argument("--output-dir", default=".", help="Directory where the project folder should be created.")
    create_parser.add_argument("--description", default="An agent-ready open-source project.")
    create_parser.add_argument("--author", default="Ukyo")
    create_parser.add_argument("--year", default=str(datetime.now().year))
    create_parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    create_parser.add_argument("--dry-run", action="store_true", help="Show files without writing them.")
    create_parser.set_defaults(func=handle_create)

    return parser


def handle_list(_args: argparse.Namespace) -> int:
    for name, template in sorted(available_templates().items()):
        print(f"{name}\t{template.description}")
    return 0


def handle_create(args: argparse.Namespace) -> int:
    result = create_project(
        CreateOptions(
            name=args.name,
            template=args.template,
            output_dir=Path(args.output_dir),
            description=args.description,
            author=args.author,
            year=args.year,
            force=args.force,
            dry_run=args.dry_run,
        )
    )
    action = "Would create" if result.dry_run else "Created"
    print(f"{action} {result.project_dir}")
    for file in result.files:
        print(f"  - {file}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except (FileExistsError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
