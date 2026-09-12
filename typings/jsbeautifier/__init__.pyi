from typing import Any, TextIO


class BeautifierOptions:
    def __init__(self, options: Any = ...) -> None: ...


def default_options() -> BeautifierOptions: ...


def beautify(string: str, opts: BeautifierOptions = ...) -> str: ...


def beautify_file(file_name: str, opts: BeautifierOptions = ...) -> str: ...


def usage(stream: TextIO = ...) -> int: ...


def main() -> None: ...