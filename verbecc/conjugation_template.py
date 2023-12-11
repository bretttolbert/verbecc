# -*- coding: utf-8 -*-

from lxml import etree
from typing import Dict

from verbecc.mood import Mood
from verbecc.exceptions import ConjugationTemplateError

class ConjugationTemplate:
    def __init__(self, template_elem: etree._Element):
        if template_elem.tag != 'template':
            raise ConjugationTemplateError(
                "Unexpected element")
        try:
            self.name = str(template_elem.get('name'))
            self.moods: Dict[str, Mood] = {}
            for mood_elem in template_elem:
                mood = Mood(mood_elem)
                self.moods[mood_elem.tag.lower()] = mood
        
        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(
                    etree.tostring(template_elem),
                    str(e)))

    def __repr__(self):
        return 'name={} moods={}'.format(self.name, self.moods)
