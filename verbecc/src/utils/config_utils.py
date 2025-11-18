from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig

# from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts


class ConfigUtils:

    @staticmethod
    def load_verbecc_config() -> VerbeccConfig:
        """Loads and returns the Verbecc configuration."""
        return VerbeccConfig()

    """
    def _apply_jsbeautifier_opts(self, config: VerbeccConfig) -> VerbeccConfig:
        # Applies the JSBeautifier options from the config to the given options object.
        opts = JSBeautifierOpts.get_opts()
        for k, v in config.JSBEAUTIFIER_OPTS.items():
            setattr(opts, k, v)
        return config
    """
