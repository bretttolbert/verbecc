# -*- coding: utf-8 -*-

from lxml import etree

from .mood import (MOOD_TENSES, Mood)


class ConjugationTemplateError(Exception):
    pass


class ConjugationTemplate:
    def __init__(self, template_elem):
        if template_elem.tag != 'template':
            raise ConjugationTemplateError("not a 'template' elem")
        try:
            self.name = u'' + template_elem.get('name')
            self.impersonal = False
            self.moods = {}
            for mood_name, mood_tenses in MOOD_TENSES.items():
                mood = Mood(mood_name, template_elem.find(mood_name))
                self.moods[mood_name] = mood
                if (mood_name == 'indicative' 
                    and len(mood.tenses['present'].person_endings) < 6):
                    self.impersonal = True
                    
        except AttributeError as e:
            raise ConjugationTemplateError(
                "Error parsing {}: {}".format(
                    etree.tostring(template_elem),
                    str(e)))
