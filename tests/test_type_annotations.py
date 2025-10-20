"""
Type annotations pytest test module.
Test to ensure all functions and methods have type annotations for parameters and return types.
This test scans the source code files in the specified directory, parses them using the `ast`
module, and checks each function and method definition for missing type annotations.
If any missing annotations are found, the test fails and reports the specific locations
and details of the missing annotations.
This test module utlizes the indirect parametrization feature of pytest to create a separate test case
for each missing type annotation found during the scan.
Copyright (c) 2026, Brett Tolbert <http://bretttolbert.com/>
"""

import pytest
import ast
import os
from typing import List

EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".venv", "env", "build", "dist", "tests"}


class Finder(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.class_stack = []
        self.reported_errors: List[str] = []

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def _report(self, node, func_name, missing_params, missing_return, lineno):
        parts = []
        if missing_params:
            parts.append("params: " + ", ".join(missing_params))
        if missing_return:
            parts.append("return")
        msg = f"{self.filename}:{lineno} - {'.'.join(self.class_stack + [func_name])} -> missing {', '.join(parts)}"
        print(msg)
        # assert False, msg
        self.reported_errors.append(msg)

    def _check_func(self, node):
        is_method = bool(self.class_stack)
        missing = []
        # posonlyargs (py3.8+), args, kwonlyargs
        all_args = []
        if hasattr(node.args, "posonlyargs"):
            all_args.extend(node.args.posonlyargs)
        all_args.extend(node.args.args)
        all_args.extend(node.args.kwonlyargs)

        for arg in all_args:
            # skip annotation check for typical self/cls on methods
            if is_method and arg.arg in ("self", "cls"):
                continue
            if arg.annotation is None:
                missing.append(arg.arg)

        # vararg / kwarg
        if node.args.vararg and node.args.vararg.annotation is None:
            missing.append("*" + node.args.vararg.arg)
        if node.args.kwarg and node.args.kwarg.annotation is None:
            missing.append("**" + node.args.kwarg.arg)

        missing_return = node.returns is None

        if missing or missing_return:
            self._report(node, node.name, missing, missing_return, node.lineno)

    def visit_FunctionDef(self, node):
        self._check_func(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_func(node)
        self.generic_visit(node)


def scan_file(path: str) -> List[str]:
    print("Scanning", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src, filename=path)
    except Exception as e:
        return [f"Path {path}: parse error: {e}"]
    finder = Finder(path)
    finder.visit(tree)
    return finder.reported_errors


def walk_root(root) -> List[str]:
    errors = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip excluded dirs
        dirnames[:] = [
            d
            for d in dirnames
            if d not in EXCLUDE_DIRS and not d.startswith(".egg-info")
        ]
        for fn in filenames:
            if fn.endswith(".py"):
                errors.extend(scan_file(os.path.join(dirpath, fn)))
    return errors


def pytest_generate_tests(metafunc):
    """Indirect parametrization for pytest to run test_per_error for each missing type annotation found."""
    if "errors" in metafunc.fixturenames:
        errors: List[str] = walk_root(metafunc.config.rootpath)
        metafunc.parametrize("errors", errors)


def test_per_error(errors: str):
    """Test that fails for each missing type annotation found.
    Works with pytest using indirect parametrization.
    (See pytest_generate_tests above.)"""
    error = errors
    assert False, error


if __name__ == "__main__":
    test_per_error()
