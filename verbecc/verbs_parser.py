# -*- coding: utf-8 -*-

from __future__ import print_function
from bisect import bisect_left
from lxml import etree
from pkg_resources import resource_filename
from typing import List

from verbecc import config
from verbecc import exceptions
from verbecc import mlconjug
from verbecc import string_utils
from verbecc import verb


class VerbsParser:
    def __init__(self, lang: str = "fr"):
        self.verbs: List[verb.Verb] = []
        parser = etree.XMLParser(encoding="utf-8")
        tree = etree.parse(
            resource_filename("verbecc", "data/verbs-{}.xml".format(lang)), parser
        )
        root = tree.getroot()
        root_tag = "verbs-{}".format(lang)
        if root.tag != root_tag:
            raise exceptions.VerbsParserError(
                "Root XML Tag {} Not Found".format(root_tag)
            )
        for child in root:
            if child.tag == "v":
                self.verbs.append(verb.Verb(child))

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

    def find_verb_by_infinitive(self, infinitive: str) -> verb.Verb:
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
            ret = verb.Verb(etree.fromstring(verb_xml))
            ret.predicted = True
            ret.pred_score = pred_score
            return ret
        else:
            raise exceptions.VerbNotFoundError

    def get_verbs_that_start_with(self, pre: str, max_results: int = 10) -> List[str]:
        ret: List[str] = []
        pre_no_accents = string_utils.strip_accents(pre.lower())
        for verb in self.verbs:
            if verb.infinitive_no_accents.startswith(pre_no_accents):
                ret.append(verb.infinitive)
                if len(ret) >= max_results:
                    break
        return ret
