from dataclasses import dataclass, field

from verbecc.core.defs.types.config.logging.handler_config import HandlerConfig


@dataclass
class StreamHandlerConfig(HandlerConfig):
    # 'class' is a keyword, so use metadata
    class_: str = field(default="logging.StreamHandler", metadata={"name": "class"})
    stream: str = field(default="ext://sys.stdout")
