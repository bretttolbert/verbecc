import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from typing import Dict, Tuple

from verbecc.src.defs.types.language_codes import LangISOCode639_1
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person

# map of ISO 639-1 codes to long names (in target language)
SUPPORTED_LANGUAGES: Dict[LangISOCode639_1, str] = {
    LangISOCode639_1.Ca: "català",
    LangISOCode639_1.Es: "español",
    LangISOCode639_1.Fr: "français",
    LangISOCode639_1.It: "italiano",
    LangISOCode639_1.Pt: "português",
    LangISOCode639_1.Ro: "română",
}

# Order of grammatical persons in data structures
# Note: 'usted' is 3s despite being semantically 2p
PERSONS: Tuple[Person, Person, Person, Person, Person, Person] = (
    Person.FirstPersonSingular,
    Person.SecondPersonSingular,
    Person.ThirdPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
    Person.ThirdPersonPlural,
)

IMPERATIVE_PRESENT_PERSONS: Tuple[Person, Person, Person] = (
    Person.SecondPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
)

# Order of participle inflections in XML
PARTICIPLE_INFLECTIONS: Tuple[
    ParticipleInflection,
    ParticipleInflection,
    ParticipleInflection,
    ParticipleInflection,
] = (
    ParticipleInflection.MasculineSingular,
    ParticipleInflection.MasculinePlural,
    ParticipleInflection.FeminineSingular,
    ParticipleInflection.FemininePlural,
)

ALPHABET = {
    LangISOCode639_1.Fr: {
        "vowels": "aáàâeêéèiîïoôöœuûùy",
        "consonants": "bcçdfghjklmnpqrstvwxyz",
    },
    LangISOCode639_1.En: {
        "vowels": "aeiouy",
        "consonants": "bcdfghjklmnpqrstvwxyz",
    },
    LangISOCode639_1.Ca: {
        "vowels": "aáàâeéèiïoôuûùy",
        "consonants": "bcdfghjklmnñpqrstvwxyz",
    },
    LangISOCode639_1.Es: {
        "vowels": "aáeiíoóuúy",
        "consonants": "bcdfghjklmnñpqrstvwxyz",
    },
    LangISOCode639_1.Es: {
        "vowels": "aàeéèiìîoóòuùy",
        "consonants": "bcdfghjklmnpqrstvwxyz",
    },
    LangISOCode639_1.Pt: {
        "vowels": "aàãááeêéiíoóõuúy",
        "consonants": "bcçdfghjklmnpqrstvwxyz",
    },
    LangISOCode639_1.Ro: {
        "vowels": "aăâeiîouy",
        "consonants": "bcdfghjklmnpqrsșştțţvwxyz",
    },
}
