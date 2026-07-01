# Contributing

Thanks for helping improve `agent-repo-kit`.

## Good Contributions

- New templates for common project types
- Better generated README or AGENTS.md defaults
- Better tests for generated projects
- More CI examples
- Safer overwrite behavior

## Before Opening a PR

Run:

```bash
python -m unittest discover -s tests
python -m agent_repo_kit list
```

If you change a template, add or update tests that generate it.

## Template Rules

Generated projects should be:

- Small
- Launch-ready
- Agent-friendly
- Dependency-light
- Easy to understand in the first README screen
