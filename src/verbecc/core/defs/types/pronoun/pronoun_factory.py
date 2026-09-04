from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.pronoun.pronoun import Pronoun
from verbecc.core.defs.types.pronoun.pronouns import Pronouns


class PronounFactory:
    @classmethod
    def from_string(cls, lang: Lang, s: str) -> Pronoun:
        if lang == Lang.fr:
            return Pronouns.fr(s)
        elif lang == Lang.es:
            return Pronouns.es(s)
        elif lang == Lang.en:
            return Pronouns.en(s)
        elif lang == Lang.it:
            return Pronouns.it(s)
        elif lang == Lang.ca:
            return Pronouns.ca(s)
        elif lang == Lang.ro:
            return Pronouns.ro(s)
        elif lang == Lang.pt:
            return Pronouns.pt(s)
