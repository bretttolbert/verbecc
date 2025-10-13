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

from verbecc.src.parsers.verb import Verb
from verbecc.src.defs.types.exceptions import VerbNotFoundError, VerbsParserError
from verbecc.src.defs.constants import config
from verbecc.src.mlconjug import mlconjug
from verbecc.src.utils import string_utils


class VerbsParser:
    def __init__(self, lang: str = "fr"):
        self.verbs: List[Verb] = []
        parser = etree.XMLParser(encoding="utf-8", remove_blank_text=True, remove_comments=True)  # type: ignore
        source = files("verbecc.data.xml.verbs").joinpath("verbs-{}.xml".format(lang))
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
            root_tag = "verbs-{}".format(lang)
            if root.tag != root_tag:
                raise VerbsParserError("Root XML Tag {} Not Found".format(root_tag))
            for child in root:
                if child.tag == "v":
                    self.verbs.append(Verb(child))  # type: ignore

            self.verbs = sorted(self.verbs, key=lambda v: v.infinitive)
            self._infinitives = [v.infinitive for v in self.verbs]
            self._verbs_no_accents = sorted(
                self.verbs, key=lambda v: v.infinitive_no_accents
            )
            self._infinitives_no_accents = [
                v.infinitive_no_accents for v in self._verbs_no_accents
            ]
            if config.ml:
                self.template_predictor = mlconjug.TemplatePredictor(
                    [(v.infinitive, v.template) for v in self.verbs], lang
                )

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        """First try to find with accents, e.g. if infinitive is 'Abañar',
        search for 'abañar' and not 'abanar'.
        If not found then try searching with accents stripped.
        If all else fails, use machine-learning magic to predict
        which conjugation template should be used.
        """
        query = infinitive.lower()
        i = bisect_left(self._infinitives, query)
        if i != len(self._infinitives) and self._infinitives[i] == query:
            return self.verbs[i]
        query = string_utils.strip_accents(infinitive.lower())
        i = bisect_left(self._infinitives_no_accents, query)
        if (
            i != len(self._infinitives_no_accents)
            and self._infinitives_no_accents[i] == query
        ):
            return self._verbs_no_accents[i]
        if config.ml:
            template, pred_score = self.template_predictor.predict(query)
            verb_xml = "<v><i>{}</i><t>{}</t></v>".format(infinitive.lower(), template)
            ret = Verb(etree.fromstring(verb_xml))  # type: ignore
            ret.predicted = True
            ret.pred_score = pred_score
            return ret
        else:
            raise VerbNotFoundError

    def get_verbs_that_start_with(self, pre: str, max_results: int = 10) -> List[str]:
        ret: List[str] = []
        pre_no_accents = string_utils.strip_accents(pre.lower())
        for verb in self.verbs:
            if verb.infinitive_no_accents.startswith(pre_no_accents):
                ret.append(verb.infinitive)
                if len(ret) >= max_results:
                    break
        return ret
