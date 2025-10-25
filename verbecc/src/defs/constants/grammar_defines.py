import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from typing import Dict, List, Tuple

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
# for most moods and tenses
# Exceptions: imperative and participle
# Note: 'usted' is grammatically 3s despite being semantically 2s
# Note: 'usteded' is grammatically 3p despite being semantically 2p
PERSONS: Tuple[Person, Person, Person, Person, Person, Person] = (
    Person.FirstPersonSingular,
    Person.SecondPersonSingular,
    Person.ThirdPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
    Person.ThirdPersonPlural,
)

# e.g. manger : mange, mangeons, mangez
IMPERATIVE_PERSONS_FR: Tuple[Person, Person, Person] = (
    Person.SecondPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
)

# e.g. habla, hable, hablemos, hablad, hablen
IMPERATIVE_PERSONS_ES: Tuple[Person, Person, Person, Person, Person] = (
    Person.SecondPersonSingular,
    Person.ThirdPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
    Person.ThirdPersonPlural,
)

# e.g. habla, habli, hablem, hableu, hablin
IMPERATIVE_PERSONS_CA = IMPERATIVE_PERSONS_ES

# e.g. -, sii, sia, siamo, siate, siano
# Italian currently has the "-" placeholder for the 1s unlike French and Spanish
# TODO: Make them consistent
IMPERATIVE_PERSONS_IT: Tuple[Person, Person, Person, Person, Person, Person] = (
    Person.FirstPersonSingular,
    Person.SecondPersonSingular,
    Person.ThirdPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural,
    Person.ThirdPersonPlural,
)

# e.g. -, sê tu, seja você, sejamos nós, sede vós, sejam vocês
# Portuguese currently has the "-" placeholder for the 1s like Italian and unlike French and Spanish
# TODO: Make them consistent
IMPERATIVE_PERSONS_PT = IMPERATIVE_PERSONS_IT

# The Romanian imperative is used for commands and requests and
# is formed primarily using the second person verb forms.
IMPERATIVE_PERSONS_RO: Tuple[Person, Person] = (
    Person.SecondPersonSingular,
    Person.SecondPersonPlural,
)

IMPERATIVE_PERSONS: Dict[LangCodeISO639_1, List[Person]] = {
    LangCodeISO639_1.fr: IMPERATIVE_PERSONS_FR,
    LangCodeISO639_1.es: IMPERATIVE_PERSONS_ES,
    LangCodeISO639_1.ca: IMPERATIVE_PERSONS_CA,
    LangCodeISO639_1.it: IMPERATIVE_PERSONS_IT,
    LangCodeISO639_1.pt: IMPERATIVE_PERSONS_PT,
    LangCodeISO639_1.ro: IMPERATIVE_PERSONS_IT,
}

# Default order of participle inflections in XML
# Currently overridden by some langs because the XML
# templates are inconsistent (TODO: Standardize the XML files)
# Default order is like French XML file, i.e. MS, MP, FS, FP
# But in some lang XML files, e.g. Italian, the order is MS, FS, MP, FP,
PARTICIPLE_INFLECTIONS_DEFAULT: Tuple[
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

PARTICIPLE_INFLECTION_FR = PARTICIPLE_INFLECTIONS_DEFAULT
PARTICIPLE_INFLECTION_ES = PARTICIPLE_INFLECTIONS_DEFAULT
PARTICIPLE_INFLECTION_PT = PARTICIPLE_INFLECTIONS_DEFAULT
PARTICIPLE_INFLECTION_CA = PARTICIPLE_INFLECTIONS_DEFAULT
PARTICIPLE_INFLECTION_RO = PARTICIPLE_INFLECTIONS_DEFAULT
PARTICIPLE_INFLECTION_IT: Tuple[
    ParticipleInflection,
    ParticipleInflection,
    ParticipleInflection,
    ParticipleInflection,
] = (
    ParticipleInflection.MasculineSingular,
    ParticipleInflection.FeminineSingular,
    ParticipleInflection.MasculinePlural,
    ParticipleInflection.FemininePlural,
)

PARTICIPLE_INFLECTIONS: Dict[LangCodeISO639_1, List[Person]] = {
    LangCodeISO639_1.fr: PARTICIPLE_INFLECTION_FR,
    LangCodeISO639_1.es: PARTICIPLE_INFLECTION_ES,
    LangCodeISO639_1.ca: PARTICIPLE_INFLECTION_CA,
    LangCodeISO639_1.it: PARTICIPLE_INFLECTION_IT,
    LangCodeISO639_1.pt: PARTICIPLE_INFLECTION_PT,
    LangCodeISO639_1.ro: PARTICIPLE_INFLECTION_RO,
}

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
