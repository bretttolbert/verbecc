from typing import Optional

from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.defs.types.lang_specific_options.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.core.defs.types.lang_specific_options.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)


class LangSpecificOptionsFactory:
    @classmethod
    def make_lang_specific_options(
        cls, lang: LangCodeISO639_1
    ) -> Optional[LangSpecificOptions]:
        if lang == LangCodeISO639_1.es:
            return LangSpecificOptionsEs()
        return None
