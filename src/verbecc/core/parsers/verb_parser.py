from typing import Optional

from verbecc.core.defs.types.data.verb import Verb
from verbecc.core.defs.types.data.xml_types import XmlElement
from verbecc.core.defs.types.exceptions import VerbsParserError
from verbecc.core.parsers.parser import Parser
from verbecc.core.utils.xml_utils import xml_element_get_tag, xml_element_find, xml_element_get_text, xml_element_to_string


class VerbParser(Parser):
    def __init__(self) -> None:
        pass

    def parse(self, elem: Optional[XmlElement] = None) -> Verb:
        if elem is None:
            raise ValueError("elem must not be None")
        infinitive = ""
        template = ""
        translation_en = ""
        if xml_element_get_tag(elem) != "v":
            raise VerbsParserError("Unexpected element")
        try:
            infinitive : str = ""
            e = xml_element_find(elem, "i")
            if e is not None:
                txt : str | None = xml_element_get_text(e)
                infinitive = txt if txt is not None else ""
            template : str = ""
            e = xml_element_find(elem, "t")
            if e is not None:
                txt : str | None = xml_element_get_text(e)
                template = txt if txt is not None else ""
            translation_en : str = ""
            e = xml_element_find(elem, "en")
            if e is not None:
                txt : str | None = xml_element_get_text(e)
                translation_en = txt if txt is not None else ""
        except AttributeError as e:
            raise VerbsParserError(
                "Error parsing {}: {}".format(xml_element_to_string(elem), str(e))
            )
        return Verb(infinitive, template, translation_en)
