from typing import List, Optional, Tuple

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.pronoun import Pronoun, Pronouns

# ConjugationData is a tuple of [Person, Number, Gender, Pronoun, Conjugations]
#
# This allows us to have one PPC for "tú" and another for "vos" e.g.
# [Person.Second, Number.Singular, Gender.m, "tú", ["tú bebes"]],
# [Person.Second, Number.Singular, Gender.m, "vos", ["vos bebés"]],
#
# or one PPC for "il" and another for "elle" e.g.
# [Person.Third, Number.Singular, Gender.m, "il", ["il parle"]],
# [Person.Third, Number.Singular, Gender.f, "elle", ["elle parle"]],
#
# Pronoun is omitted for tenses conjugated without pronouns e.g. participle or imperative.
# Person and pronoun are omitted for participle tense.
#
# E.g. French participe passé:
# [None, Number.Singular, Gender.m, None, ["eu"]]
# [None, Number.Plural, Gender.m, None, ["eus"]]
# [None, Number.Singular, Gender.f, None, ["eue"]]
# [None, Number.Plural, Gender.f, None, ["eues"]]
#
# E.g. French imperatif-présent:
# [Person.Second, Number.Singular, None, None, ["aie"]],
# [Person.First, Number.Plural, None, None, ["ayons"]],
# [Person.Second, Number.Plural, None, None, ["ayez"]],
#
# person/number/gender/pronoun are omitted for the inifinitive mood.
#
# E.g. French infinitif-présent:
# [None, None, None, None ["avoir"]]
#

ConjugationData = Tuple[
    Optional[Person], Optional[Number], Optional[Gender], Optional[Pronoun], List[str]
]
