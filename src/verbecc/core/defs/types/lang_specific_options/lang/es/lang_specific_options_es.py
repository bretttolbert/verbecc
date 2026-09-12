from verbecc.core.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.core.defs.types.lang_specific_options.lang.es.voseo_options import (
    VoseoOptions,
)


class LangSpecificOptionsEs(LangSpecificOptions):

    def __init__(self, voseo_options: VoseoOptions = VoseoOptions.VoseoTipo3) -> None:
        super().__init__()
        self._voseo_options = voseo_options

    def get_voseo_options(self) -> VoseoOptions:
        return self._voseo_options
