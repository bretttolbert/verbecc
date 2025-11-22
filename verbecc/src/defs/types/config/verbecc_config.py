from dataclasses import dataclass, field
from dataclass_wizard import YAMLWizard

from verbecc.src.defs.types.config.jsbeautifier_opts import JSBeautifierOpts
from verbecc.src.defs.types.config.json_opts import JSONOpts


@dataclass
class VerbeccConfig(YAMLWizard):
    version: int = field(default=1)
    ENABLE_ML_PREDICTION: bool = field(default=True)
    JSBEAUTIFIER_ENABLE: bool = field(default=True)
    JSBEAUTIFIER_OPTS: JSBeautifierOpts = field(default_factory=JSBeautifierOpts)
    JSON_OPTS: JSONOpts = field(default_factory=JSONOpts)
