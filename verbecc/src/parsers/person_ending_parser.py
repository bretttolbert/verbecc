from lxml import etree
from typing import List

from verbecc.src.parsers.parser import Parser
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.person import Person


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

    def parse(self, elem: etree._Element, person: Person) -> PersonEnding:
        """
        elem: a single <p> element
        Example:
            <p><i>ez</i></p>
            <p><i>eoir</i><i>oir</i></p>
            <p></p>
        """
        endings: List[str] = []
        for i_elem in elem.findall("i", None):
            ending = str("")
            if i_elem.text is not None:
                ending += str(i_elem.text)
            endings.append(ending)
        return PersonEnding(person, endings)
