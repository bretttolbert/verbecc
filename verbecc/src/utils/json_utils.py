from dataclasses import fields
import json

from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig
from verbecc.src.defs.types.config.json_opts import JSONOpts
from verbecc.src.utils.config_util_verbecc import VerbeccConfigUtil
from verbecc.src.utils.jsbeautifier_utils import JSBeautifier

config = VerbeccConfigUtil().load_config()


class JSONUtils:

    @classmethod
    def to_json(cls, data: object, beautify: bool = config.JSBEAUTIFIER_ENABLE) -> str:
        """The data of the given object as a JSON string, optionally pretty-formatted,
        using the JSON and JSBEAUTIFIER options from the VerbeccConfig.
        :param beautify: Whether to pretty-format the JSON output
        :return: JSON string
        """
        kwargs = {}
        json_opts = config.JSON_OPTS
        for field in fields(json_opts):
            kwargs[field.name] = getattr(json_opts, field.name)
        ret = json.dumps(data, **kwargs)
        if beautify:
            ret = JSBeautifier.beautify(ret)
        return ret
