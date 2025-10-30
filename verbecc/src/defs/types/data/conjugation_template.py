from typing import List

from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.data.mood_template import MoodTemplate


class ConjugationTemplate(Element):
    def __init__(
        self,
        lang: Lang,
        name: str,
        mood_templates: List[MoodTemplate],
        modify_stem: str = "",
    ) -> None:
        self.lang = lang
        self.name = name
        self.mood_templates = mood_templates
        self.modify_stem = modify_stem

    def __repr__(self) -> str:
        return f"lang={self.lang} name={self.name} mood_templates={self.mood_templates} modify_stem={self.modify_stem}"
