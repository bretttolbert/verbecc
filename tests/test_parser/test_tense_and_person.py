from lxml import etree

from verbecc.src.parsers.tense_template import TenseTemplate
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.tense import Tense


def test_tense_and_person():
    mood = "indicatif"
    tense_elem_str: str = """<présent>
        <p><i>ie</i><i>ye</i></p>
        <p><i>ies</i><i>yes</i></p>
        <p><i>ie</i><i>ye</i></p>
        <p><i>yons</i></p>
        <p><i>yez</i></p>
        <p><i>ient</i><i>yent</i></p>
        </présent>"""
    tense_elem: etree._Element = etree.fromstring(tense_elem_str)
    tense = Tense.fr.Présent
    tense_template = TenseTemplate(Lang.fr, mood, tense_elem)
    assert tense_template.mood == mood
    assert tense_template.name == str(tense.value)
    assert tense_template.person_endings[0].get_ending() == "ie"
    assert tense_template.person_endings[0].get_alternate_ending_if_available() == "ye"
    assert tense_template.person_endings[0].get_person() == "1s"
    assert tense_template.person_endings[3].get_ending() == "yons"
    assert (
        tense_template.person_endings[3].get_alternate_ending_if_available() == "yons"
    )
    assert tense_template.person_endings[3].get_person() == "1p"
