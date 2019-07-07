# -*- coding: utf-8 -*-

from __future__ import print_function

from bisect import bisect_left

from lxml import etree

from pkg_resources import resource_filename

from . import string_utils
from . import verb
from . import exceptions

class VerbsParser:
    def __init__(self, lang='fr'):
        self.verbs = []
        parser = etree.XMLParser(encoding='utf-8')
        tree = etree.parse(resource_filename(
                           "verbecc",
                           "data/verbs-{}.xml".format(lang)),
                           parser)
        root = tree.getroot()
        root_tag = 'verbs-{}'.format(lang)
        if root.tag != root_tag:
            raise exceptions.VerbsParserError(
                "Root XML Tag {} Not Found".format(root_tag))
        for child in root:
            if child.tag == 'v':
                self.verbs.append(verb.Verb(child))

        self.verbs = sorted(self.verbs, key=lambda x: x.infinitive)
        self._infinitives = [verb.infinitive for verb in self.verbs]
        self._verbs_no_accents = sorted(self.verbs, key=lambda x: x.infinitive_no_accents)
        self._infinitives_no_accents = [verb.infinitive_no_accents for verb in self.verbs]

    def find_verb_by_infinitive(self, infinitive):
        """First try to find with accents, e.g. if infinitive is 'abañar',
        search for 'abañar' and not 'abanar'. 
        If not found then try searching with accents stripped."""
        i = bisect_left(self._infinitives, infinitive)
        if i != len(self._infinitives) and self._infinitives[i] == infinitive:
            return self.verbs[i]
        infinitive_no_accents = string_utils.strip_accents(infinitive.lower())
        i = bisect_left(self._infinitives_no_accents, infinitive_no_accents)
        if (i != len(self._infinitives_no_accents) 
        and self._infinitives_no_accents[i] == infinitive_no_accents):
            return self._verbs_no_accents[i]
        raise exceptions.VerbNotFoundError

    def get_verbs_that_start_with(self, pre, max_results=10):
        ret = []
        pre_no_accents = string_utils.strip_accents(pre.lower())
        for verb in self.verbs:
            if verb.infinitive_no_accents.startswith(pre_no_accents):
                ret.append(verb.infinitive)
                if len(ret) >= max_results:
                    break
        return ret
