from typing import Iterable, Dict, Optional

from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.src.defs.types.conjugation.moods_conjugation_data import (
    MoodsConjugationData,
)


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
