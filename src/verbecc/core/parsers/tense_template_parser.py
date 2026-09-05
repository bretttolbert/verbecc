from lxml import etree
from typing import Optional

from verbecc.core.utils.logging_utils import LoggingUtils
from verbecc.core.defs.constants import grammar_defines
from verbecc.core.defs.constants.localization import xmood
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.data.tense_template import TenseTemplate
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.tense import TenseFactory
from verbecc.core.parsers.parser import Parser
from verbecc.core.parsers.person_ending_parser import PersonEndingParser


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
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)
        self.lang = lang
        self.mood = mood

    def parse(self, elem: Optional[etree._Element] = None) -> TenseTemplate:
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

        French infinitive-present has only 1 <p> element
        E.g. <p><i>avoir</i></p>

        """
        if elem is None:
            raise ValueError("elem must not be None")
        self.tense = TenseFactory.from_string(self.lang, elem.tag)
        person_endings: list[PersonEnding] = []
        person_num = 0
        participle_inflections = grammar_defines.PARTICIPLE_INFLECTIONS[self.lang]
        imperative_persons = grammar_defines.IMPERATIVE_PERSONS[self.lang]
        p_elems = elem.findall("p", namespaces=None)
        for p_elem in p_elems:
            gender = None
            person = None
            number = None

            if len(p_elems) == 1:
                # only 1 <p> element
                # so it's likely a tense with a single conjugation e.g.
                # French present participle or infinitive present
                # e.g., for the French verb "avoir" the present participle is simply
                # ["ayant"], a single conjugation with no gender, number or person
                pass  # leave gender, number, person as None
            elif self.mood == xmood(self.lang, Moods.en.Participle):
                if len(p_elems) == len(participle_inflections):
                    gender, number = participle_inflections[person_num].value
                else:
                    self._logger.warning(
                        f"Unexpected number of participle inflections {len(p_elems)} "
                        + f"on tense template for language {self.lang}: "
                        + f"{[etree.tostring(p) for p in p_elems]}"
                    )
            elif self.mood == xmood(self.lang, Moods.en.Imperative):
                if len(p_elems) == len(imperative_persons):
                    person, number = imperative_persons[person_num]
                else:
                    self._logger.warning(
                        f"Unexpected number of imperative person inflections {len(p_elems)} "
                        + f"on tense template for language {self.lang}: "
                        + f"{[etree.tostring(p) for p in p_elems]}"
                    )
            else:
                # normal case: all persons
                person, number = grammar_defines.PERSONS[person_num]

            pe = PersonEndingParser().parse(p_elem, person, number, gender)
            person_num += 1
            if len(pe.endings) > 0:
                person_endings.append(pe)

        return TenseTemplate(self.lang, self.mood, self.tense, person_endings)
