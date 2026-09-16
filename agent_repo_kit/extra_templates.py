"""Small executable scaffolds; generation itself makes no network calls."""

TYPESCRIPT_FILES = {
    '.gitignore': 'node_modules/\ndist/\n.env\n*.log\n',
    'package.json': '''{
  "name": "{{package_name}}",
  "version": "0.1.0",
  "description": {{description_json}},
  "license": "MIT",
  "type": "module",
  "engines": {"node": ">=22"},
  "bin": {"{{package_name}}": "dist/cli.js"},
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "test": "npm run build && node --test tests/*.test.mjs"
  },
  "devDependencies": {"typescript": "7.0.2", "@types/node": "22.20.3"}
}
''',
    'tsconfig.json': '''{
  "compilerOptions": {
    "target": "ES2022", "module": "NodeNext", "moduleResolution": "NodeNext",
    "strict": true, "outDir": "dist", "rootDir": "src", "declaration": true, "types": ["node"]
  },
  "include": ["src/**/*.ts"]
}
''',
    'src/greet.ts': '''export function greet(name: string): string {
  if (!name.trim()) throw new Error("Name must not be empty");
  return `Hello, ${name}!`;
}
''',
    'src/cli.ts': '''#!/usr/bin/env node
import { greet } from "./greet.js";

try {
  console.log(greet(process.argv[2] ?? "world"));
} catch (error) {
  console.error(error instanceof Error ? error.message : "Invalid input");
  process.exitCode = 1;
}
''',
    'tests/greet.test.mjs': '''import { test } from 'node:test';
import assert from 'node:assert/strict';
import { greet } from '../dist/greet.js';
test('greets a name', () => assert.equal(greet('Ada'), 'Hello, Ada!'));
test('rejects blank names', () => assert.throws(() => greet(' ')));
''',
    'README.md': '''# {{project_name}}

{{description}}

## Why

A small TypeScript CLI with a tested entry point. Replace the greeting with your use case.

## Install and use

Requires Node.js 22+.

```bash
npm install
npm test
node dist/cli.js Ada
```

Commit the generated package-lock.json after the first install, then use npm ci in CI.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run npm test before submitting changes.

## License

MIT
''',
    '.github/workflows/ci.yml': '''name: Test
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm install --ignore-scripts
      - run: npm test
''',
}

AWESOME_FILES = {
    'data/tools.json': '[]\n',
    'README.md': '''# {{project_name}}

{{description}}

## Why

A curated list with structured data and reproducible validation.

## Usage

Add projects to data/tools.json with name, url and summary. Include only maintained
projects with public documentation and a clear use case. Disclose self-promotion.

<!-- BEGIN GENERATED -->

| Project | Summary |
| --- | --- |

<!-- END GENERATED -->

## Contributing

Run python scripts/generate_readme.py and python scripts/validate_catalog.py.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
''',
    'scripts/validate_catalog.py': '''import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def load():
    tools = json.loads((ROOT / "data/tools.json").read_text(encoding="utf-8"))
    if not isinstance(tools, list):
        raise ValueError("Catalog must be a list")
    seen = set()
    for item in tools:
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in ("name", "url", "summary")):
            raise ValueError("Each entry needs name, url and summary")
        if item["name"].casefold() in seen:
            raise ValueError("Duplicate name")
        seen.add(item["name"].casefold())
        parsed = urlparse(item["url"])
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("Expected an HTTP(S) URL")
    return tools

if __name__ == "__main__":
    print(f"Validated {len(load())} projects")
''',
    'scripts/generate_readme.py': '''from validate_catalog import ROOT, load
import html

path = ROOT / "README.md"
text = path.read_text(encoding="utf-8")
start, end = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"
def escape(value):
    return html.escape(value).replace("|", "&#124;").replace("\\n", " ")
rows = ["| Project | Summary |", "| --- | --- |"]
for item in load():
    rows.append(f"| <a href=\\"{escape(item['url'])}\\">{escape(item['name'])}</a> | {escape(item['summary'])} |")
path.write_text(text[:text.index(start) + len(start)] + "\\n\\n" + "\\n".join(rows) + "\\n\\n" + text[text.index(end):], encoding="utf-8", newline="\\n")
''',
    '.github/workflows/ci.yml': '''name: Validate catalog
on: [push, pull_request]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python scripts/validate_catalog.py
      - run: python scripts/generate_readme.py
      - run: git diff --exit-code -- README.md
''',
}
