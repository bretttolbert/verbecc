from typing import cast, Iterable, Optional

from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.core.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.core.defs.types.conjugation.moods_conjugation_data import (
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
        data: Optional[dict[Mood, MoodConjugation]] = None,
    ) -> None:
        super().__init__()
        self._data: dict[Mood, MoodConjugation] = {}
        if data is not None:
            for k, v in data.items():
                v.set_parent(self)
                self._data[k] = v

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, MoodsConjugation):
            raise TypeError()
        return self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data))

    def __getitem__(self, key: Mood) -> MoodConjugation:
        return self._data[key]

    def __setitem__(self, key: Mood, value: MoodConjugation) -> None:
        value.set_parent(self)
        self._data[key] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterable[Mood]:
        return iter(self._data)

    def __contains__(self, key: Mood) -> bool:
        return key in self._data

    def get_data(self) -> MoodsConjugationData:
        return {m: mc.get_data() for m, mc in self._data.items()}

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb
        E.g. "fr:parler"
        E.g. "fr:parler"
        """
        _parent_str_id = ""
        parent = self.get_parent()
        if parent is not None:
            _parent_str_id = cast(AbstractConjugation, parent).get_str_id()
        return ":".join([str(_parent_str_id)])
