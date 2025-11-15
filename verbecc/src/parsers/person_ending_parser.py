import logging

from verbecc.src.defs.constants.config import DEVEL_MODE

logging_level = logging.CRITICAL + 1  # effectively disables logging
if DEVEL_MODE:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("verbecc.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

from lxml import etree
from typing import List, Optional

from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.gender import Gender
from verbecc.src.parsers.parser import Parser
from verbecc.src.defs.types import ConjugationTemplateError


class PersonEndingParser(Parser):
    """
    p_elem
    aka <p>
    Ending for a specific verb template, mood, tense and grammatical person
    May also have an alternate ending for an alternative spelling.
    E.g. Ending for aim:er indicatif présent 2nd Person Plural = ['ez']
    E.g. Ending for pa:yer indicatif présent 1st Person Singular = ['ie', 'ye']
    Explanation: 'ye' is an alternate spelling (je paie, je paye)
    p_elem
        Example p_elems:
            <p><i>ez</i></p>
            <p><i>eoir</i><i>oir</i></p>
            <p></p>

    person
    A grammar_defines.PERSONS value indicating which person
    this PersonEnding is for, e.g. for aim:er, "ez" is '2p' (second person plural)
    """

    def __init__(self) -> None:
        pass

    def parse(
        self,
        elem: Optional[etree._Element] = None,
        person: Optional[Person] = None,
        number: Optional[Number] = None,
        gender: Optional[Gender] = None,
    ) -> PersonEnding:
        """
        elem: a single <p> element
            Example:
            <p><i>ez</i></p>
            <p><i>eoir</i><i>oir</i></p>
            <p></p>
        person: The grammatical person of this conjugation ending.
            person will be None if this is a participle tense.
        number: The grammatical number of this conjugation ending.
        gender: The gender of this person ending.
            gender will be None unless this is a participle tense.

        Participle tense endings only have gender and number.
        All other tense endings only have person and number.
        """
        if elem is None or number is None:
            raise ValueError("elem and number must not be None")
        if person is None and gender is None:
            raise ValueError("neither person nor gender were provided")
        elif person is not None and gender is not None:
            raise ValueError("person and gender are mutually-exclusive")
        endings: List[str] = []
        i_elems = elem.findall("i", None)
        if len(i_elems) == 0:
            logger.warning("Empty <p> element in conjugation template")
        for i_elem in i_elems:
            ending = str("")
            if i_elem.text is not None:
                ending += str(i_elem.text)
            endings.append(ending)
        return PersonEnding(person, number, gender, endings)
