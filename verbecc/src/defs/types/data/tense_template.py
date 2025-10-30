from typing import List

from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.person import Person


class TenseTemplate(Element):

    def __init__(
        self, lang: Lang, mood: Mood, tense: Tense, person_endings: List[PersonEnding]
    ) -> None:
        self.lang = lang
        self.mood = mood
        self.tense = tense
        self.person_endings = person_endings

    def get_person_ending(self, person: Person) -> PersonEnding:
        for pe in self.person_endings:
            if pe.person == person:
                return pe
        raise ValueError(
            "TenseTemplate '{}' has no PersonEnding for person '{}'".format(
                self.name, person
            )
        )

    def __repr__(self) -> str:
        return f"lang={self.lang} mood={self.mood} tense={self.tense} person_endings={self.person_endings}"
