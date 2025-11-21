from dataclasses import asdict
from importlib_resources import abc, as_file, files
from pathlib import Path
from typing import TextIO

from verbecc.src.utils.config_util import AbstractConfigUtil
from verbecc.src.utils.logging_utils import LoggingUtils
from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig


class VerbeccConfigUtil(AbstractConfigUtil):
    # static
    APP_NAME = "verbecc"
    YAML_FILENAME = "verbecc_config.yaml"
    # instance:
    _yaml_resource_path = None

    def __init__(self) -> None:
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)
        try:
            self._yaml_resource_path = files("verbecc.config") / self.YAML_FILENAME
        except TypeError as ex1:
            try:
                # python <=3.9 hack
                self._yaml_resource_path = (
                    Path(__file__).parent.parent.parent / "config" / self.YAML_FILENAME
                )

            except Exception as ex2:
                msg = (
                    "You are likely running an incompatible python version. "
                    + "_yaml_resource_path={0} ex1={1} ex2={2}".format(
                        self._yaml_resource_path, ex1, ex2
                    )
                )
                raise Exception(msg)

    def load_config(self) -> VerbeccConfig:
        """Loads and returns the Verbecc configuration."""
        return self._load_config_yaml_resource()

    def _load_config_yaml_resource(self) -> VerbeccConfig:
        ret = VerbeccConfig()
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
        else:
            raise TypeError(
                "Invalid _yaml_resource_path ({0})".format(self._yaml_resource_path)
            )
        return ret

    def __load_config_from_filestream(self, filestream: TextIO) -> VerbeccConfig:
        ret = VerbeccConfig()
        data = VerbeccConfig.from_yaml(filestream)
        if isinstance(data, list):
            ret = data[0]
        else:
            ret = data
        return ret
