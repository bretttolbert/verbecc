from typing import Optional
import jsbeautifier

from verbecc.src.utils.config_utils import ConfigUtils

config = ConfigUtils.load_verbecc_config()


class JSBeautifierOpts:

    opts: Optional[jsbeautifier.BeautifierOptions] = None

    @classmethod
    def get_opts(cls) -> jsbeautifier.BeautifierOptions:
        if cls.opts is None:
            cls.opts = jsbeautifier.default_options()
            for k, v in config.JSBEAUTIFIER_OPTS.items():
                setattr(cls.opts, k, v)
        return cls.opts
