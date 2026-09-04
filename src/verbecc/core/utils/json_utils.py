from typing import Optional
from dataclasses import fields
import json

from verbecc.core.utils.config.verbecc_config_util import VerbeccConfigUtil
from verbecc.core.utils.jsbeautifier_utils import JSBeautifier

config = VerbeccConfigUtil().load_config()


class JSONUtils:

    @classmethod
    def to_json(
        cls,
        data: object,
        indent: Optional[int] = config.JSON_OPTS.indent,
        beautify: bool = config.JSBEAUTIFIER_ENABLE,
    ) -> str:
        """The data of the given object as a JSON string, optionally pretty-formatted,
        using the JSON and JSBEAUTIFIER options from the VerbeccConfig.
        :param indent: Passed json.dumps(). None=no whitespace. Overrides config.JSON_OPS.indent.
        :param beautify: Whether to pretty-format the JSON output using jsbeautifier. Overrides config.JSBEAUTIFIER_ENABLE.
        :return: JSON string
        """
        kwargs = {}
        json_opts = config.JSON_OPTS
        if indent != json_opts.indent:
            json_opts.indent = indent
        for field in fields(json_opts):
            kwargs[field.name] = getattr(json_opts, field.name)
        ret = json.dumps(data, **kwargs) # type: ignore
        if beautify:
            ret = JSBeautifier.beautify(ret)
        return ret
