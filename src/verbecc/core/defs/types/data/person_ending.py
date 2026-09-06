from typing import Optional, cast

from verbecc.core.defs.types.data.element import Element
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.gender import Gender


class PersonEnding(Element):
    """
    person: The grammatical person of this conjugation ending.
        person will be None if this is a participle tense.
    number: The grammatical number of this conjugation ending.
    gender: The gender of this person ending.
        gender will be None unless this is a participle tense.

    Participle tense endings only have gender and number.
    All other tense endings only have person and number.

    Ending for a specific grammatical person and number,
    for a specific verb template, mood, tense
    May also have one or more alternate endings for an alternative spellings
    or regional variations.
    E.g. Endings for aim:er indicatif présent 2nd Person Plural = ['ez']
    E.g. Endings for pa:yer indicatif présent 1st Person Singular = ['ie', 'ye']
    Explanation: 'ye' is an alternate spelling (je paie, je paye)
    person
    """

    def __init__(
        self,
        person: Optional[Person | str],
        number: Optional[Number | str],
        gender: Optional[Gender | str],
        endings: list[str],
    ) -> None:
        self.person = cast(Optional[Person], person)
        self.number = cast(Optional[Number], number)
        self.gender = cast(Optional[Gender], gender)
        self.endings = endings

    def get_person(self) -> Optional[Person]:
        return self.person

    def get_number(self) -> Optional[Number]:
        return self.number

    def get_gender(self) -> Optional[Gender]:
        return self.gender

    def get_endings(self) -> list[str]:
        return self.endings

    def get_ending(self) -> str:
        return self.endings[0]

    def get_alternate_ending_if_available(self) -> str:
        if len(self.endings) > 1:
            return self.endings[1]
        return self.endings[0]

    def __repr__(self) -> str:
        return f"person={self.person} number={self.number} gender={self.gender} endings={self.endings}"
