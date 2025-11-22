from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.tense.tense import Tense
from verbecc.src.defs.types.tense.tenses import Tenses


class TenseFactory:
    @classmethod
    def from_string(cls, lang: Lang, s: str) -> Tense:
        if lang == Lang.fr:
            return Tenses.fr(s)
        elif lang == Lang.es:
            return Tenses.es(s)
        elif lang == Lang.en:
            return Tenses.en(s)
        elif lang == Lang.it:
            return Tenses.it(s)
        elif lang == Lang.ca:
            return Tenses.ca(s)
        elif lang == Lang.ro:
            return Tenses.ro(s)
        elif lang == Lang.pt:
            return Tenses.pt(s)
