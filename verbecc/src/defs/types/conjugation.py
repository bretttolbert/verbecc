from typing import Union, Dict, List

from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense

import json


# PersonConjugation format depends on AlternatesBehavior
# With AlternatesBehavior.All, its a List[str]
# With AlternatesBehavior.FirstOnly or SecondOnly, it's a str
PersonConjugation = Union[List[str], str]
TenseConjugation = List[PersonConjugation]
MoodConjugation = Dict[Tense, TenseConjugation]
MoodsConjugation = Dict[Mood, MoodConjugation]  # the "moods" section
ConjugationInfoData = Dict[str, Union[str, bool, float]]  # the "verb" section
Conjugation = Dict[str, Union[ConjugationInfoData, MoodsConjugation]]


class ConjugationInfo:
    infinitive: str
    predicted: bool
    pred_score: float
    template: str
    translation_en: str
    stem: str

    def __init__(
        self,
        infinitive: str,
        predicted: bool,
        pred_score: float,
        template: str,
        translation_en: str,
        stem: str,
    ) -> None:
        self.infinitive = infinitive
        self.predicted = predicted
        self.pred_score = pred_score
        self.template = template
        self.translation_en = translation_en
        self.stem = stem

    def __str__(self) -> str:
        return json.dumps(
            self,
            allow_nan=False,
            sort_keys=True,
            indent=4,
        )

    @property
    def data(self) -> ConjugationInfoData:
        return {
            "infinitive": self.infinitive,
            "predicted": self.predicted,
            "pred_score": self.pred_score,
            "template": self.template,
            "translation_en": self.translation_en,
            "stem": self.stem,
        }
