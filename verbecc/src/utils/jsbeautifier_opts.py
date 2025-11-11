from typing import Optional
import jsbeautifier

from verbecc.src.defs.constants.config import JSBEAUTIFIER_OPTS


class JSBeautifierOpts:

    opts: Optional[jsbeautifier.BeautifierOptions] = None

    @classmethod
    def get_opts(cls) -> jsbeautifier.BeautifierOptions:
        if cls.opts is None:
            cls.opts = jsbeautifier.default_options()
            for k, v in JSBEAUTIFIER_OPTS.items():
                setattr(cls.opts, k, v)
        return cls.opts
