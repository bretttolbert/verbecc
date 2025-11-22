from dataclasses import dataclass, field

from verbecc.src.defs.types.config.logging.handler_config import HandlerConfig


@dataclass
class FileHandlerConfig(HandlerConfig):
    # 'class' is a keyword, so use metadata
    class_: str = field(default="logging.FileHandler", metadata={"name": "class"})
    filename: str = field(default="verbecc.log")
    maxBytes: int = field(default=10485760)
    backupCount: int = field(default=5)
