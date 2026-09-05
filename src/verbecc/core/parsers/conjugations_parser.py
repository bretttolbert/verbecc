from __future__ import print_function


# try:
from lxml import etree

# except ImportError:
#     import xml.etree.ElementTree as etree
from importlib_resources import as_file, files

# import gzip

# import tempfile
from typing import cast, Optional

from verbecc.core.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.core.defs.types.data.conjugations import Conjugations
from verbecc.core.defs.types.exceptions import ConjugationsParserError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.parsers.conjugation_template_parser import ConjugationTemplateParser
from verbecc.core.parsers.parser import Parser


class ConjugationsParser(Parser):
    def __init__(self, lang: LangCodeISO639_1 = LangCodeISO639_1.fr) -> None:
        self.lang = lang

    def parse(self, elem: Optional[etree._Element] = None) -> Conjugations:
        if elem is not None:
            # this is the the only Parser that doesn't use the elem argument,
            # of the Parser.parser() interface, so this method must implement
            # it even though it isn't used.
            raise ValueError("elem must be None")
        templates: list[ConjugationTemplate] = []
        parser = etree.XMLParser(
            dtd_validation=True, encoding="utf-8", remove_blank_text=True, remove_comments=True  # type: ignore
        )
        source = files("verbecc.data.xml.conjugations").joinpath(
            f"conjugations-{self.lang}.xml"
        )
        with as_file(source) as fp:
            """
            with gzip.open(fp, "rt") as zf:
                with tempfile.NamedTemporaryFile(
                    prefix=f"/tmp/conjugations-{lang}.xml.out.",
                    suffix=".xml",
                    mode="wt+",
                    encoding="utf-8",
                    delete=True,
                ) as tf:
                    next(zf)  # Skips the first line (gzip header plus xml header)
                    # Regenerate xml header
                    tf.write('<?xml version="1.0" encoding="utf-8"?>' + os.linesep)
                    for line in zf:
                        # there are some null bytes at the end that must be stripped
                        for byte in line:
                            if not byte.endswith("\x00"):
                                tf.write(byte)
                    tf.flush()
                    tree = etree.parse(
                        tf.name,
                        parser,  # type: ignore
                    )
            """
            tree = etree.parse(fp, parser)  # type: ignore
            root = tree.getroot()
            root_tag = "conjugation-{}".format(self.lang)
            if root.tag != root_tag:
                raise ConjugationsParserError(
                    "Root XML Tag {} Not Found".format(root_tag)
                )
            for child in root:
                if child.tag == "template":
                    templates.append(
                        ConjugationTemplateParser(lang=self.lang).parse(
                            cast(etree._Element, child)
                        )
                    )
        return Conjugations(self.lang, sorted(templates, key=lambda x: x.name))
