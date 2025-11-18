import json
from typing import Iterable

from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.verb_info import VerbInfo
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.src.defs.types.conjugation.moods_conjugation import MoodsConjugation
from verbecc.src.defs.types.conjugation.complete_conjugation_data import (
    CompleteConjugationData,
)
from verbecc.src.utils.config_utils import ConfigUtils

config = ConfigUtils.load_verbecc_config()


class CompleteConjugation(AbstractConjugation):

    def __init__(
        self,
        verb_info: VerbInfo,
        moods_conjugation: MoodsConjugation,
    ) -> None:
        super().__init__()
        verb_info.set_parent(self)
        self._verb_info = verb_info
        moods_conjugation.set_parent(self)
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

    def __getitem__(self, key: Mood) -> MoodConjugation:
        return self._moods_conjugation[key]

    def __setitem__(self, key: Mood, value: MoodConjugation) -> None:
        self._moods_conjugation[key] = value

    def __len__(self) -> int:
        return len(self._moods_conjugation)

    def __iter__(self) -> Iterable[Mood]:
        return iter(self._moods_conjugation._data)

    def __contains__(self, key: Mood) -> bool:
        return key in self._moods_conjugation

    def get_verb_info(self) -> VerbInfo:
        return self._verb_info

    def get_moods(self) -> MoodsConjugation:
        return self._moods_conjugation

    def get_data(self) -> CompleteConjugationData:
        return {
            "verb": self._verb_info.get_data(),
            "moods": self._moods_conjugation.get_data(),
        }

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb
        E.g. "fr:parler"
        E.g. "fr:parler"
        """
        # This is the root node, so it has no parent.
        return self._verb_info.get_str_id()
