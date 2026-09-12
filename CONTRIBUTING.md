# Contributing to verbecc

First off, thank you for taking the time to contribute! 🎉 

---

## Table of Contents

- [Style Guide](#style-guide)

## Style Guide

### R001 - The Python `@property` decorator shall not be used

This is primarily because I intend to port verbecc to Java and other languages and I wish to keep the implementations as consistent as possible, preferably a _1:1_ equivalence in all symbol names, _mutata mutandis_.

### R002 - There shall not be more than one class definition per file

This simplifies porting to Java, allowing _1:1_ source file correspondence. This rule is enforced by the `test_ast` unit-tests.

### R003 - Type annotations are required for all parameters and return statements

This rule is enforced by the `test_ast` unit-tests.

### R004 - Don't use parentheses in import statements

Without parentheses, I can easily sort the import statements (_Ctrl+P Sort Lines Ascending_), 
but with parentheses, I can't do that.

### R005 - `__init__.py` files shall only use relative imports

- Allowed: `from .module import SomeClass`
- Not allowed: `from verbecc.core.foo import bar`

How to check:
```bash
python -m pytest -k test_STYLE_GUIDE_R005_only_relative_imports
```

### R006 - `__init__.py` files shall not contain imports deeper than one level

- Allowed: `from .module import SomeClass`
- Not Allowed: `from .module.submodule import SomeClass`

Why:
- Pollutes the namespace
- Hides where things come from
- Slows down import time by unnecessarily loading unused modules
- Causes circular imports
