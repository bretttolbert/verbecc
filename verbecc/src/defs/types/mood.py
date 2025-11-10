import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


class Mood(StrEnum):
    pass


class MoodEn(Mood):
    Conditional = "conditional"
    Gerund = "gerund"
    Imperative = "imperative"
    Indicative = "indicative"
    Infinitive = "infinitive"
    Participle = "participle"
    Subjunctive = "subjunctive"


class MoodFr(Mood):
    Conditionnel = "conditionnel"
    Imperatif = "imperatif"
    Indicatif = "indicatif"
    Infinitif = "infinitif"
    Participe = "participe"
    Subjonctif = "subjonctif"


class MoodEs(Mood):
    Condicional = "condicional"
    Gerundio = "gerundio"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinitivo = "infinitivo"
    Participo = "participo"
    Subjuntivo = "subjuntivo"


class MoodIt(Mood):
    Condizionale = "condizionale"
    Congiuntivo = "congiuntivo"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinito = "infinito"
    Participio = "participio"


class MoodCa(Mood):
    Condicional = "condicional"
    Gerundi = "gerundi"
    Imperatiu = "imperatiu"
    Indicatiu = "indicatiu"
    Infinitiu = "infinitiu"
    Participi = "particip"
    Subjuntiu = "subjuntiu"


class MoodRo(Mood):
    NA = "(nu se aplică)"  # For "not applicable", the Romanian equivalent is "nu se aplică"
    Condițional = "condițional"
    Conjunctiv = "conjunctiv"
    Gerunziu = "gerunziu"
    Imperativ = "imperativ"
    Indicativ = "indicativ"
    Infinitiv = "infinitiv"
    Participiu = "participiu"
    Subjunctiv = "subjunctiv"


class MoodPt(Mood):
    Condicional = "condicional"
    Gerúndio = "gerúndio"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinitivo = "infinitivo"
    Particípio = "particípio"
    Subjuntivo = "subjuntivo"


class Moods:
    ca = MoodCa
    en = MoodEn
    es = MoodEs
    fr = MoodFr
    it = MoodIt
    pt = MoodPt
    ro = MoodRo


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
