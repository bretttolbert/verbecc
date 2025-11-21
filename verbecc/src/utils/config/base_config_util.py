from abc import abstractmethod
from importlib_resources import abc, as_file, files
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
        except KeyError as ex0:
            # unit-tests path
            try:
                self._yaml_resource_path = (
                    files("verbecc.verbecc.config") / self.yaml_filename
                )
            except TypeError as ex1:
                # python <=3.9 hack
                try:
                    dir_path = Path(__file__).parent.parent.parent
                    self._yaml_resource_path = dir_path / "config" / self.yaml_filename
                    while self._yaml_resource_path is None or not Path.exists(
                        self._yaml_resource_path
                    ):
                        self._yaml_resource_path = (
                            dir_path.parent / "config" / self.yaml_filename
                        )

                except Exception as ex2:
                    msg = (
                        "You are likely running an incompatible python version. "
                        + "_yaml_resource_path={0} ex1={1} ex2={2}".format(
                            self._yaml_resource_path, ex1, ex2
                        )
                    )
                    raise Exception(msg)

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
            # python >= 3.10 code path:
            with as_file(self._yaml_resource_path) as path:
                with path.open("r", encoding="utf-8") as f:
                    ret = self._load_config_from_filestream(f)
        elif isinstance(self._yaml_resource_path, Path):
            # python <= 3.9 code path:
            path = self._yaml_resource_path
            with open(path, "r", encoding="utf-8") as f:
                ret = self._load_config_from_filestream(f)
        if ret is not None:
            return ret
        else:
            raise TypeError(
                "Invalid _yaml_resource_path ({0})".format(self._yaml_resource_path)
            )

    @abstractmethod
    def _load_config_from_filestream(self, filestream: TextIO) -> T:
        pass
