from lxml import etree
from typing import Dict

from verbecc.src.parsers.tense_template import TenseTemplate


class MoodTemplate:
    def __init__(self, mood_elem: etree._Element) -> None:
        self.name = mood_elem.tag.lower()
        self.tense_templates: Dict[str, TenseTemplate] = {}
        for tense_elem in mood_elem:  # type: ignore
            self.tense_templates[tense_elem.tag] = TenseTemplate(tense_elem)

    def __repr__(self) -> str:
        return "name={} tense_templates={}".format(self.name, self.tense_templates)
