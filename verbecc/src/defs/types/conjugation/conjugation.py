from typing import cast, Iterator, List, Optional, Union

from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.pronoun import Pronoun
from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.conjugation_data import (
    ConjugationData,
    ConjugationKeyPerson,
    ConjugationKeyNumber,
    ConjugationKeyGender,
    ConjugationKeyPronoun,
    ConjugationKeyConjugations,
)


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
        :param conjugations (optional): The list of one or more conjugations.
            The first conjugation is the primary or default conjugation.
            The second conjugation, if present, is the first alternate conjugation.
            There may be any number of alternate conjugations.
            In some languages, the first alternate conjugation is used when
            conjugating the auxiliary verb to form certain compound conjugations.
        """
        super().__init__()
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
            raise TypeError()
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
                tuple(self._conjugations),
            )
        )

    def __getitem__(self, index: int) -> Union[object, str]:
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

    def set_pronoun(self, value: Pronoun) -> None:
        self._pronoun = value

    def get_conjugations(self) -> List[str]:
        return self._conjugations

    def set_conjugations(self, value: List[str]) -> None:
        self._conjugations = value

    def get_data(self) -> ConjugationData:
        return {
            ConjugationKeyConjugations: self._conjugations,
            ConjugationKeyGender: self._gender,
            ConjugationKeyNumber: self._number,
            ConjugationKeyPerson: self._person,
            ConjugationKeyPronoun: self._pronoun,
        }

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb:mood:tense:person:number:gender:pronoun
        E.g. "fr:parler:participe:participe-passé::s:f:"
        E.g. "fr:parler:participe:participe-passé::p:m:"
        E.g. "fr:parler:indicatif:présent:1:s::je"
        E.g. "fr:parler:indicatif:présent:3:s:f:elle"
        """
        _parent_str_id = ""
        parent = self.get_parent()
        if parent is not None:
            _parent_str_id = cast(AbstractConjugation, parent).get_str_id()
        return ":".join(
            [
                str(_parent_str_id),
                "" if self._person is None else str(self._person),
                "" if self._number is None else str(self._number),
                "" if self._gender is None else str(self._gender),
                "" if self._pronoun is None else str(self._pronoun),
            ]
        )

    def set_base_str_id(self, value: str) -> None:
        self._base_str_id = value
