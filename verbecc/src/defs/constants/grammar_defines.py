import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from typing import Dict, Tuple

from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person

# map of ISO 639-1 codes to long names (in target language)
SUPPORTED_LANGUAGES: Dict[LangCodeISO639_1, str] = {
    LangCodeISO639_1.ca: "català",
    LangCodeISO639_1.es: "español",
    LangCodeISO639_1.fr: "français",
    LangCodeISO639_1.it: "italiano",
    LangCodeISO639_1.pt: "português",
    LangCodeISO639_1.ro: "română",
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
    LangCodeISO639_1.fr: {
        "vowels": "aáàâeêéèiîïoôöœuûùy",
        "consonants": "bcçdfghjklmnpqrstvwxyz",
    },
    LangCodeISO639_1.en: {
        "vowels": "aeiouy",
        "consonants": "bcdfghjklmnpqrstvwxyz",
    },
    LangCodeISO639_1.ca: {
        "vowels": "aáàâeéèiïoôuûùy",
        "consonants": "bcdfghjklmnñpqrstvwxyz",
    },
    LangCodeISO639_1.es: {
        "vowels": "aáeiíoóuúy",
        "consonants": "bcdfghjklmnñpqrstvwxyz",
    },
    LangCodeISO639_1.es: {
        "vowels": "aàeéèiìîoóòuùy",
        "consonants": "bcdfghjklmnpqrstvwxyz",
    },
    LangCodeISO639_1.pt: {
        "vowels": "aàãááeêéiíoóõuúy",
        "consonants": "bcçdfghjklmnpqrstvwxyz",
    },
    LangCodeISO639_1.ro: {
        "vowels": "aăâeiîouy",
        "consonants": "bcdfghjklmnpqrsșştțţvwxyz",
    },
}
