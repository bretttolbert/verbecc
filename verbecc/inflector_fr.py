import copy

from . import inflector
from . import parse_conjugations
from . import parse_verbs
from . import grammar_defines
from . import string_utils
from . import exceptions

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

def get_pronoun_suffix(person, gender='m'):
    if person == '1s':
        return '-je'
    elif person == '2s':
        return '-toi'
    elif person == '3s':
        if gender == 'm':
            return '-il'
        else:
            return '-elle'
    elif person == '1p':
        return '-nous'
    elif person == '2p':
        return '-vous'
    elif person == '3p':
        if gender == 'm':
            return '-ils'
        else:
            return '-elles'

def get_default_pronoun(person, gender='m', is_reflexive=False):
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
        if gender == 'f':
            ret = 'elle'
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
        if gender == 'f':
            ret = 'elles'
        if is_reflexive:
            ret += ' se'
    return ret

class InflectorFr(inflector.Inflector):
    def __init__(self):
        self.lang = 'fr'
        self._verb_parser = parse_verbs.VerbsParser(self.lang)
        self._conj_parser = parse_conjugations.ConjugationsParser(self.lang)

    def _is_impersonal_verb(self, infinitive):
        ret = False
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        if len(template.moods['indicatif'].tenses['présent'].person_endings) < 6:
            ret = True
        return ret

    def _verb_can_be_reflexive(self, infinitive):
        return (not self._is_impersonal_verb(infinitive) 
            and infinitive not in 
            VERBS_THAT_CANNOT_BE_REFLEXIVE_OTHER_THAN_IMPERSONAL_VERBS) 

    def _conjugate_simple_mood_tense(self, verb_stem, mood_name, 
                                     tense_template, is_reflexive=False):
        ret = []
        if tense_template.name in TENSES_CONJUGATED_WITHOUT_PRONOUNS:
            for person_ending in tense_template.person_endings:
                conj = ''
                if is_reflexive and tense_template.name == 'participe-passé':
                    conj += 'étant '
                conj += verb_stem + person_ending.get_ending()
                if is_reflexive:
                    if mood_name != 'imperatif':
                        conj = string_utils.prepend_with_se(conj)
                    else:
                        conj += get_pronoun_suffix(person_ending.get_person())
                ret.append(conj)
        else:
            for person_ending in tense_template.person_endings:
                pronoun = get_default_pronoun(
                    person_ending.get_person(), is_reflexive)
                ending = person_ending.get_ending()
                conjugation = self._conjugate_simple_mood_tense_pronoun(
                    verb_stem, ending, pronoun)
                if mood_name == 'subjonctif':
                    conjugation = string_utils.prepend_with_que(conjugation)
                ret.append(conjugation)
        return ret

    def _conjugate_simple_mood_tense_pronoun(self, verb_stem, ending, pronoun):
        ret = u''
        conjugated_verb = verb_stem + ending
        if pronoun[-1] == "e" and string_utils.starts_with_vowel(conjugated_verb):
            ret += pronoun[:-1] + "'"
        else:
            ret += pronoun + " "
        ret += conjugated_verb
        return ret

    def _get_compound_conjugations_map(self):
        return {
            'indicatif': {
                'passé-composé': 'présent',
                'plus-que-parfait': 'imparfait',
                'futur-antérieur': 'futur-simple',
                'passé-antérieur': 'passé-simple'
            },
            'subjonctif': {
                'passé': 'présent',
                'plus-que-parfait': 'imparfait'
            },
            'conditionnel': {
                'passé': 'présent'
            },
            'imperatif': {
                'imperatif-passé': 'imperatif-présent'
            }
        }

    def _conjugate_compound(self, co, mood_name, hv_tense_name):
        """Conjugate a compound tense
        Args:
            co: ConjugationObjects for the verb being conjugated
            mood_name: mood verb is being conjugated in
            hv_tense_name: tense_name for conjugating helping verb
        """
        ret = []
        if (co.is_reflexive and mood_name == 'imperatif' 
            and hv_tense_name == 'imperatif-présent'):
            return ret
        persons = [pe.person for pe in 
            co.template.moods[mood_name].tenses[hv_tense_name].person_endings]
        helping_verb = 'avoir'
        if (co.verb.infinitive in VERBS_CONJUGATED_WITH_ETRE
            or co.is_reflexive):
            helping_verb = 'être'
        hvco = self._get_conj_obs(helping_verb)
        hvtense_template = copy.deepcopy(
            hvco.template.moods[mood_name].tenses[hv_tense_name])
        hvperson_endings = []
        for pe in hvtense_template.person_endings:
            if pe.person in persons:
                hvperson_endings.append(pe)
        hvtense_template.person_endings = hvperson_endings
        hvconj = self._conjugate_simple_mood_tense(
            hvco.verb_stem, 
            'indicatif', 
            hvtense_template,
            co.is_reflexive)
        participle = self._conjugate_simple_mood_tense(
            co.verb_stem, 
            'participe', 
            co.template.moods['participe'].tenses['participe-passé'])
        if helping_verb == 'avoir':
            for hv in hvconj:
                p = participle[0]
                ret.append(hv + ' ' + p)
        else:
            for i, hv in enumerate(hvconj):
                participle_inflection = \
                    grammar_defines.get_default_participle_inflection_for_person(persons[i])
                p = participle[grammar_defines.PARTICIPLE_INFLECTIONS.index(participle_inflection)]
                ret.append(hv + ' ' + p)
        if mood_name == 'subjonctif':
            ret = [string_utils.prepend_with_que(i) for i in ret]
        return ret
