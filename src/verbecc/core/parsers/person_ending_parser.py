from typing import Optional

from verbecc.core.defs.types.data.xml_types import XmlElement
from verbecc.core.utils.logging_utils import LoggingUtils
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.gender import Gender
from verbecc.core.parsers.parser import Parser
from verbecc.core.utils.xml_utils import xml_element_findall, xml_element_get_text


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
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)

    def parse(
        self,
        elem: Optional[XmlElement] = None,
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
        Present-Participle tense has neither person, number, nor gender,
        because there is only a single conjugation form. E.g. "ayant"
        All other tense endings only have person and number.

        Returns a PersonEnding object.
        """
        if elem is None:
            raise ValueError("elem must not be None")
        endings: list[str] = []
        i_elems = xml_element_findall(elem, "i")
        if len(i_elems) == 0:
            self._logger.debug("Empty <p> element in conjugation template")
        for i_elem in i_elems:
            ending = str("")
            i_elem_text = xml_element_get_text(i_elem)
            if i_elem_text is not None:
                ending += i_elem_text
            endings.append(ending)
        return PersonEnding(person, number, gender, endings)
