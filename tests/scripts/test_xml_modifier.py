from pathlib import Path

import pytest

from scripts import xml_modifier

"""
The "tests" in this module are for development purposes only
and will normally be marked skip but may be unmarked skip 
and ran with dry_run=True (test) or dry_run=False (do)
"""


@pytest.mark.skip("devel")
def test_or_do_spanish_conjugation_xml_mods():
    """
    This is just a unit-test.
    (unless I change dry_run to False, that is)
    """
    INPUT_PATH = Path("verbecc/data/xml/conjugations/conjugations-es.xml")
    OUTPUT_PATH = Path("verbecc/data/xml/conjugations/conjugations-es.mod.xml") 
    xml_modifier.do_spanish_mods(INPUT_PATH, OUTPUT_PATH, dry_run=True)


@pytest.mark.skip("devel")
def test_or_do_portuguese_conjugation_xml_mods():
    """
    This is just a unit-test.
    (unless I change dry_run to False, that is)
    """
    INPUT_PATH = Path("verbecc/data/xml/conjugations/conjugations-pt.xml")
    OUTPUT_PATH = Path("verbecc/data/xml/conjugations/conjugations-pt.mod.xml")
    xml_modifier.do_portuguese_mods(INPUT_PATH, OUTPUT_PATH, dry_run=True)
