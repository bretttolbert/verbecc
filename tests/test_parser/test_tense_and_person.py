from lxml import etree

from verbecc.core.parsers.tense_template_parser import TenseTemplateParser
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.defs.types.mood import Moods
from verbecc.core.defs.types.tense import Tenses
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.number import Number


def test_tense_and_person():
    mood = Moods.fr.Indicatif
    tense = Tenses.fr.Présent
    tense_elem_str: str = """<présent>
        <p><i>ie</i><i>ye</i></p>
        <p><i>ies</i><i>yes</i></p>
        <p><i>ie</i><i>ye</i></p>
        <p><i>yons</i></p>
        <p><i>yez</i></p>
        <p><i>ient</i><i>yent</i></p>
        </présent>"""
    tense_elem: etree._Element = etree.fromstring(tense_elem_str)
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    assert tense_template.mood == mood
    assert tense_template.tense == tense
    assert tense_template.person_endings[0].get_ending() == "ie"
    assert tense_template.person_endings[0].get_alternate_ending_if_available() == "ye"
    assert tense_template.person_endings[0].get_person() == Person.First
    assert tense_template.person_endings[0].get_number() == Number.Singular
    assert tense_template.person_endings[3].get_ending() == "yons"
    assert (
        tense_template.person_endings[3].get_alternate_ending_if_available() == "yons"
    )
    assert tense_template.person_endings[3].get_person() == Person.First
    assert tense_template.person_endings[3].get_number() == Number.Plural
