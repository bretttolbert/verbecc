from typing import Optional

from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.exceptions import InvalidLangError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.inflectors.lang.inflector_ca import InflectorCa
from verbecc.src.inflectors.lang.inflector_es import InflectorEs
from verbecc.src.inflectors.lang.inflector_fr import InflectorFr
from verbecc.src.inflectors.lang.inflector_it import InflectorIt
from verbecc.src.inflectors.lang.inflector_pt import InflectorPt
from verbecc.src.inflectors.lang.inflector_ro import InflectorRo


class InflectorFactory:
    @classmethod
    def make_inflector(
        cls,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
    ) -> Inflector:
        """
        :param lang: two-letter language code (ISO 639-1 Code)
        :type lang: LangCodeISO639_1
        """
        ret = None
        if lang == "ca":
            ret = InflectorCa(lang_specific_options)
        elif lang == "es":
            ret = InflectorEs(lang_specific_options)
        elif lang == "fr":
            ret = InflectorFr(lang_specific_options)
        elif lang == "it":
            ret = InflectorIt(lang_specific_options)
        elif lang == "pt":
            ret = InflectorPt(lang_specific_options)
        elif lang == "ro":
            ret = InflectorRo(lang_specific_options)
        else:
            raise InvalidLangError
        return ret
