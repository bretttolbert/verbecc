from typing import Dict

from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.defs.types.exceptions import InvalidLangError
from verbecc.src.inflectors.lang.inflector_ca import InflectorCa
from verbecc.src.inflectors.lang.inflector_es import InflectorEs
from verbecc.src.inflectors.lang.inflector_fr import InflectorFr
from verbecc.src.inflectors.lang.inflector_it import InflectorIt
from verbecc.src.inflectors.lang.inflector_pt import InflectorPt
from verbecc.src.inflectors.lang.inflector_ro import InflectorRo


SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ca": "català",
    "es": "español",
    "fr": "français",
    "it": "italiano",
    "pt": "português",
    "ro": "română",
}


class InflectorFactory:
    @classmethod
    def make_inflector(cls, lang: str) -> Inflector:
        """
        :param lang: two-letter language code
        :type lang: str
        """
        ret = None
        if lang == "ca":
            ret = InflectorCa()
        elif lang == "es":
            ret = InflectorEs()
        elif lang == "fr":
            ret = InflectorFr()
        elif lang == "it":
            ret = InflectorIt()
        elif lang == "pt":
            ret = InflectorPt()
        elif lang == "ro":
            ret = InflectorRo()
        else:
            raise InvalidLangError
        return ret
