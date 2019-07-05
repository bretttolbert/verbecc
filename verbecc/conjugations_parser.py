# -*- coding: utf-8 -*-

from __future__ import print_function

from bisect import bisect_left

from lxml import etree

from pkg_resources import resource_filename

from .conjugation_template import ConjugationTemplate


class ConjugationsParserError(Exception):
    pass

class TemplateNotFoundError(Exception):
    pass

class ConjugationsParser:
    def __init__(self):
        self.templates = []
        parser = etree.XMLParser(dtd_validation=True, encoding='utf-8')
        tree = etree.parse(
            resource_filename("verbecc",
                              "data/conjugations_fr.xml"),
            parser)
        root = tree.getroot()
        if root.tag != 'conjugation-fr':
            raise ConjugationsParserError("Root XML Tag <conjugation-fr> Not Found")
        for child in root:
            if child.tag == 'template':
                self.templates.append(ConjugationTemplate(child))
        self.templates = sorted(self.templates, key=lambda x: x.name)
        self._keys = [template.name for template in self.templates]

    def find_template(self, name):
        """Assumes templates are already sorted by name"""
        i = bisect_left(self._keys, name)
        if i != len(self._keys) and self._keys[i] == name:
            return self.templates[i]
        raise TemplateNotFoundError


if __name__ == "__main__":
    conj = ConjugationsParser()
