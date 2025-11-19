from importlib_resources import as_file, files
from typing import Any, Dict, Optional
import logging
import logging.config
import yaml

LoggingConfigDict = Dict[str, Any]


class LogUtils:
    APP_NAME = "verbecc"
    LOGGING_CONFIG_YAML_FILENAME = "logging_config.yaml"
    LOGGING_CONFIG_YAML_RESOURCE_PATH = (
        files("verbecc.config") / LOGGING_CONFIG_YAML_FILENAME
    )
    _logger: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        # todo: do something with name
        if LogUtils._logger is None:
            LogUtils.set_logging_config(LogUtils.load_logging_config())
            LogUtils._logger = logging.getLogger(cls.APP_NAME)
        return LogUtils._logger

    @staticmethod
    def set_logging_config(logging_config: LoggingConfigDict) -> None:
        """Loads logging configuration from a YAML file."""
        logging.config.dictConfig(logging_config)

    @staticmethod
    def load_logging_config() -> LoggingConfigDict:
        """Loads verbecc logging configuration."""
        ret = LogUtils._load_logging_config_yaml()
        return ret

    @classmethod
    def _load_logging_config_yaml(cls) -> LoggingConfigDict:
        """Loads base logging configuration from yaml file."""
        logging_config: LoggingConfigDict = {}
        with as_file(cls.LOGGING_CONFIG_YAML_RESOURCE_PATH) as path:
            with path.open("r", encoding="utf-8") as f:
                logging_config.update(yaml.safe_load(f))
                return logging_config
