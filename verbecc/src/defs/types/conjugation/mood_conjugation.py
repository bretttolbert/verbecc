from typing import cast, Dict, Iterable, Optional

from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.mood_conjugation_data import MoodConjugationData


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
