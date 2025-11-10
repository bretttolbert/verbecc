from typing import List

from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number


class PersonEnding(Element):
    """
    Ending for a specific grammatical person and number,
    for a specific verb template, mood, tense
    May also have one or more alternate endings for an alternative spellings
    or regional variations.
    E.g. Endings for aim:er indicatif présent 2nd Person Plural = ['ez']
    E.g. Endings for pa:yer indicatif présent 1st Person Singular = ['ie', 'ye']
    Explanation: 'ye' is an alternate spelling (je paie, je paye)
    person
    A grammar_defines.PERSONS value indicating which person
    this PersonEnding is for, e.g. for aim:er, "ez" is '2p' (second person plural)
    """

    def __init__(self, person: Person, number: Number, endings: List[str]) -> None:
        self.person = person
        self.number = number
        self.endings = endings

    def get_person(self) -> Person:
        return self.person

    def get_number(self) -> Number:
        return self.number

    def get_endings(self) -> List[str]:
        return self.endings

    def get_ending(self) -> str:
        return self.endings[0]

    def get_alternate_ending_if_available(self) -> str:
        if len(self.endings) > 1:
            return self.endings[1]
        return self.endings[0]

    def __repr__(self) -> str:
        return f"person={self.person} number={self.number} endings={self.endings}"
