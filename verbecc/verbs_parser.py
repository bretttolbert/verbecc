# -*- coding: utf-8 -*-

from __future__ import print_function

from bisect import bisect_left

from lxml import etree

from pkg_resources import resource_filename

from .string_utils import strip_accents
from .verb import (Verb, VerbsParserError)


class VerbNotFoundError(Exception):
    pass


class VerbsParser:
    def __init__(self, lang='fr'):
        self.verbs = []
        parser = etree.XMLParser(encoding='utf-8')
        tree = etree.parse(resource_filename(
                           "verbecc",
                           "data/verbs_{}.xml".format(lang)),
                           parser)
        root = tree.getroot()
        root_tag = 'verbs-{}'.format(lang)
        if root.tag != root_tag:
            raise VerbsParserError(
                "Root XML Tag {} Not Found".format(root_tag))
        for child in root:
            if child.tag == 'v':
                self.verbs.append(Verb(child))
        self.verbs = sorted(self.verbs, key=lambda x: x.infinitive_no_accents)
        self._keys = [verb.infinitive_no_accents for verb in self.verbs]

    def find_verb_by_infinitive(self, infinitive):
        """Assumes verbs are already sorted by infinitive"""
        infinitive_no_accents = strip_accents(infinitive.lower())
        i = bisect_left(self._keys, infinitive_no_accents)
        if i != len(self._keys) and self._keys[i] == infinitive_no_accents:
            return self.verbs[i]
        raise VerbNotFoundError

    def get_verbs_that_start_with(self, pre, max_results=10):
        ret = []
        pre_no_accents = strip_accents(pre.lower())
        for verb in self.verbs:
            if verb.infinitive_no_accents.startswith(pre_no_accents):
                ret.append(verb.infinitive)
                if len(ret) >= max_results:
                    break
        return ret
