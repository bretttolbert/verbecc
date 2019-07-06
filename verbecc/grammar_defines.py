# -*- coding: utf-8 -*-

from enum import Enum

PERSONS = ('1s', '2s', '3s', '1p', '2p', '3p')

class ParticipleInflection(Enum):
    MasculineSingular = 0
    MasculinePlural = 1
    FeminineSingular = 2
    FemininePlural = 3

IMPERATIVE_PRESENT_PERSONS = ('2s', '1p', '2p')

TENSES_CONJUGATED_WITHOUT_PRONOUNS = ['infinitif-présent', 'participe-présent', 
                                      'imperatif-présent', 'participe-passé']
VERBS_CONJUGATED_WITH_ETRE = [
"aller",
"arriver",
"descendre",
"redescendre",
"entrer",
"rentrer",
"monter",
"remonter",
"mourir",
"naître",
"renaître",
"partir",
"repartir",
"passer",
"rester",
"retourner",
"sortir",
"ressortir",
"tomber",
"retomber",
"venir",
"devenir",
"parvenir",
"revenir"]

VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS = [
"être",
"aller",
"avoir"]

def get_pronoun_suffix(person):
    if person == '1s':
        return '-je'
    elif person == '2s':
        return '-toi'
    elif person == '3s':
        return '-il'
    elif person == '1p':
        return '-nous'
    elif person == '2p':
        return '-vous'
    elif person == '3p':
        return '-ils'

def get_default_pronoun(person, is_reflexive=False):
    ret = None
    if person == '1s':
        ret = 'je'
        if is_reflexive:
            ret += ' me'
    elif person == '2s':
        ret = 'tu'
        if is_reflexive:
            ret += ' te'
    elif person == '3s':
        ret = 'il'
        if is_reflexive:
            ret += ' se'
    elif person == '1p':
        ret = 'nous'
        if is_reflexive:
            ret += ' nous'
    elif person == '2p':
        ret = 'vous'
        if is_reflexive:
            ret += ' vous'
    elif person == '3p':
        ret = 'ils'
        if is_reflexive:
            ret += ' se'
    return ret

def get_default_pronouns():
    return list(map(get_default_pronoun, PERSONS))

def get_person_by_pronoun(pronoun):
    pronoun = pronoun.lower()
    if pronoun.startswith('j'):
        return '1s'
    elif pronoun.startswith('tu'):
        return '2s'
    elif pronoun.startswith(('ils', 'elles')):
        return '3p'
    elif pronoun.startswith(('il', 'elle', 'on')):
        return '3s'
    elif pronoun.startswith('nous'):
        return '1p'
    elif pronoun.startswith('vous'):
        return '2p'

def get_default_participle_inflection_for_person(person):
    if person[1] == 's':
        return ParticipleInflection.MasculineSingular
    else:
        return ParticipleInflection.MasculinePlural
