# -*- coding: utf-8 -*-

from lxml import etree

from .mood import Mood


class ConjugationTemplateError(Exception):
    pass


class ConjugationTemplate:
    def __init__(self, template_elem):
        if template_elem.tag != 'template':
            raise ConjugationTemplateError("Unexpected element")
        try:
            self.name = u'' + template_elem.get('name')
            self.moods = {}
            for mood_elem in list(template_elem):
                mood = Mood(mood_elem)
                self.moods[mood_elem.tag] = mood
                    
        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(
                    etree.tostring(template_elem),
                    str(e)))
