# -*- coding: utf-8 -*-

PERSONS = ('1s', '2s', '3s', '1p', '2p', '3p')

IMPERATIVE_PRESENT_PERSONS = ('2s', '1p', '2p')

PARTICIPLE_INFLECTIONS = ('ms', 'mp', 'fs', 'fp')

def get_default_participle_inflection_for_person(person):
    if person[1] == 's':
        return 'ms'
    else:
        return 'mp'
