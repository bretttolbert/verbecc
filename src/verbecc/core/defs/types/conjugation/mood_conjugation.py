from typing import cast, Iterable, Optional

from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.core.defs.types.conjugation.mood_conjugation_data import MoodConjugationData


class MoodConjugation(AbstractConjugation):
    """
    The conjugations for a specific mood,
    for a specific verb,
    including alternate conjugations (if applicable).
    """

    def __init__(
        self, mood: Mood, data: Optional[dict[Tense, TenseConjugation]] = None
    ) -> None:
        super().__init__()
        self._mood = mood
        self._data: dict[Tense, TenseConjugation] = {}
        if data is not None:
            for k, v in data.items():
                v.set_parent(self)
                self._data[k] = v

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, MoodConjugation):
            raise TypeError()
        return self._mood == other._mood and self._data == other._data

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._mood, self._data))

    def __getitem__(self, key: Tense) -> TenseConjugation:
        return self._data[key]

    def __setitem__(self, key: Tense, value: TenseConjugation) -> None:
        value.set_parent(self)
        self._data[key] = value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterable[Tense]:
        return iter(self._data)

    def __contains__(self, key: Tense) -> bool:
        return key in self._data

    def get_mood(self) -> Mood:
        return self._mood

    def get_data(self) -> MoodConjugationData:
        return {t: tc.get_data() for t, tc in self._data.items()}

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb:mood
        E.g. "fr:parler:participe"
        E.g. "fr:parler:indicatif"
        """
        _parent_str_id = ""
        parent = self.get_parent()
        if parent is not None:
            _parent_str_id = cast(AbstractConjugation, parent).get_str_id()
        return ":".join([str(_parent_str_id), str(self._mood)])
