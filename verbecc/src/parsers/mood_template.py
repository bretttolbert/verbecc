from lxml import etree
from typing import Dict

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser
from verbecc.src.defs.types.mood import MoodFactory


class MoodTemplate:
    def __init__(self, lang: Lang, mood_elem: etree._Element) -> None:
        self.lang = lang
        self.mood = MoodFactory.from_string(self.lang, mood_elem.tag.lower())
        self.tense_templates: Dict[str, TenseTemplate] = {}
        for tense_elem in mood_elem:
            self.tense_templates[tense_elem.tag] = TenseTemplateParser(
                lang=lang, mood=self.mood
            ).parse(tense_elem)

    def __repr__(self) -> str:
        return "mood={} tense_templates={}".format(self.mood, self.tense_templates)
