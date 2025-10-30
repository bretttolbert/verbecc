from __future__ import print_function

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
from importlib_resources import as_file, files

# import gzip
import os

# import tempfile
from typing import List

from verbecc.src.defs.types.data.verb import Verb
from verbecc.src.defs.types.data.verbs import Verbs
from verbecc.src.defs.types.exceptions import VerbsParserError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.parsers.verb_parser import VerbParser


class VerbsParser:
    def __init__(self, lang: LangCodeISO639_1 = LangCodeISO639_1.fr) -> None:
        self.lang = lang

    def parse(self) -> Verbs:
        ret: List[Verb] = []
        parser = etree.XMLParser(encoding="utf-8", remove_blank_text=True, remove_comments=True)  # type: ignore
        source = files("verbecc.data.xml.verbs").joinpath(
            "verbs-{}.xml".format(self.lang)
        )
        with as_file(source) as fp:
            """
            with gzip.open(fp, "rt") as zf:
                with tempfile.NamedTemporaryFile(
                    prefix=f"/tmp/verbs-{lang}.xml.out.",
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
                    tree = etree.parse(tf.name, parser)  # type: ignore
            """
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
