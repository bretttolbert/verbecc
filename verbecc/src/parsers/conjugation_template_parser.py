from lxml import etree
from typing import Dict, Optional


from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.data.mood_template import MoodTemplate
from verbecc.src.defs.types.exceptions import ConjugationTemplateError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Mood, MoodFactory
from verbecc.src.parsers.mood_template_parser import MoodTemplateParser
from verbecc.src.parsers.parser import Parser


class ConjugationTemplateParser(Parser):
    def __init__(self, lang: Lang) -> None:
        self.lang = lang

    def parse(self, elem: Optional[etree._Element] = None) -> ConjugationTemplate:
        if elem is None:
            raise ValueError("elem must not be None")
        if elem.tag != "template":
            raise ConjugationTemplateError("Unexpected element")
        try:
            name_attrib = elem.get("name", default=None)
            name = str(name_attrib)
            mood_templates: Dict[Mood, MoodTemplate] = {}
            for mood_elem in elem:
                mood_template = MoodTemplateParser(lang=self.lang).parse(mood_elem)
                mood = MoodFactory.from_string(self.lang, mood_elem.tag.lower())
                mood_templates[mood] = mood_template
            modify_stem = ""
            modify_stem_attrib = elem.get("modify-stem", default=None)
            if modify_stem_attrib is not None:
                modify_stem = str(modify_stem_attrib)
                if modify_stem not in ("strip-accents"):
                    raise ConjugationTemplateError(
                        "Invalid 'modify-stem' attribute value '{self.modify_stem}'"
                    )
            else:
                modify_stem = ""
            return ConjugationTemplate(self.lang, name, mood_templates, modify_stem)
        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(etree.tostring(elem), str(e))
            )
