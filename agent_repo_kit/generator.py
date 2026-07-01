from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Mapping

from .templates import TEMPLATES, Template


@dataclass(frozen=True)
class CreateOptions:
    name: str
    template: str
    output_dir: Path
    description: str
    author: str
    year: str
    force: bool = False
    dry_run: bool = False


@dataclass(frozen=True)
class CreateResult:
    project_dir: Path
    files: list[str]
    dry_run: bool


def available_templates() -> dict[str, Template]:
    return TEMPLATES


def create_project(options: CreateOptions) -> CreateResult:
    if options.template not in TEMPLATES:
        raise ValueError(f"Unknown template: {options.template}")

    project_dir = (options.output_dir / options.name).resolve()
    context = build_context(options)
    files = render_files(TEMPLATES[options.template], context)
    planned = sorted(files)

    if project_dir.exists() and any(project_dir.iterdir()) and not options.force:
        raise FileExistsError(f"Target directory is not empty: {project_dir}")

    if options.dry_run:
        return CreateResult(project_dir, planned, True)

    project_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, content in files.items():
        path = project_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not options.force:
            raise FileExistsError(f"File already exists: {path}")
        path.write_text(content, encoding="utf-8", newline="\n")

    return CreateResult(project_dir, planned, False)


def build_context(options: CreateOptions) -> dict[str, str]:
    package_name = slugify(options.name)
    module_name = package_name.replace("-", "_")
    return {
        "project_name": options.name,
        "package_name": package_name,
        "module_name": module_name,
        "description": options.description,
        "author": options.author,
        "year": options.year,
        "setup_command": setup_command(options.template),
        "check_command": check_command(options.template, module_name),
    }


def setup_command(template: str) -> str:
    if template == "python-cli":
        return "python -m pip install -e ."
    return "python scripts/validate_docs.py"


def check_command(template: str, module_name: str) -> str:
    if template == "python-cli":
        return f"python -m unittest discover -s tests && python -m {module_name} hello"
    return "python scripts/validate_docs.py"


def render_files(template: Template, context: Mapping[str, str]) -> dict[str, str]:
    output: dict[str, str] = {}
    for raw_path, raw_content in template.files.items():
        path = render_string(raw_path, context)
        content = render_string(raw_content, context)
        output[path] = content
    return output


def render_string(value: str, context: Mapping[str, str]) -> str:
    rendered = value
    for key, replacement in context.items():
        rendered = rendered.replace("{{" + key + "}}", replacement)
    return rendered


def slugify(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", name.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    if not slug:
        raise ValueError("Project name must contain at least one alphanumeric character.")
    return slug
