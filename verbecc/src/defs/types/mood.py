import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


class MoodEn(StrEnum):
    Conditional = "conditional"
    Gerund = "gerund"
    Imperative = "imperative"
    Indicative = "indicative"
    Infinitive = "infinitive"
    Participle = "participle"
    Subjunctive = "subjunctive"


class MoodFr(StrEnum):
    Conditionnel = "conditionnel"
    Imperatif = "imperatif"
    Indicatif = "indicatif"
    Infinitif = "infinitif"
    Participe = "participe"
    Subjonctif = "subjonctif"


class MoodEs(StrEnum):
    Condicional = "condicional"
    Gerundio = "gerundio"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinitivo = "infinitivo"
    Participo = "participo"
    Subjuntivo = "subjuntivo"


class MoodIt(StrEnum):
    Condizionale = "condizionale"
    Congiuntivo = "congiuntivo"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinito = "infinito"
    Participio = "participio"


class MoodCa(StrEnum):
    Condicional = "condicional"
    Gerundi = "gerundi"
    Imperatiu = "imperatiu"
    Indicatiu = "indicatiu"
    Infinitiu = "infinitiu"
    Participi = "particip"
    Subjuntiu = "subjuntiu"


class MoodRo(StrEnum):
    Condițional = "condițional"
    Conjunctiv = "conjunctiv"
    Gerunziu = "gerunziu"
    Imperativ = "imperativ"
    Indicativ = "indicativ"
    Infinitiv = "infinitiv"
    Participiu = "participiu"
    Subjunctiv = "subjunctiv"


class MoodPt(StrEnum):
    Condicional = "condicional"
    Gerúndio = "gerúndio"
    Imperativo = "imperativo"
    Indicativo = "indicativo"
    Infinitivo = "infinitivo"
    Particípio = "particípio"
    Subjuntivo = "subjuntivo"


class Mood:
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
            return MoodCa(s)
        elif lang == Lang.en:
            return MoodEn(s)
        elif lang == Lang.es:
            return MoodEs(s)
        elif lang == Lang.fr:
            return MoodFr(s)
        elif lang == Lang.it:
            return MoodIt(s)
        elif lang == Lang.pt:
            return MoodPt(s)
        elif lang == Lang.ro:
            return MoodRo
