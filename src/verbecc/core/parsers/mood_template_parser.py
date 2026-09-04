from lxml import etree
from typing import Optional

from verbecc.core.defs.types.data.mood_template import MoodTemplate
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import MoodFactory
from verbecc.core.defs.types.tense import TenseFactory
from verbecc.core.defs.types.tense import Tense
from verbecc.core.parsers.parser import Parser
from verbecc.core.parsers.tense_template_parser import TenseTemplateParser


class MoodTemplateParser(Parser):
    def __init__(self, lang: Lang) -> None:
        self.lang = lang

    def parse(self, elem: Optional[etree._Element] = None) -> MoodTemplate:
        if elem is None:
            raise ValueError
        mood = MoodFactory.from_string(self.lang, elem.tag.lower())
        tense_templates: dict[Tense, TenseTemplate] = {}
        for tense_elem in elem:
            tense = TenseFactory.from_string(self.lang, tense_elem.tag.lower())
            tense_templates[tense] = TenseTemplateParser(
                lang=self.lang, mood=mood
            ).parse(tense_elem)
        return MoodTemplate(self.lang, mood, tense_templates)
