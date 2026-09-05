from abc import abstractmethod
from importlib.resources import abc, as_file, files
from pathlib import Path
from typing import Optional, TextIO, TypeVar, Generic

T = TypeVar("T")


class BaseConfigUtil(Generic[T]):
    """
    Abstract base utility class for loading configuration from YAML config file"""

    yaml_filename = ""
    _yaml_resource_path = None

    def __init__(self, yaml_filename: str) -> None:
        self.yaml_filename = yaml_filename
        self.find_config_yaml_resource_path()

    def find_config_yaml_resource_path(self) -> None:
        try:
            # source path
            self._yaml_resource_path = files("verbecc.config") / self.yaml_filename
        except KeyError:
            # unit-tests path
            self._yaml_resource_path = files("verbecc.verbecc.config") / self.yaml_filename

    def load_config(self) -> T:
        """Loads and returns the configuration."""
        return self._load_config_yaml_resource()

    def _load_config_yaml_filepath(self, filepath: Path) -> T:
        with open(filepath, "r", encoding="utf-8") as f:
            return self._load_config_from_filestream(f)

    def _load_config_yaml_resource(self) -> T:
        ret: Optional[T] = None
        if self._yaml_resource_path is None:
            raise Exception(f"Failed to load yaml config file {self.yaml_filename}")
        elif isinstance(self._yaml_resource_path, abc.Traversable):  # type: ignore
            with as_file(self._yaml_resource_path) as path:
                with path.open("r", encoding="utf-8") as f:
                    ret = self._load_config_from_filestream(f)
        if ret is not None:
            return ret
        else:
            raise TypeError("Invalid _yaml_resource_path ({0})".format(self._yaml_resource_path))

    @abstractmethod
    def _load_config_from_filestream(self, filestream: TextIO) -> T:
        pass
