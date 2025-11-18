from importlib_resources import as_file, files
from typing import Any, Dict, Optional
import logging
import logging.config
import yaml

from verbecc.src.defs.constants import config as verbecc_config


class LogUtils:
    APP_NAME = "verbecc"
    _logger: Optional[logging.Logger] = None

    @classmethod
    def setup_logging(cls) -> None:
        """Loads logging configuration from a YAML file.
        ENABLE_LOGGING must be enabled in order for logging to be enabled.
        DEVEL_MODE increases verbosity from INFO to DEBUG level.
        """
        logging_level = logging.CRITICAL + 1  # effectively disables logging
        if verbecc_config.ENABLE_LOGGING:
            if verbecc_config.DEVEL_MODE:
                logging_level = logging.DEBUG
            else:
                logging_level = logging.INFO
        logging_config: Dict[str, Any] = {"level": logging_level}
        source = files("verbecc.config").joinpath("logging_config.yaml")
        with as_file(source) as path:
            with path.open("r", encoding="utf-8") as f:
                logging_config.update(yaml.safe_load(f))
        logging.config.dictConfig(logging_config)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        # todo: do something with name
        if LogUtils._logger is None:
            cls.setup_logging()
            LogUtils._logger = logging.getLogger(cls.APP_NAME)
        return LogUtils._logger
