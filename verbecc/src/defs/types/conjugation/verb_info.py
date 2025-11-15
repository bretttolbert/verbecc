from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.verb_info_data import VerbInfoData


class VerbInfo(AbstractConjugation):
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

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        elif not isinstance(other, VerbInfo):
            raise TypeError
        return (
            self.infinitive == other.infinitive
            and self.predicted == other.predicted
            and self.pred_score == other.pred_score
            and self.template == other.template
            and self.translation_en == other.translation_en
            and self.stem == other.stem
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(
            (
                self.infinitive,
                self.predicted,
                self.pred_score,
                self.template,
                self.translation_en,
                self.stem,
            )
        )

    def get_data(self) -> VerbInfoData:
        return {
            "infinitive": self.infinitive,
            "predicted": self.predicted,
            "pred_score": self.pred_score,
            "template": self.template,
            "translation_en": self.translation_en,
            "stem": self.stem,
        }
