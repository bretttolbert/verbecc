from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Mood, Moods


class MoodFactory:
    @classmethod
    def from_string(cls, lang: Lang, s: str) -> Mood:
        if lang == Lang.ca:
            return Moods.ca(s)
        elif lang == Lang.en:
            return Moods.en(s)
        elif lang == Lang.es:
            return Moods.es(s)
        elif lang == Lang.fr:
            return Moods.fr(s)
        elif lang == Lang.it:
            return Moods.it(s)
        elif lang == Lang.pt:
            return Moods.pt(s)
        elif lang == Lang.ro:
            return Moods.ro(s)
