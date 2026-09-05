from dataclasses import dataclass, field


@dataclass
class LoggerConfig:
    level: str = field(default="CRITICAL")
    handlers: list[str] = field(default_factory=list[str])
    propagate: bool = field(default=True)
