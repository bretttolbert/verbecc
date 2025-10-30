from lxml import etree
from typing import Dict

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.data.mood_template import MoodTemplate
from verbecc.src.defs.types.mood import MoodFactory
from verbecc.src.parsers.parser import Parser
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser


class MoodTemplateParser(Parser):
    def __init__(self, lang: Lang) -> None:
        self.lang = lang

    def parse(self, elem: etree._Element) -> MoodTemplate:
        mood = MoodFactory.from_string(self.lang, elem.tag.lower())
        tense_templates: Dict[str, TenseTemplate] = {}
        for tense_elem in elem:
            tense_templates[tense_elem.tag] = TenseTemplateParser(
                lang=self.lang, mood=mood
            ).parse(tense_elem)
        return MoodTemplate(self.lang, mood, tense_templates)
