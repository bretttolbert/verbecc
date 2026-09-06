from dataclasses import fields

from typing import Optional
import jsbeautifier

from verbecc.core.utils.config.verbecc_config_util import VerbeccConfigUtil


class JSBeautifier:
    config = VerbeccConfigUtil().load_config()
    opts: Optional[jsbeautifier.BeautifierOptions] = None

    @classmethod
    def beautify(cls, s: str) -> str:
        """Pretty-format the given JavaScript string.
        :param s: The JavaScript string to beautify
        :return: The pretty-formatted JavaScript string

        Note: Ignores config.JSBEAUTIFIER_ENABLE; caller must check that separately.
        If you are calling this, we assume you want beautification regardless of config.
        """
        return jsbeautifier.beautify(s, JSBeautifier.get_opts())

    @classmethod
    def get_opts(cls) -> jsbeautifier.BeautifierOptions:
        if cls.opts is None:
            cls.opts = jsbeautifier.default_options()
            config_opts = cls.config.JSBEAUTIFIER_OPTS
            for field in fields(config_opts):
                key = field.name
                value = getattr(config_opts, key)
                setattr(cls.opts, key, value)
        return cls.opts
