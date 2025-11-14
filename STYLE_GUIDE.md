# verbecc Style Guide

## The Python `@property` decorator shall not be used

This is primarily because I intend to port verbecc to Java and other languages and I wish to keep the implementations as consistent as possible, preferably a 1:1 equivalence in all symbol names, _mutata mutandis_.

## There shall not be more than class definition per file

This simplifies porting to Java, allowing 1:1 source file correspondence. This rule is enforced by the `test_type_annotations` unit-tests.
