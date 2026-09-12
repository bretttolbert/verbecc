import pytest
import subprocess
import ast
from pathlib import Path

@pytest.fixture
def project_root(pytestconfig: pytest.Config) -> Path:
    # Injects the built-in pytestconfig fixture
    return pytestconfig.rootpath


def test_STYLE_GUIDE_R005_only_relative_imports(project_root: Path) -> None:
    """Enforces STYLE_GUIDE rule R005 - `__init__.py` files shall only use relative imports"""
    command: list[str] = [
        "find",
        str(project_root),
        "-name",
        "__init__.py",
        "-exec",
        "grep",
        "-PHn",
        r"^(?:from|import)(?! \.)",
        "{}",
        ";",
    ]

    # Execute the command safely as a subprocess
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Assert that stdout is completely empty
    assert result.stdout == "", (
        f"Found violation of STYLE_GUIDE rule R005 - "
        f"`__init__.py` files shall only use relative imports:\n"
        + f"\n{result.stdout}\nErrors: {result.stderr}"
    )


def test_STYLE_GUIDE_R006_no_deep_relative_imports(project_root: Path) -> None:
    """Enforces STYLE_GUIDE rule R006 - `__init__.py` imports shall be at most one level deep."""
    violations: list[str] = []
    for path in project_root.rglob("__init__.py"):
        if any(part in {".git", "__pycache__", "venv", ".venv", "env", "build", "dist"} for part in path.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            violations.append(f"{path}: parse error: {error}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            module_depth = len(node.module.split(".")) if node.module else 0
            if node.level > 1 or module_depth > 1:
                violations.append(f"{path}:{node.lineno}: {ast.unparse(node)}")

    assert violations == [], (
        "Found violation of STYLE_GUIDE rule R006 - "
        f"`__init__.py` imports shall not be deeper than one level:\n"
        + "\n".join(violations)
    )
