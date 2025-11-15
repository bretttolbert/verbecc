from verbecc.src.defs.types.conjugation.abstract_conjugation import AbstractConjugation
from verbecc.src.defs.types.conjugation.verb_info_data import VerbInfoData
from verbecc.src.defs.types.lang_code import LangCodeISO639_1


class VerbInfo(AbstractConjugation):
    lang: LangCodeISO639_1
    infinitive: str
    predicted: bool
    pred_score: float
    template: str
    translation_en: str
    stem: str

    def __init__(
        self,
        lang: LangCodeISO639_1,
        infinitive: str,
        predicted: bool,
        pred_score: float,
        template: str,
        translation_en: str,
        stem: str,
    ) -> None:
        super().__init__()
        self.lang = lang
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
            self.lang == other.lang
            and self.infinitive == other.infinitive
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
                self.lang,
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
            "lang": self.lang,
            "infinitive": self.infinitive,
            "predicted": self.predicted,
            "pred_score": self.pred_score,
            "template": self.template,
            "translation_en": self.translation_en,
            "stem": self.stem,
        }

    def get_str_id(self) -> str:
        """
        Return unique string identifier consisting of
        lang:verb
        E.g. "fr:parler"
        E.g. "fr:parler"
        """
        # This singleton info node represents the root node, so it has no parent.
        _str_id = ""
        return ":".join([str(self.lang), str(self.infinitive)])
