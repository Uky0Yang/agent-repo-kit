import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_repo_kit.generator import CreateOptions, create_project


class ExtraTemplateTests(unittest.TestCase):
    def test_typescript_manifest_and_test_command(self):
        with tempfile.TemporaryDirectory() as directory:
            result = create_project(CreateOptions('demo', 'typescript-cli', Path(directory), 'A "quoted" description', 'Tester', '2026'))
            package = json.loads((result.project_dir / 'package.json').read_text())
            self.assertEqual(package['scripts']['test'], 'npm run build && node --test tests/*.test.mjs')
            self.assertEqual(package['description'], 'A "quoted" description')

    def test_awesome_generated_catalog_is_valid_and_rejects_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = create_project(CreateOptions('links', 'awesome-list', Path(directory), 'Useful links', 'Tester', '2026')).project_dir
            subprocess.run([sys.executable, 'scripts/generate_readme.py'], cwd=root, check=True, capture_output=True)
            subprocess.run([sys.executable, 'scripts/validate_catalog.py'], cwd=root, check=True, capture_output=True)
            data = root / 'data/tools.json'
            item = {'name': 'Example', 'url': 'https://example.com', 'summary': 'Example project'}
            data.write_text(json.dumps([item, item]), encoding='utf-8')
            invalid = subprocess.run([sys.executable, 'scripts/validate_catalog.py'], cwd=root, capture_output=True)
            self.assertNotEqual(invalid.returncode, 0)
