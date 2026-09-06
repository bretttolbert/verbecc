from typing import Optional

from verbecc.core.defs.types.data.mood_template import MoodTemplate
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import MoodFactory
from verbecc.core.defs.types.tense import TenseFactory
from verbecc.core.defs.types.tense import Tense
from verbecc.core.parsers.parser import Parser
from verbecc.core.parsers.tense_template_parser import TenseTemplateParser

from verbecc.core.defs.types.data.xml_types import XmlElement
from verbecc.core.utils.xml_utils import xml_element_get_tag

class MoodTemplateParser(Parser):
    def __init__(self, lang: Lang) -> None:
        self.lang = lang

    def parse(self, elem: Optional[XmlElement] = None) -> MoodTemplate:
        if elem is None:
            raise ValueError
        mood = MoodFactory.from_string(self.lang, xml_element_get_tag(elem).lower())
        tense_templates: dict[Tense, TenseTemplate] = {}
        for tense_elem in elem:
            tense = TenseFactory.from_string(self.lang, xml_element_get_tag(tense_elem).lower())
            tense_templates[tense] = TenseTemplateParser(
                lang=self.lang, mood=mood
            ).parse(tense_elem)
        return MoodTemplate(self.lang, mood, tense_templates)
