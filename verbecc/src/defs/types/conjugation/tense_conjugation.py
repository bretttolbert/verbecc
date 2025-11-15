from typing import Iterable, Iterator, List, Optional

from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.conjugation import Conjugation
from verbecc.src.defs.types.conjugation.tense_conjugation_data import (
    TenseConjugationData,
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
