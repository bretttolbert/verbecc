from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.defs.types.lang.es.voseo_options import VoseoOptions


class LangSpecificOptionsEs(LangSpecificOptions):

    def __init__(self, voseo_options: VoseoOptions = VoseoOptions.NoVoseo) -> None:
        super().__init__()
        self._voseo_options = voseo_options

    @property
    def voseo_options(self) -> VoseoOptions:
        return self._voseo_options
