from lxml import etree

from verbecc.src.parsers.person_ending import PersonEnding
from verbecc.src.parsers.tense_template import TenseTemplate


def test_tense_and_person():
    tense_elem = etree.fromstring(
        """<present>
        <p><i>ie</i><i>ye</i></p>
        <p><i>ies</i><i>yes</i></p>
        <p><i>ie</i><i>ye</i></p>
        <p><i>yons</i></p>
        <p><i>yez</i></p>
        <p><i>ient</i><i>yent</i></p>
        </present>""",
        None,
    )
    tense_name = "present"
    tense = TenseTemplate(tense_elem)
    assert tense.name == tense_name
    assert tense.person_endings[0].get_ending() == "ie"
    assert tense.person_endings[0].get_alternate_ending_if_available() == "ye"
    assert tense.person_endings[0].get_person() == "1s"
    assert tense.person_endings[3].get_ending() == "yons"
    assert tense.person_endings[3].get_alternate_ending_if_available() == "yons"
    assert tense.person_endings[3].get_person() == "1p"
