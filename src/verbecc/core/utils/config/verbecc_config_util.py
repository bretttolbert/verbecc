from typing import TextIO

from verbecc.core.utils.config.base_config_util import BaseConfigUtil
from verbecc.core.defs.types.config.verbecc_config import VerbeccConfig


class VerbeccConfigUtil(BaseConfigUtil[VerbeccConfig]):
    """
    Utility class for loading Verbecc configuration from YAML config file
    """

    yaml_filename = "verbecc_config.yaml"
    _yaml_resource_path = None

    def __init__(self) -> None:
        super().__init__(self.yaml_filename)

    def _load_config_from_filestream(self, filestream: TextIO) -> VerbeccConfig:
        ret = VerbeccConfig()
        data: VerbeccConfig | list[VerbeccConfig] = VerbeccConfig.from_yaml(  # pyright: ignore[reportUnknownMemberType]
            filestream
        )
        if isinstance(data, list):
            ret = data[0]
        else:
            ret = data
        return ret
