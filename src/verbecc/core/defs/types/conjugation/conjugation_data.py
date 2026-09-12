from typing import Optional, Union

from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.pronoun import Pronoun

# ConjugationData is a dict of {"p":Person, "n":Number, "g":Gender, "pr":Pronoun, "c":list[Conjugations]}
#
# This allows us to have one Conjugation for "tú" and another for "vos" e.g.
# {"p":Person.Second, "n":Number.Singular, "g":Gender.m, "pr":"tú", "c":["tú bebes"]],
# {"p":Person.Second, "n":Number.Singular, "g":Gender.m, "pr":"vos", "c":["vos bebés"]],
#
# or one Conjugation for "il" and another for "elle" e.g.
# {"p":Person.Third, "n":Number.Singular, "g":Gender.m, "pr":"il", "c":["il parle"]},
# {"p":Person.Third, "n":Number.Singular, "g":Gender.f, "pr":"elle", "c":["elle parle"]},
#
# Pronoun is omitted for tenses conjugated without pronouns e.g. participle or imperative.
# Person and pronoun are omitted for participle tense.
#
# E.g. French participe passé:
# {"p":None, "n":Number.Singular, "g":Gender.m, None, ["eu"]}
# {"p":None, "n":Number.Plural, "g":Gender.m, None, ["eus"]}
# {"p":None, "n":Number.Singular, "g":Gender.f, None, ["eue"]}
# {"p":None, "n":Number.Plural, "g":Gender.f, None, ["eues"]}
#
# E.g. French imperatif-présent:
# {"p":Person.Second, "n":Number.Singular, "g":None, "pr":None, "c":["aie"]},
# {"p":Person.First, "n":Number.Plural, "g":None, "pr":None, "c":["ayons"]},
# {"p":Person.Second, "n":Number.Plural, "g":None, "pr":None, "c":["ayez"]},
#
# person/number/gender/pronoun are omitted for the inifinitive mood.
#
# E.g. French infinitif-présent:
# {"p":None, "n":None, "g":None, "pr":None "c":["avoir"]}
#

ConjugationKeyPerson = "p"
ConjugationKeyNumber = "n"
ConjugationKeyGender = "g"
ConjugationKeyPronoun = "pr"
ConjugationKeyConjugations = "c"
ConjugationKey = Union[
    ConjugationKeyPerson,
    ConjugationKeyNumber,
    ConjugationKeyGender,
    ConjugationKeyPronoun,
    ConjugationKeyConjugations,
]
ConjugationValue = Union[
    Optional[Person],
    Optional[Number],
    Optional[Gender],
    Optional[Pronoun],
    list[str],
]
ConjugationData = dict[ConjugationKey, ConjugationValue]
