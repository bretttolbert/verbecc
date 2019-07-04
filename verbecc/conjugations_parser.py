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


"""
Conjugations XML structure:

Moods:
    infinitive (infinitive-present)
    indicative (present, imperfect, future, simple-past)
    conditional (present)
    subjunctive (present, imperfect)
    imperative (imperative-present)
    participle (present-participle, past-participle)

Tenses:
    infinitive-present (p)
    present (p, p, p, p, p, p)
    imperfect (p, p, p, p, p, p)
    future (p, p, p, p, p, p)
    simple-past (p, p, p, p, p, p)
    imperative-present (p, p, p)
    present-participle (p)
    past-participle (p, p, p, p)

Class Diagram:

    ConjugationsParser
        has 1..* Template
            has 1..* Mood
                has 1..* Tense
                    has 1..* Person
"""


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
        self.impersonal_templates = \
            [t.name for t in self.templates if t.impersonal]
        print('Loaded {} conjugation templates'.format(len(self.templates)))

    def find_template(self, name):
        """Assumes templates are already sorted by name"""
        i = bisect_left(self._keys, name)
        if i != len(self._keys) and self._keys[i] == name:
            return self.templates[i]
        raise TemplateNotFoundError


if __name__ == "__main__":
    conj = ConjugationsParser()
