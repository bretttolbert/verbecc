from verbecc.src.utils.string_utils import strip_accents
from verbecc.src.defs.types.data.element import Element


class Verb(Element):
    def __init__(
        self, infinitive: str, template: str, translation_en: str = ""
    ) -> None:
        self.predicted = False
        self.pred_score = 1.0
        self.infinitive = infinitive
        self.infinitive_no_accents = strip_accents(self.infinitive)
        self.template = template
        self.translation_en = translation_en
        self.impersonal = False

    def __repr__(self) -> str:
        return "infinitive={} infinitive_no_accents={} template={} translation_en={} impersonal={} predicted={} pred_score={}".format(
            self.infinitive,
            self.infinitive_no_accents,
            self.template,
            self.translation_en,
            self.impersonal,
            self.predicted,
            self.pred_score,
        )
