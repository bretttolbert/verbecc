from typing import Dict

from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense


class MoodTemplate(Element):
    def __init__(
        self, lang: Lang, mood: Mood, tense_templates: Dict[Tense, TenseTemplate]
    ) -> None:
        self.lang = lang
        self.mood = mood
        self.tense_templates = tense_templates

    def __repr__(self) -> str:
        return (
            f"lang={self.lang} mood={self.mood} tense_templates={self.tense_templates}"
        )
