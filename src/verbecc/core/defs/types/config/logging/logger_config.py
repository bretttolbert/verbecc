from dataclasses import dataclass, field
from typing import List


@dataclass
class LoggerConfig:
    level: str = field(default="CRITICAL")
    handlers: list[str] = field(default_factory=list)
    propagate: bool = field(default=True)
