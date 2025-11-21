from dataclasses import asdict
from importlib_resources import abc, as_file, files
from pathlib import Path
from typing import Dict, Optional, TextIO
import logging
import logging.config
import yaml

from verbecc.src.utils.config_util import AbstractConfigUtil
from verbecc.src.defs.types.config.logging.logging_config import (
    LoggingConfig,
    LoggerConfig,
    FormatterConfig,
    HandlerConfig,
    StreamHandlerConfig,
    FileHandlerConfig,
)
from verbecc.src.utils.dict_utils import DictUtils


class LoggingConfigUtil(AbstractConfigUtil):
    """
    Utility class for loading Python logging configuration from YAML config file
    """

    # static:
    APP_NAME = "verbecc"
    YAML_FILENAME = "logging_config.yaml"
    # instance:
    _yaml_resource_path = None
    _logger: Optional[logging.Logger] = None

    def __init__(self) -> None:
        try:
            # source path
            self._yaml_resource_path = files("verbecc.config") / self.YAML_FILENAME
        except KeyError as ex0:
            # unit-tests path
            try:
                self._yaml_resource_path = (
                    files("verbecc.verbecc.config") / self.YAML_FILENAME
                )
            except TypeError as ex1:
                # python <=3.9 hack
                try:
                    self._yaml_resource_path = (
                        Path(__file__).parent.parent.parent
                        / "config"
                        / self.YAML_FILENAME
                    )

                except Exception as ex2:
                    msg = (
                        "You are likely running an incompatible python version. "
                        + "_yaml_resource_path={0} ex1={1} ex2={2}".format(
                            self._yaml_resource_path, ex1, ex2
                        )
                    )
                    raise Exception(msg)

    def apply_config(self, logging_config: LoggingConfig) -> None:
        """Sets logging configuration to the provided config
        dataclass instance."""
        try:
            data = asdict(logging_config)
            data = DictUtils.unmarshall_keys_recursive(data)
            logging.config.dictConfig(data)
        except ValueError as ex:
            raise ex

    def load_config(self, filepath: Optional[str] = None) -> LoggingConfig:
        """Loads and returns the Verbecc logging configuration."""
        return self._load_config_yaml_resource()

    def _load_config_yaml_filepath(self, filepath: Path) -> LoggingConfig:
        with open(filepath, "r", encoding="utf-8") as f:
            return self.__load_config_from_filestream(f)

    def _load_config_yaml_resource(self) -> LoggingConfig:
        ret: Optional[LoggingConfig] = None
        if self._yaml_resource_path is None:
            raise Exception("Failed to load verbecc config.")
        elif isinstance(self._yaml_resource_path, abc.Traversable):  # type: ignore
            # python >= 3.10 code path:
            with as_file(self._yaml_resource_path) as path:
                with path.open("r", encoding="utf-8") as f:
                    ret = self.__load_config_from_filestream(f)
        elif isinstance(self._yaml_resource_path, Path):
            # python <= 3.9 code path:
            path = self._yaml_resource_path
            with open(path, "r", encoding="utf-8") as f:
                ret = self.__load_config_from_filestream(f)
        if ret is not None:
            return ret
        else:
            raise TypeError(
                "Invalid _yaml_resource_path ({0})".format(self._yaml_resource_path)
            )

    def __load_config_from_filestream(self, filestream: TextIO) -> LoggingConfig:
        """
        Manually convert the dictionary to our dataclass structure
        This part can be simplified with libraries like `dacite` or `marshmallow-dataclass`
        """
        data = yaml.safe_load(filestream)
        data = DictUtils.marshall_keys_recursive(data, ["class"])
        formatters = {
            name: FormatterConfig(**d) for name, d in data.get("formatters", {}).items()
        }
        handlers: Dict[str, HandlerConfig] = {}
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
