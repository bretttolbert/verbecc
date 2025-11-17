import jsbeautifier

from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts
from verbecc.src.defs.constants import config


class JSBeautifier:

    @classmethod
    def beautify(cls, s: str) -> str:
        ret = s
        if config.JSBEAUTIFIER_ENABLE:
            ret = jsbeautifier.beautify(s, JSBeautifierOpts.get_opts())
        return ret
