from typing import cast, Iterable, Iterator, Optional

from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.core.defs.types.conjugation.conjugation import Conjugation
from verbecc.core.defs.types.conjugation.tense_conjugation_data import (
    TenseConjugationData,
)


class TenseConjugation(AbstractConjugation):
    """
    The conjugations for a specific mood and tense,
    for a specific verb,
    including alternate conjugations (if applicable).
    """

    def __init__(self, tense: Tense, data: Optional[list[Conjugation]] = None) -> None:
        super().__init__()
        self._tense = tense
        self._data: list[Conjugation] = []
        if data is not None:
            for c in data:
                c.set_parent(self)
                self._data.append(c)

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, TenseConjugation):
            raise TypeError()
        return self._tense == other._tense and self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data))

    def __getitem__(self, index: int) -> Conjugation:
        return self._data[index]

    def __setitem__(self, index: int, value: Conjugation) -> None:
        value.set_parent(self)
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
        value.set_parent(self)
        self._data.append(value)

    def extend(self, values: Iterable[Conjugation]) -> None:
        for value in values:
            value.set_parent(self)
            self._data.append(value)

    def get_data(self) -> TenseConjugationData:
        return [p.get_data() for p in self._data]

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb:mood:tense
        E.g. "fr:parler:participe:participe-passé"
        E.g. "fr:parler:indicatif:présent"
        """
        _parent_str_id = ""
        parent = self.get_parent()
        if parent is not None:
            _parent_str_id = cast(AbstractConjugation, parent).get_str_id()
        return ":".join([str(_parent_str_id), str(self._tense)])
