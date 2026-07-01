from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_repo_kit.generator import CreateOptions, create_project, slugify


class GeneratorTests(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(slugify("My Cool Tool"), "my-cool-tool")
        self.assertEqual(slugify("repo_context.card"), "repo_context.card")

    def test_create_python_cli_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = create_project(
                CreateOptions(
                    name="demo-tool",
                    template="python-cli",
                    output_dir=Path(directory),
                    description="Demo CLI",
                    author="Tester",
                    year="2026",
                )
            )
            root = result.project_dir

            self.assertTrue((root / "pyproject.toml").exists())
            self.assertTrue((root / "demo_tool" / "cli.py").exists())
            self.assertTrue((root / "tests" / "test_cli.py").exists())
            self.assertIn("README.md", result.files)

    def test_create_agent_docs_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = create_project(
                CreateOptions(
                    name="agent-playbooks",
                    template="agent-docs",
                    output_dir=Path(directory),
                    description="Agent playbooks",
                    author="Tester",
                    year="2026",
                )
            )

            self.assertTrue((result.project_dir / "playbooks" / "code-review.md").exists())
            self.assertTrue((result.project_dir / "scripts" / "validate_docs.py").exists())

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = create_project(
                CreateOptions(
                    name="dry-run-demo",
                    template="python-cli",
                    output_dir=Path(directory),
                    description="Demo",
                    author="Tester",
                    year="2026",
                    dry_run=True,
                )
            )

            self.assertFalse(result.project_dir.exists())
            self.assertTrue(result.files)

    def test_refuses_non_empty_directory_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "demo"
            root.mkdir()
            (root / "README.md").write_text("existing", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                create_project(
                    CreateOptions(
                        name="demo",
                        template="python-cli",
                        output_dir=Path(directory),
                        description="Demo",
                        author="Tester",
                        year="2026",
                    )
                )


if __name__ == "__main__":
    unittest.main()
