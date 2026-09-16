# New templates (v0.2.0)

```bash
agent-repo-kit create my-cli --template typescript-cli
cd my-cli
npm install
npm test
node dist/cli.js Ada
```

The TypeScript template has a strict compiler configuration, a CLI entry point, Node
tests, package metadata and CI. It requires Node.js 22+. Generation is offline; npm
install is an explicit later step. Commit the lockfile and switch CI to npm ci after
the first install.

```bash
agent-repo-kit create useful-links --template awesome-list
cd useful-links
python scripts/generate_readme.py
python scripts/validate_catalog.py
```

The catalog starts empty. Add objects with name, url and summary to data/tools.json.
Validation rejects duplicate names, missing fields and invalid URLs. CI verifies
that the README matches the structured data. The template includes contribution,
license, security and agent guidance. Existing non-empty destinations remain protected
unless --force is explicitly supplied.
