# -*- coding: utf-8 -*-

from enum import Enum

class Person(Enum):
    FirstPersonSingular = 0
    SecondPersonSingular = 1
    ThirdPersonSingular = 2
    FirstPersonPlural = 3
    SecondPersonPlural = 4
    ThirdPersonPlural = 5

class ParticipleInflection(Enum):
    MasculineSingular = 0
    MasculinePlural = 1
    FeminineSingular = 2
    FemininePlural = 3

IMPERATIVE_PRESENT_PERSONS = (
    Person.SecondPersonSingular,
    Person.FirstPersonPlural,
    Person.SecondPersonPlural
)

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
    if person == Person.FirstPersonSingular:
        return '-je'
    elif person == Person.SecondPersonSingular:
        return '-toi'
    elif person == Person.ThirdPersonSingular:
        return '-il'
    elif person == Person.FirstPersonPlural:
        return '-nous'
    elif person == Person.SecondPersonPlural:
        return '-vous'
    elif person == Person.ThirdPersonPlural:
        return '-ils'

def get_default_pronoun(person, is_reflexive=False):
    ret = None
    if person == Person.FirstPersonSingular:
        ret = 'je'
        if is_reflexive:
            ret += ' me'
    elif person == Person.SecondPersonSingular:
        ret = 'tu'
        if is_reflexive:
            ret += ' te'
    elif person == Person.ThirdPersonSingular:
        ret = 'il'
        if is_reflexive:
            ret += ' se'
    elif person == Person.FirstPersonPlural:
        ret = 'nous'
        if is_reflexive:
            ret += ' nous'
    elif person == Person.SecondPersonPlural:
        ret = 'vous'
        if is_reflexive:
            ret += ' vous'
    elif person == Person.ThirdPersonPlural:
        ret = 'ils'
        if is_reflexive:
            ret += ' se'
    return ret

def get_default_pronouns():
    return list(map(get_default_pronoun, Person))
        
def get_person_by_pronoun(pronoun):
    pronoun = pronoun.lower()
    if pronoun.startswith('j'):
        return Person.FirstPersonSingular
    elif pronoun.startswith('tu'):
        return Person.SecondPersonSingular
    elif pronoun.startswith(('ils', 'elles')):
        return Person.ThirdPersonPlural
    elif pronoun.startswith(('il', 'elle', 'on')):
        return Person.ThirdPersonSingular
    elif pronoun.startswith('nous'):
        return Person.FirstPersonPlural
    elif pronoun.startswith('vous'):
        return Person.SecondPersonPlural

def get_default_participle_inflection_for_person(person):
    if person == Person.FirstPersonSingular:
        return ParticipleInflection.MasculineSingular
    elif person == Person.SecondPersonSingular:
        return ParticipleInflection.MasculineSingular
    elif person == Person.ThirdPersonSingular:
        return ParticipleInflection.MasculineSingular
    elif person == Person.FirstPersonPlural:
        return ParticipleInflection.MasculinePlural
    elif person == Person.SecondPersonPlural:
        return ParticipleInflection.MasculinePlural
    elif person == Person.ThirdPersonPlural:
        return ParticipleInflection.MasculinePlural
    else:
        raise Exception("Invalid Person")
