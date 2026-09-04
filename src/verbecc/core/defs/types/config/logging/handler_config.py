from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HandlerConfig:
    level: str = field(default="INFO")
    formatter: Optional[str] = field(default="simpleFormatter")
