from lxml import etree
from typing import List

from verbecc.src.parsers.parser import Parser
from verbecc.src.parsers.person_ending_parser import PersonEndingParser
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.constants import grammar_defines
from verbecc.src.defs.types.tense import TenseFactory
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.constants.localization import xmood


class TenseTemplateParser(Parser):
    """
    Contains PersonEndings for a specific verb template, mood and tense
    Note: The template name and mood is only known by the Mood object
          which owns this Tense.
    Class relationships:
        ConjugationTemplate has many Mood
            Mood has many Tense
                Tense has many PersonEnding
    E.g. aim:er indicatif présent
    name
        the name of the tense, e.g. présent
    tense_elem
        A tense_elem contains one or more <p> (PersonEnding) elems
        Example tense_elem children:
            <p><i>e</i></p>
            <p><i>es</i></p>
            <p><i>e</i></p>
            <p><i>ons</i></p>
            <p><i>ez</i></p>
            <p><i>ent</i></p>
    """

    def __init__(self, lang: Lang, mood: Mood) -> None:
        self.lang = lang
        self.mood = mood

    def parse(self, elem: etree._Element) -> TenseTemplate:
        self.tense = TenseFactory.from_string(self.lang, elem.tag)
        """
        Normally each <p> elem defines six grammatical persons:
            (see grammar_defines.PERSONS)
            [0]= '1s' (je)
            [1]= '2s' (tu)
            [2]= '3s' (il, elle, on)
            [3]= '1p' (nous)
            [4]= '2p' (vous)
            [5]= '3p' (ils, elles)

        The following tenses have all 6 Persons:
          présent, impafait, futur, passé-simple
        These do not:
          infinitive-present has only 1
          imperative-present has 3
            [0]= '2s' e.g. lève-toi
            [2]= '1p' e.g. levons-nous
            [3]= '2p' e.g. levez-vous
          participe-présent has 1
          participe-passé has 4
              [0]= ms
              [1]= mp
              [2]= fs
              [3]= fp

        For some verbs, e.g. être, the past-participle
        is the same for all 4 inflections, so the xml omits them:
            <p><i>été</i></p>
            <p></p>
            <p></p>
            <p></p>
        Workaround: We do not add a PersonEnding unless it contains an <i>

        Also some verbs are impersonal, e.g. pleuvoir, so they don't have
        ending for all pronouns. Just 3rd person singular and plural

            <p></p>
            <p></p>
            <p><i>eut</i></p> e.g. il pleut
            <p></p>
            <p></p>
            <p><i>euvent</i></p> e.g. ils pleuvent (rare, but valid)

        Spanish imperative tenses have 5, i.e. all except 1st person singular

        """
        person_endings: List[PersonEnding] = []
        person_num = 0
        for p_elem in elem.findall("p", namespaces=None):
            person = grammar_defines.PERSONS[person_num]
            if self.mood == xmood(self.lang, Mood.en.Imperative):
                person = grammar_defines.IMPERATIVE_PERSONS[self.lang][person_num]
            pe = PersonEndingParser().parse(p_elem, person)
            person_num += 1
            if len(pe.endings) > 0:
                person_endings.append(pe)

        return TenseTemplate(self.lang, self.mood, self.tense, person_endings)
