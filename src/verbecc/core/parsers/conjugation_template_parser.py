from typing import Optional

from verbecc.core.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.core.defs.types.data.mood_template import MoodTemplate
from verbecc.core.defs.types.exceptions import ConjugationTemplateError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Mood, MoodFactory
from verbecc.core.parsers.mood_template_parser import MoodTemplateParser
from verbecc.core.parsers.parser import Parser
from verbecc.core.defs.types.data.xml_types import XmlElement
from verbecc.core.utils.xml_utils import xml_element_get_attr, xml_element_get_tag, xml_element_to_string

class ConjugationTemplateParser(Parser):
    def __init__(self, lang: Lang) -> None:
        self.lang = lang

    def parse(self, elem: Optional[XmlElement] = None) -> ConjugationTemplate:
        if elem is None:
            raise ValueError("elem must not be None")
        tag = xml_element_get_tag(elem)
        if tag != "template":
            raise ConjugationTemplateError("Unexpected element")
        try:
            name_attrib = xml_element_get_attr(elem, "name", default=None)
            name = str(name_attrib)
            mood_templates: dict[Mood, MoodTemplate] = {}
            for mood_elem in elem:
                mood_template = MoodTemplateParser(lang=self.lang).parse(mood_elem)
                mood = MoodFactory.from_string(self.lang, xml_element_get_tag(mood_elem).lower())
                mood_templates[mood] = mood_template
            modify_stem = ""
            modify_stem_attrib = xml_element_get_attr(elem, "modify-stem", default=None)
            if modify_stem_attrib is not None:
                modify_stem = str(modify_stem_attrib)
                if modify_stem not in ("strip-accents"):
                    raise ConjugationTemplateError(
                        f"Invalid 'modify-stem' attribute value '{modify_stem}'"
                    )
            else:
                modify_stem = ""
            return ConjugationTemplate(self.lang, name, mood_templates, modify_stem)
        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(xml_element_to_string(elem), str(e))
            )
