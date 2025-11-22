"""
Abstract Syntax Tree (AST) pytest test module
Uses Python ast module with pytest to test various code attributes

1. Test Type Annotations
Test to ensure all functions and methods have type annotations for parameters
and return types.
This test scans the source code files in the specified directory, parses them
using the `ast` module, and checks each function and method definition for
missing type annotations.
If any missing annotations are found, the test fails and reports the specific
locations and details of the missing annotations.
This test module utilizes the indirect parametrization feature of pytest to
create a separate test case for each missing type annotation found during the scan.
Useful if you are trying to write code that is easily portable to Java.

2. Test One Class Per File
Test to ensure that there is only one class definition in each source file.
Useful if you are trying to write code that is easily portable to Java.

Copyright (c) 2026, Brett Tolbert <http://bretttolbert.com/>
"""

import ast
import os
from typing import List, Union

EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".venv", "env", "build", "dist", "tests"}

TEST_NAMES = [("Test Type Annotations"), ("Test One Class Per File")]
TEST_TYPE_ANNOTATIONS = 0
TEST_ONE_CLASS_PER_FILE = 1


class Finder(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.class_stack = []
        self._class_count = 0
        self._reported_errors: List[str] = []

    def get_reported_errors(self) -> List[str]:
        return self._reported_errors

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_count += 1
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self._check_class(node)
        self.class_stack.pop()

    def _base_errmsg(self, test_id: int) -> str:
        test_name = TEST_NAMES[test_id]
        return f"Test AST test {test_name} failed: "

    def _report_error_param_or_return_missing_type_hint(
        self, node, func_name: str, lineno, missing_params, missing_return
    ):
        parts = []
        errmsg = self._base_errmsg(TEST_TYPE_ANNOTATIONS)
        if missing_params:
            parts.append(
                errmsg + "params missing type annotation: " + ", ".join(missing_params)
            )
        if missing_return:
            parts.append(errmsg + "return statement missing type annotation")
        msg = (
            f"{self.filename}:{lineno} - "
            + f"{'.'.join(self.class_stack + [func_name])} -> "
            + f"missing {', '.join(parts)}"
        )
        print(msg)
        self._reported_errors.append(msg)

    def _report_error_multiple_class_definitions_in_same_file(
        self, node, class_name: str, lineno
    ) -> None:
        errmsg = self._base_errmsg(TEST_ONE_CLASS_PER_FILE)
        msg = (
            errmsg
            + f"multiple class definitions in same file: {self.filename}:{lineno} {class_name}"
        )
        self._reported_errors.append(msg)

    def _check_class(self, node: ast.ClassDef) -> None:
        if self._class_count > 1:
            self._report_error_multiple_class_definitions_in_same_file(
                node, node.name, node.lineno
            )

    def _check_func(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
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
            self._report_error_param_or_return_missing_type_hint(
                node, node.name, node.lineno, missing, missing_return
            )

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_func(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
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
    return finder.get_reported_errors()


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


NO_ERRORS = "(no errors)"


def pytest_generate_tests(metafunc):
    """Indirect parametrization for pytest to run test_per_error for
    each missing type annotation found."""
    if "error" in metafunc.fixturenames:
        errors: List[str] = walk_root(metafunc.config.rootpath)
        # below is a bit hacky but allows test_ast module to
        # show as passing rather than as skipped due to an empty
        # errors list being sent to parametrize
        if len(errors) == 0:
            errors.append(NO_ERRORS)
        metafunc.parametrize("error", errors)


def test_per_error(error: str):
    """Test that fails for each AST error found.
    If there are no errors, it will run once and pass.
    Works with pytest using indirect parametrization.
    (See pytest_generate_tests above)
    """
    assert error == NO_ERRORS
