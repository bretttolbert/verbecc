from lxml import etree
from typing import Dict

from verbecc.src.parsers.mood_template import MoodTemplate
from verbecc.src.defs.types.exceptions import ConjugationTemplateError
from verbecc.src.defs.types.mood import Mood


class ConjugationTemplate:
    def __init__(self, template_elem: etree._Element) -> None:
        if template_elem.tag != "template":
            raise ConjugationTemplateError("Unexpected element")
        try:
            name_attrib = template_elem.get("name", default=None)
            self.name = str(name_attrib)
            self.mood_templates: Dict[Mood, MoodTemplate] = {}
            for mood_elem in template_elem:  # type: ignore
                mood_template = MoodTemplate(mood_elem)
                self.mood_templates[mood_elem.tag.lower()] = mood_template
            self.modify_stem = ""
            modify_stem_attrib = template_elem.get("modify-stem", default=None)
            if modify_stem_attrib is not None:
                self.modify_stem = str(modify_stem_attrib)
                if self.modify_stem not in ("strip-accents"):
                    raise ConjugationTemplateError(
                        "Invalid 'modify-stem' attribute value '{self.modify_stem}'"
                    )
            else:
                self.modify_stem = ""

        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(etree.tostring(template_elem), str(e))
            )

    def __repr__(self) -> str:
        return "name={} mood_templates={}".format(self.name, self.mood_templates)
