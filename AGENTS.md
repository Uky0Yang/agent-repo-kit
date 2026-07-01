# Agent Instructions

## Purpose

Maintain `agent-repo-kit`, a dependency-free Python CLI that scaffolds launch-ready, AI-agent-friendly open-source repositories.

## Scope

These instructions apply to generator code, templates, tests, documentation, and GitHub workflow files in this repository.

## Commands

Run these checks before publishing:

```bash
python -m unittest discover -s tests
python -m agent_repo_kit list
```

## Safety

- Do not add network calls to the default generation path.
- Do not add telemetry.
- Do not overwrite user files unless `--force` is explicitly used.
- Do not include secrets, tokens, or private data in generated templates.

## Style

- Prefer standard-library Python.
- Keep generated repositories small and readable.
- Add tests for every new template.
- Keep template output deterministic.
