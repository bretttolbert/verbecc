from typing import Optional
from dataclasses import dataclass, field
from dataclass_wizard.v0 import YAMLWizard


@dataclass
class JSONOpts(YAMLWizard):
    allow_nan: bool = field(default=False)
    sort_keys: bool = field(default=True)
    ensure_ascii: bool = field(default=True)
    indent: Optional[int] = field(default=4)
