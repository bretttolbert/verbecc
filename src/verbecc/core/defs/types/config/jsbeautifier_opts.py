from dataclasses import dataclass, field
from dataclass_wizard import YAMLWizard


@dataclass
class JSBeautifierOpts(YAMLWizard):
    brace_style: str = field(default="expand")
    break_chained_methods: bool = field(default=False)
    comma_first: bool = field(default=False)
    e4x: bool = field(default=False)
    end_with_newline: bool = field(default=False)
    indent_char: str = field(default=" ")
    indent_empty_lines: bool = field(default=False)
    indent_inner_html: bool = field(default=False)
    indent_scripts: str = field(default="normal")
    indent_size: int = field(default=4)
    jslint_happy: bool = field(default=False)
    keep_array_indentation: bool = field(default=False)
    max_preserve_newlines: int = field(default=-1)
    preserve_newlines: bool = field(default=False)
    space_before_conditional: bool = field(default=True)
    unescape_strings: bool = field(default=False)
    wrap_line_length: int = field(default=80)
