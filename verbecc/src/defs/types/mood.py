import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


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
    Participi = "participi"
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
