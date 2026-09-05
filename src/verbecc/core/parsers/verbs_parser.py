from __future__ import print_function
from io import BytesIO
try:
    # Python 3.11+
    from importlib.resources.abc import Traversable  # type: ignore
except ImportError:
    # Python 3.10 and earlier
    from importlib.abc import Traversable  # type: ignore
from lxml import etree
from importlib.resources import files


from verbecc.core.defs.types.data.verb import Verb
from verbecc.core.defs.types.data.verbs import Verbs
from verbecc.core.defs.types.exceptions import VerbsParserError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.parsers.verb_parser import VerbParser


class VerbsParser:
    def __init__(self, lang: LangCodeISO639_1 = LangCodeISO639_1.fr) -> None:
        self.lang = lang

    def parse(self) -> Verbs:
        ret: list[Verb] = []
        parser = etree.XMLParser(encoding="utf-8", remove_blank_text=True, remove_comments=True)  # type: ignore
        source: Traversable = files("verbecc.data.xml.verbs").joinpath(
            "verbs-{}.xml".format(self.lang)
        )
        with BytesIO(source.read_bytes()) as fp:  # type: ignore
            tree = etree.parse(fp, parser)  # type: ignore
            root = tree.getroot()
            root_tag = "verbs-{}".format(self.lang)
            if root.tag != root_tag:
                raise VerbsParserError("Root XML Tag {} Not Found".format(root_tag))
            for child in root:
                if child.tag == "v":
                    ret.append(VerbParser().parse(child))  # type: ignore

            ret = sorted(ret, key=lambda v: v.infinitive)
            return Verbs(self.lang, ret)
