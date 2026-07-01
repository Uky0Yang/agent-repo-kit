# agent-repo-kit

Scaffold launch-ready, AI-agent-friendly open-source repositories.

`agent-repo-kit` is a dependency-free Python CLI that creates repositories with the boring but important launch pieces already in place: README, AGENTS.md, license, CI, tests, contributing guide, security policy, issue/PR templates, roadmap, `.gitignore`, and `.gitattributes`.

## Why

Recent high-growth developer projects are clustered around AI coding agents, skills, context engineering, templates, and developer automation. A common gap remains: starting a repo that is ready for both humans and coding agents still takes repetitive setup.

This tool turns that setup into one command.

## Install

From this repository:

```bash
python -m pip install -e .
```

Or run without installing:

```bash
python -m agent_repo_kit list
```

## Usage

List templates:

```bash
agent-repo-kit list
```

Create a Python CLI project:

```bash
agent-repo-kit create my-tool \
  --template python-cli \
  --description "A useful developer CLI" \
  --author "Your Name"
```

Create an agent playbooks/docs repository:

```bash
agent-repo-kit create agent-playbooks \
  --template agent-docs \
  --description "Reusable AI coding agent playbooks"
```

Preview without writing files:

```bash
agent-repo-kit create my-tool --dry-run
```

## Templates

### `python-cli`

A standard-library Python CLI package with:

- `pyproject.toml`
- importable package
- console script
- unit test
- GitHub Actions CI across Python 3.10, 3.11, and 3.12
- launch-ready repo files

### `agent-docs`

A Markdown repository for reusable AI coding agent playbooks with:

- AGENTS.md
- code review playbook
- release playbook
- docs validation script
- GitHub Actions CI
- launch-ready repo files

## Generated Repository Standards

Every template includes:

- README
- AGENTS.md
- MIT license
- Contributing guide
- Security policy
- Code of conduct
- Roadmap
- GitHub Actions workflow
- Issue template
- Pull request template
- `.gitignore`
- `.gitattributes`

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m agent_repo_kit list
```

## License

MIT
