import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from typing import Dict, Tuple, Union

from verbecc.src.defs.types.language import Lanugage
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.person import Person

# map of ISO 639 codes to long names (in target language)
SUPPORTED_LANGUAGES: Dict[Lanugage, str] = {
    Lanugage.Catalan: "català",
    Lanugage.Spanish: "español",
    Lanugage.French: "français",
    Lanugage.Italian: "italiano",
    Lanugage.Portuguese: "português",
    Lanugage.Romanian: "română",
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
    "fr": {"vowels": "aáàâeêéèiîïoôöœuûùy", "consonants": "bcçdfghjklmnpqrstvwxyz"},
    "en": {"vowels": "aeiouy", "consonants": "bcdfghjklmnpqrstvwxyz"},
    "ca": {"vowels": "aáàâeéèiïoôuûùy", "consonants": "bcdfghjklmnñpqrstvwxyz"},
    "es": {"vowels": "aáeiíoóuúy", "consonants": "bcdfghjklmnñpqrstvwxyz"},
    "it": {"vowels": "aàeéèiìîoóòuùy", "consonants": "bcdfghjklmnpqrstvwxyz"},
    "pt": {"vowels": "aàãááeêéiíoóõuúy", "consonants": "bcçdfghjklmnpqrstvwxyz"},
    "ro": {"vowels": "aăâeiîouy", "consonants": "bcdfghjklmnpqrsșştțţvwxyz"},
}
