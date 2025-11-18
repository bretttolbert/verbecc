import json

# from verbecc.src.utils.jsbeautifier_utils import JSBeautifier


class VerbeccConfig:
    ENABLE_LOGGING = True
    DEVEL_MODE = False
    ENABLE_ML_PREDICTION = True
    JSON_OPT_ENSURE_ASCII = False
    JSBEAUTIFIER_ENABLE = True
    JSBEAUTIFIER_OPTS = {
        "indent_size": "4",
        "indent_char": " ",
        "max_preserve_newlines": "-1",
        "preserve_newlines": False,
        "keep_array_indentation": False,
        "break_chained_methods": False,
        "indent_scripts": "normal",
        "brace_style": "expand",
        "space_before_conditional": True,
        "unescape_strings": False,
        "jslint_happy": False,
        "end_with_newline": False,
        "wrap_line_length": "80",
        "indent_inner_html": False,
        "comma_first": False,
        "e4x": False,
        "indent_empty_lines": False,
    }

    def __init__(self) -> None:
        pass

    def get_data(self) -> object:
        """The data of this object as primitive types (JSON-serializable)"""
        return {
            "ENABLE_LOGGING": VerbeccConfig.ENABLE_LOGGING,
            "DEVEL_MODE": VerbeccConfig.DEVEL_MODE,
            "ENABLE_ML_PREDICTION": VerbeccConfig.ENABLE_ML_PREDICTION,
            "JSON_OPT_ENSURE_ASCII": VerbeccConfig.JSON_OPT_ENSURE_ASCII,
            "JSBEAUTIFIER_ENABLE": VerbeccConfig.JSBEAUTIFIER_ENABLE,
            "JSBEAUTIFIER_OPTS": VerbeccConfig.JSBEAUTIFIER_OPTS,
        }

    def to_json(self, beautify: bool = True) -> str:
        """The data of this object as a JSON string,
        optionally pretty-formatted.
        """
        ret = json.dumps(
            self.get_data(),
            allow_nan=False,
            sort_keys=True,
            indent=4,
            ensure_ascii=self.JSON_OPT_ENSURE_ASCII,
        )

        # Below would be a circular import, sadly.
        # if beautify:
        #    ret = JSBeautifier.beautify(ret)

        return ret

    def __str__(self) -> str:
        return self.to_json()
