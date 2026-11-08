from typing import Optional
import logging

from verbecc.core.utils.config.logging_config_util import LoggingConfigUtil


APP_NAME = "verbecc"


class LoggingUtils:
    _logger: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        # todo: do something with name
        if cls._logger is None:
            log_cfg_util = LoggingConfigUtil()
            logging_config = log_cfg_util.load_config()
            log_cfg_util.apply_config(logging_config)
            cls._logger = logging.getLogger(APP_NAME)
        return cls._logger
