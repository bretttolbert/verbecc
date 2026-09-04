from typing import List

from verbecc.core.defs.types.data.element import Element
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number


class TenseTemplate(Element):

    def __init__(
        self,
        lang: Lang,
        mood: Mood,
        tense: Tense,
        person_endings: list[PersonEnding],
    ) -> None:
        self.lang = lang
        self.mood = mood
        self.tense = tense
        self.person_endings = person_endings

    def get_person_ending(self, person: Person, number: Number) -> PersonEnding:
        for pe in self.person_endings:
            if pe.person == person and pe.number == number:
                return pe
        raise ValueError(
            f"TenseTemplate has no PersonEnding for person={person} number={number}"
        )

    def __repr__(self) -> str:
        return f"lang={self.lang} mood={self.mood} tense={self.tense} person_endings={self.person_endings}"
