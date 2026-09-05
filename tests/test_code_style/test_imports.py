import pytest
import subprocess
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
    assert result.stdout == "", \
        f"Found violation of STYLE_GUIDE rule R005 - `__init__.py` files shall only use relative imports):" + \
        f"\n{result.stdout}\nErrors: {result.stderr}"
