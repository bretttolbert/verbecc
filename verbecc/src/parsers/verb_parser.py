from lxml import etree
from lxml.etree import Element

from verbecc.src.parsers.parser import Parser
from verbecc.src.defs.types.exceptions import VerbsParserError
from verbecc.src.defs.types.data.verb import Verb


class VerbParser(Parser):
    def __init__(self) -> None:
        pass

    def parse(self, elem: etree._Element) -> Verb:
        infinitive = ""
        template = ""
        translation_en = ""
        if elem.tag != "v":
            raise VerbsParserError("Unexpected element")
        try:
            infinitive = ""
            e = elem.find("i", None)
            if e is not None:
                infinitive = e.text if e.text is not None else ""
            template = ""
            e = elem.find("t", None)
            if e is not None:
                template = e.text if e.text is not None else ""
            translation_en = ""
            e = elem.find("en", None)
            if e is not None:
                translation_en = e.text if e.text is not None else ""
        except AttributeError as e:
            raise VerbsParserError(
                "Error parsing {}: {}".format(etree.tostring(elem), str(e))
            )
        return Verb(infinitive, template, translation_en)
