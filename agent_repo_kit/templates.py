from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    name: str
    description: str
    files: dict[str, str]


COMMON_FILES = {
    ".gitattributes": "* text=auto eol=lf\n",
    ".gitignore": "__pycache__/\n.pytest_cache/\n.venv/\nvenv/\ndist/\nbuild/\n*.egg-info/\n*.pyc\n.DS_Store\nThumbs.db\n",
    "LICENSE": """MIT License

Copyright (c) {{year}} {{author}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    "CONTRIBUTING.md": """# Contributing

Thanks for helping improve `{{project_name}}`.

## Setup

```bash
{{setup_command}}
```

## Checks

```bash
{{check_command}}
```

## Pull Requests

- Keep changes focused.
- Add or update tests when behavior changes.
- Update documentation when user-facing behavior changes.
""",
    "SECURITY.md": """# Security Policy

Please do not open public issues for sensitive vulnerabilities.

Report security issues through GitHub private vulnerability reporting if enabled, or open a minimal issue asking for a maintainer contact path without disclosing exploit details.
""",
    "CODE_OF_CONDUCT.md": """# Code of Conduct

## Expected Behavior

- Be direct and respectful.
- Keep discussions technical and actionable.
- Avoid harassment, personal attacks, or discriminatory language.

## Enforcement

Maintainers may remove comments or contributions that violate this code of conduct.
""",
    "ROADMAP.md": """# Roadmap

## Near Term

- Improve examples
- Add more tests
- Publish a first release

## Mid Term

- Add more integrations
- Improve documentation

## Non-Goals

- No misleading adoption or star claims
""",
    "AGENTS.md": """# Agent Instructions

## Purpose

Maintain `{{project_name}}`: {{description}}

## Scope

These instructions apply to code, tests, documentation, and GitHub workflow files in this repository.

## Commands

Run these checks before publishing:

```bash
{{check_command}}
```

## Safety

- Do not commit secrets, tokens, cookies, private keys, or local environment files.
- Do not add network calls to default checks unless they are explicitly documented.
- Keep generated files out of commits unless they are part of the published artifact.

## Style

- Keep changes small and reviewable.
- Prefer clear names and deterministic behavior.
- Update tests when behavior changes.
""",
    ".github/PULL_REQUEST_TEMPLATE.md": """## Summary

- 

## Checks

- [ ] `{{check_command}}`

## Notes
""",
    ".github/ISSUE_TEMPLATE/feature_request.yml": """name: Feature request
description: Suggest an improvement
title: "[Feature] "
labels:
  - enhancement
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem should this solve?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposal
      description: What should change?
    validations:
      required: true
""",
}


PYTHON_CLI_FILES = {
    "README.md": """# {{project_name}}

{{description}}

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
{{package_name}} --help
{{package_name}} hello
```

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m {{module_name}} hello
```

## License

MIT
""",
    "pyproject.toml": """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{{package_name}}"
version = "0.1.0"
description = "{{description}}"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
  { name = "{{author}}" }
]
dependencies = []

[project.scripts]
{{package_name}} = "{{module_name}}.cli:main"
""",
    "{{module_name}}/__init__.py": "\"\"\"{{description}}\"\"\"\n\n__version__ = \"0.1.0\"\n",
    "{{module_name}}/__main__.py": "from .cli import main\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n",
    "{{module_name}}/cli.py": """from __future__ import annotations

import argparse
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="{{package_name}}", description="{{description}}")
    parser.add_argument("command", nargs="?", default="hello", choices=("hello",))
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "hello":
        print("{{project_name}} is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
""",
    "tests/test_cli.py": """from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO

from {{module_name}}.cli import main


class CliTests(unittest.TestCase):
    def test_hello(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            code = main(["hello"])
        self.assertEqual(code, 0)
        self.assertIn("ready", output.getvalue())


if __name__ == "__main__":
    unittest.main()
""",
    ".github/workflows/ci.yml": """name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m pip install -e .
      - run: python -m unittest discover -s tests
      - run: python -m {{module_name}} hello
""",
}


AGENT_DOCS_FILES = {
    "README.md": """# {{project_name}}

{{description}}

## What This Contains

- Agent instructions
- Workflow playbooks
- Review checklists
- Safety notes

## Usage

Copy the relevant Markdown files into your project and adapt them to your stack.

## Development

```bash
python scripts/validate_docs.py
```

## License

MIT
""",
    "playbooks/code-review.md": """# Code Review Playbook

## Goal

Find correctness, security, test, and maintainability issues before merge.

## Checklist

- Does the change match the request?
- Are tests present for behavior changes?
- Are secrets or credentials absent?
- Is error handling clear?
""",
    "playbooks/release.md": """# Release Playbook

## Checklist

- Tests pass
- README is current
- Changelog or release notes are ready
- Version is updated where applicable
""",
    "scripts/validate_docs.py": """from pathlib import Path


def main() -> int:
    required = ["README.md", "AGENTS.md", "playbooks/code-review.md", "playbooks/release.md"]
    missing = [path for path in required if not Path(path).exists()]
    if missing:
        print("Missing required files:", ", ".join(missing))
        return 1
    print("Documentation scaffold is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    ".github/workflows/ci.yml": """name: Validate docs

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python scripts/validate_docs.py
""",
}


TEMPLATES = {
    "python-cli": Template("python-cli", "Dependency-free Python CLI package with tests and CI.", {**COMMON_FILES, **PYTHON_CLI_FILES}),
    "agent-docs": Template("agent-docs", "Markdown playbook repository for AI coding agents and teams.", {**COMMON_FILES, **AGENT_DOCS_FILES}),
}
