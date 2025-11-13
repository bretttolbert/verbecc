from abc import ABC, abstractmethod
from typing import cast, Iterator, Iterable, Union, Dict, List, Optional, Tuple
from jsbeautifier import beautify

from verbecc.src.defs.constants import config
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.gender import Gender
from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts

import json

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
Pronoun = str
ConjugationData = Tuple[
    Optional[Person], Optional[Number], Optional[Gender], Optional[Pronoun], List[str]
]
TenseConjugationData = List[ConjugationData]
MoodConjugationData = Dict[Tense, TenseConjugationData]
MoodsConjugationData = Dict[Mood, MoodConjugationData]  # the "moods" section
VerbInfoData = Dict[str, Union[str, bool, float]]  # the "verb" section
CompleteConjugationData = Dict[str, Union[VerbInfoData, MoodsConjugationData]]


class AbstractConjugation:

    @abstractmethod
    def get_data(self) -> object:
        """The data of this object as primitive types (JSON-serializable)"""
        pass

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """The data of this object as a pretty-formatted JSON string"""
        pretty_json = json.dumps(
            self.get_data(),
            allow_nan=False,
            sort_keys=True,
            indent=4,
            ensure_ascii=config.JSON_OPT_ENSURE_ASCII,
        )
        if config.JSBEAUTIFIER_ENABLE:
            pretty_json = beautify(pretty_json, JSBeautifierOpts.get_opts())
        return pretty_json


class Conjugation(AbstractConjugation):
    """
    The fundamental unit of verbecc representing a single*, specific, inflected conjugation.
    The conjugation(s) for a specific person*, number*, gender* and pronoun*, for a specific
    mood and tense, for a specific verb,
    *including alternate conjugation(s) (if applicable)
    *pronoun is omitted for tenses conjugated without pronouns (e.g. participle or imperative)
    *person/pronoun are omitted for participle tense (only has gender and number)
    *person/number/gender/pronoun are omitted for the infinitive mood
    (e.g. infinitif présent tense)
    """

    def __init__(
        self,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
        pronoun: Optional[Pronoun] = None,
        conjugations: Optional[List[str]] = None,
    ) -> None:
        """
        :param person (optional): The grammatical person, i.e. first, second or third person.
            omitted for the infinitive mood
        :param number (optional): The grammatical number, i.e. singular or plural.
        :param gender (optional): The grammatical gender, i.e. masculine or feminine.
        :param pronoun (optional): The pronoun being conjugated, e.g. "il" vs. "elle" or "tú" vs. "vos",
            omitted if this tense is conjugated without pronouns (e.g. participle or imperative)
        :param conjugations: The list of one or more conjugations.
            The first conjugation is the primary or default conjugation.
            The second conjugation, if present, is the first alternate conjugation.
            There may be any number of alternate conjugations.
            In some languages, the first alternate conjugation is used when
            conjugating the auxiliary verb to form certain compound conjugations.
        """
        self._person = person
        self._number = number
        self._gender = gender
        self._pronoun = pronoun
        if conjugations is not None:
            self._conjugations = conjugations
        else:
            self._conjugations = []

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, Conjugation):
            raise TypeError
        return (
            self._person == other._person
            and self._number == other._number
            and self._gender == other._gender
            and self._pronoun == other._pronoun
            and self._conjugations == other._conjugations
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(
            (
                self._person,
                self._number,
                self._gender,
                self._pronoun,
                self._conjugations,
            )
        )

    def __getitem__(self, index: int) -> object | str:
        """
        Allows accessing elements using square bracket notation.
        Handles both integer indexing and slicing.
        """
        if isinstance(index, slice):
            # If a slice object is provided, return a new MyCustomList
            # containing the sliced portion of the internal data.
            return Conjugation(
                self.person,
                self.number,
                self.gender,
                self.pronoun,
                self._conjugations[index],
            )
        elif isinstance(index, int):
            # If an integer index is provided, return the element at that index.
            # This will automatically raise IndexError if the index is out of range.
            return self._conjugations[index]
        else:
            # Raise a TypeError for unsupported index types.
            raise TypeError("Index must be an integer or a slice object.")

    def __len__(self) -> int:
        return len(self._conjugations)

    def __iter__(self) -> Iterator[str]:
        return iter(self._conjugations)

    def append(self, value: str) -> None:
        self._conjugations.append(value)

    def get_person(self) -> Optional[Person]:
        return self._person

    def set_person(self, value: Person) -> None:
        self._person = value

    def get_number(self) -> Optional[Number]:
        return self._number

    def set_number(self, value: Number) -> None:
        self._number = value

    def get_gender(self) -> Optional[Gender]:
        return self._gender

    def set_gender(self, value: Gender) -> None:
        self._gender = value

    def get_pronoun(self) -> Optional[Pronoun]:
        return self._pronoun

    def set_pronoun(self, value: str) -> None:
        self._pronoun = value

    def get_conjugations(self) -> List[str]:
        return self._conjugations

    def set_conjugations(self, value: List[str]) -> None:
        self._conjugations = value

    def get_data(self) -> ConjugationData:
        return (
            self._person,
            self._number,
            self._gender,
            self._pronoun,
            self._conjugations,
        )


class TenseConjugation(AbstractConjugation):
    """
    The conjugations for a specific mood and tense,
    for a specific verb,
    including alternate conjugations (if applicable).
    """

    def __init__(self, data: Optional[List[Conjugation]] = None) -> None:
        if data is not None:
            self._data = data
        else:
            self._data = []

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, TenseConjugation):
            raise TypeError
        return self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data))

    def __getitem__(self, index: int) -> Conjugation:
        return self._data[index]

    def __setitem__(self, index: int, value: Conjugation) -> None:
        self._data[index] = value

    def __delitem__(self, index: int) -> None:
        del self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Conjugation]:
        return iter(self._data)

    def __contains__(self, value: Conjugation) -> bool:
        return value in self._data

    def append(self, value: Conjugation) -> None:
        self._data.append(value)

    def extend(self, value: Iterable[Conjugation]) -> None:
        self._data.extend(value)

    def get_data(self) -> TenseConjugationData:
        return [p.get_data() for p in self._data]


class MoodConjugation(AbstractConjugation):
    """
    The conjugations for a specific mood,
    for a specific verb,
    including alternate conjugations (if applicable).
    """

    def __init__(self, data: Optional[Dict[Tense, TenseConjugation]] = None) -> None:
        if data is not None:
            self._data = data
        else:
            self._data = {}

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, MoodConjugation):
            raise TypeError
        return self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data))

    def __getitem__(self, key: Tense) -> TenseConjugation:
        return self._data[key]

    def __setitem__(self, key: Tense, value: TenseConjugation) -> None:
        self._data[key] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterable[Tense]:
        return iter(self._data)

    def __contains__(self, key: Tense) -> bool:
        return key in self._data

    def get_data(self) -> MoodConjugationData:
        return {t: tc.get_data() for t, tc in self._data.items()}

    @classmethod
    def combine(cls, a: object, b: object):  # type: ignore
        combined = {}
        for o in (a, b):
            mood_conjugation_instance = cast(MoodConjugation, o)
            combined.update(mood_conjugation_instance._data)
        return cls(combined)


class MoodsConjugation(AbstractConjugation):
    """
    The conjugations for all moods,
    for a specific verb,
    including alternate conjugations (if applicable).
    """

    def __init__(
        self,
        data: Optional[Dict[Mood, MoodConjugation]] = None,
    ) -> None:
        self._data = {}
        if data is not None:
            self._data = data

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, MoodsConjugation):
            raise TypeError
        return self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data))

    def __getitem__(self, key: Mood) -> MoodConjugation:
        return self._data[key]

    def __setitem__(self, key: Mood, value: MoodConjugation) -> None:
        self._data[key] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterable[Mood]:
        return iter(self._data)

    def __contains__(self, key: Mood) -> bool:
        return key in self._data

    def get_data(self) -> MoodsConjugationData:
        return {m: mc.get_data() for m, mc in self._data.items()}


class VerbInfo(AbstractConjugation):
    infinitive: str
    predicted: bool
    pred_score: float
    template: str
    translation_en: str
    stem: str

    def __init__(
        self,
        infinitive: str,
        predicted: bool,
        pred_score: float,
        template: str,
        translation_en: str,
        stem: str,
    ) -> None:
        self.infinitive = infinitive
        self.predicted = predicted
        self.pred_score = pred_score
        self.template = template
        self.translation_en = translation_en
        self.stem = stem

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, VerbInfo):
            raise TypeError
        return (
            self.infinitive == other.infinitive
            and self.predicted == other.predicted
            and self.pred_score == other.pred_score
            and self.template == other.template
            and self.translation_en == other.translation_en
            and self.stem == other.stem
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(
            (
                self.infinitive,
                self.predicted,
                self.pred_score,
                self.template,
                self.translation_en,
                self.stem,
            )
        )

    def get_data(self) -> VerbInfoData:
        return {
            "infinitive": self.infinitive,
            "predicted": self.predicted,
            "pred_score": self.pred_score,
            "template": self.template,
            "translation_en": self.translation_en,
            "stem": self.stem,
        }


class CompleteConjugation(AbstractConjugation):

    def __init__(
        self,
        verb_info: VerbInfo,
        moods_conjugation: MoodsConjugation,
    ) -> None:
        self._verb_info = verb_info
        self._moods_conjugation = moods_conjugation

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, CompleteConjugation):
            raise TypeError
        return (
            self._verb_info == other._verb_info
            and self._moods_conjugation == other._moods_conjugation
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._verb_info, self._moods_conjugation))

    def get_verb_info(self) -> VerbInfo:
        return self._verb_info

    def get_moods(self) -> MoodsConjugation:
        return self._moods_conjugation

    def get_data(self) -> CompleteConjugationData:
        return {
            "verb": self._verb_info.get_data(),
            "moods": self._moods_conjugation.get_data(),
        }
