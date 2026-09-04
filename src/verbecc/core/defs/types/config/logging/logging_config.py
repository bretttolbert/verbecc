from dataclasses import dataclass, field
from typing import Optional

from verbecc.core.defs.types.config.logging.formatter_config import FormatterConfig
from verbecc.core.defs.types.config.logging.stream_handler_config import (
    StreamHandlerConfig,
)
from verbecc.core.defs.types.config.logging.file_handler_config import FileHandlerConfig
from verbecc.core.defs.types.config.logging.handler_config import HandlerConfig
from verbecc.core.defs.types.config.logging.logger_config import LoggerConfig


@dataclass
class LoggingConfig:
    version: int = field(default=1)
    disable_existing_loggers: bool = field(default=False)
    formatters: dict[str, FormatterConfig] = field(default_factory=dict)
    handlers: dict[str, HandlerConfig] = field(
        default_factory=lambda: {
            "consoleHandler": StreamHandlerConfig(),
            "fileHandler": FileHandlerConfig(),
        }
    )
    loggers: dict[str, LoggerConfig] = field(default_factory=dict)
    root: Optional[LoggerConfig] = field(default_factory=LoggerConfig)
