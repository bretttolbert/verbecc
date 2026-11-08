from verbecc.core.defs.types.data.element import Element
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense


class MoodTemplate(Element):
    def __init__(
        self, lang: Lang, mood: Mood, tense_templates: dict[Tense, TenseTemplate]
    ) -> None:
        self.lang = lang
        self.mood = mood
        self.tense_templates = tense_templates

    def __repr__(self) -> str:
        return (
            f"lang={self.lang} mood={self.mood} tense_templates={self.tense_templates}"
        )
