from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FormatterConfig:
    format: str = field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    datefmt: Optional[str] = field(default=None)
