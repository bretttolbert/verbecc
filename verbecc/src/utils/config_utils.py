import yaml
import logging
from importlib.resources import as_file, files
from typing import Optional

from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig


class ConfigUtils:
    APP_NAME = "verbecc"
    VERBECC_CONFIG_YAML_FILENAME = "verbecc_config.yaml"
    VERBECC_CONFIG_YAML_RESOURCE_PATH = (
        files("verbecc.config") / VERBECC_CONFIG_YAML_FILENAME
    )
    _logger: Optional[logging.Logger] = None

    @classmethod
    def load_verbecc_config(cls) -> VerbeccConfig:
        """Loads and returns the Verbecc configuration."""
        return cls._load_verbecc_config_yaml()

    @classmethod
    def _load_verbecc_config_yaml(cls) -> VerbeccConfig:
        ret = VerbeccConfig()
        with as_file(cls.VERBECC_CONFIG_YAML_RESOURCE_PATH) as path:
            with path.open("r", encoding="utf-8") as f:
                data = VerbeccConfig.from_yaml(f)
                if isinstance(data, list):
                    ret = data[0]
                else:
                    ret = data
        return ret
