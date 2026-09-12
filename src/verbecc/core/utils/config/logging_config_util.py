from dataclasses import asdict
from typing import Any, TextIO, cast
import logging
import logging.config
import yaml

from verbecc.core.utils.config.base_config_util import BaseConfigUtil
from verbecc.core.defs.types.config.logging.logging_config import (
    LoggingConfig,
    LoggerConfig,
    FormatterConfig,
    HandlerConfig,
    StreamHandlerConfig,
    FileHandlerConfig,
)
from verbecc.core.utils.dict_utils import DictUtils


class LoggingConfigUtil(BaseConfigUtil[LoggingConfig]):
    """
    Utility class for loading Python logging configuration from YAML config file
    """

    yaml_filename = "logging_config.yaml"
    _yaml_resource_path = None

    def __init__(self) -> None:
        super().__init__(self.yaml_filename)

    def apply_config(self, logging_config: LoggingConfig) -> None:
        """Sets logging configuration to the provided config
        dataclass instance."""
        try:
            data = asdict(logging_config)
            data = DictUtils.unmarshall_keys_recursive(data)
            logging.config.dictConfig(cast(dict[str, object], data))
        except ValueError as ex:
            raise ex

    def _load_config_from_filestream(self, filestream: TextIO) -> LoggingConfig:
        """
        Manually convert the dictionary to our dataclass structure
        This part can be simplified with libraries like `dacite` or `marshmallow-dataclass`
        """
        loaded_data = yaml.safe_load(filestream)
        data = cast(dict[str, Any], loaded_data) if isinstance(loaded_data, dict) else {}
        data = cast(
            dict[str, Any], DictUtils.marshall_keys_recursive(data, ["class"])
        )
        formatters_data = cast(dict[str, dict[str, Any]], data.get("formatters", {}))
        formatters = {
            name: FormatterConfig(**formatter_data)
            for name, formatter_data in formatters_data.items()
        }
        handlers: dict[str, HandlerConfig] = {}
        for name, d in data.get("handlers", {}).items():
            if name == "consoleHandler":
                handlers[name] = StreamHandlerConfig(**d)
            elif name == "fileHandler":
                handlers[name] = FileHandlerConfig(**d)
        loggers = {
            name: LoggerConfig(**d) for name, d in data.get("loggers", {}).items()
        }
        root = LoggerConfig(**data["root"]) if "root" in data else None

        return LoggingConfig(
            version=data["version"],
            disable_existing_loggers=data.get("disable_existing_loggers", False),
            formatters=formatters,
            handlers=handlers,
            loggers=loggers,
            root=root,
        )
