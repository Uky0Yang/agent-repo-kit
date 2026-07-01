from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path

from agent_repo_kit.cli import main


class CliTests(unittest.TestCase):
    def test_list_templates(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            code = main(["list"])

        self.assertEqual(code, 0)
        self.assertIn("python-cli", output.getvalue())
        self.assertIn("agent-docs", output.getvalue())

    def test_create_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = StringIO()
            with redirect_stdout(output):
                code = main(["create", "demo", "--output-dir", directory, "--dry-run"])

            self.assertEqual(code, 0)
            self.assertIn("Would create", output.getvalue())
            self.assertFalse((Path(directory) / "demo").exists())

    def test_create_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = StringIO()
            with redirect_stdout(output):
                code = main(["create", "demo", "--output-dir", directory, "--description", "Demo"])

            self.assertEqual(code, 0)
            self.assertTrue((Path(directory) / "demo" / "README.md").exists())

    def test_bad_template_returns_error(self) -> None:
        error = StringIO()
        with redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                main(["create", "demo", "--template", "missing"])

        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
