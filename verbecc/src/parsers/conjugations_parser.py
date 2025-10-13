from __future__ import print_function

from bisect import bisect_left

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
from importlib_resources import as_file, files

# import gzip
import os

# import tempfile
from typing import List

from verbecc.src.parsers.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.exceptions import (
    ConjugationsParserError,
    TemplateNotFoundError,
)


class ConjugationsParser:
    def __init__(self, lang: str = "fr"):
        self.templates: List[ConjugationTemplate] = []
        parser = etree.XMLParser(
            dtd_validation=True, encoding="utf-8", remove_blank_text=True, remove_comments=True  # type: ignore
        )
        source = files("verbecc.data.xml.conjugations").joinpath(
            f"conjugations-{lang}.xml"
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
            root_tag = "conjugation-{}".format(lang)
            if root.tag != root_tag:
                raise ConjugationsParserError(
                    "Root XML Tag {} Not Found".format(root_tag)
                )
            for child in root:
                if child.tag == "template":
                    self.templates.append(ConjugationTemplate(child))  # type: ignore
            self.templates = sorted(self.templates, key=lambda x: x.name)
            self._keys = [template.name for template in self.templates]

    def find_template(self, name: str) -> ConjugationTemplate:
        """Assumes templates are already sorted by name"""
        i = bisect_left(self._keys, name)
        if i != len(self._keys) and self._keys[i] == name:
            return self.templates[i]
        raise TemplateNotFoundError


if __name__ == "__main__":
    conj = ConjugationsParser()
