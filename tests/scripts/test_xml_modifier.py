from pathlib import Path

import pytest
from lxml import etree

from scripts import xml_modifier
from verbecc.core.utils.xml_utils import xml_element_to_string

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
    INPUT_PATH = Path("src/verbecc/data/xml/conjugations/conjugations-es.xml")
    OUTPUT_PATH = Path("src/verbecc/data/xml/conjugations/conjugations-es.mod.xml")
    xml_modifier.do_spanish_mods(INPUT_PATH, OUTPUT_PATH, dry_run=True)


@pytest.mark.skip("devel")
def test_or_do_portuguese_conjugation_xml_mods():
    """
    This is just a unit-test.
    (unless I change dry_run to False, that is)
    """
    INPUT_PATH = Path("src/verbecc/data/xml/conjugations/conjugations-pt.xml")
    OUTPUT_PATH = Path("src/verbecc/data/xml/conjugations/conjugations-pt.mod.xml")
    xml_modifier.do_portuguese_mods(INPUT_PATH, OUTPUT_PATH, dry_run=True)


@pytest.mark.parametrize("encoding", ["utf-8", "iso-8859-1", "unicode"])
def test_xml_element_to_string_decodes_serialized_xml(encoding):
    elem = etree.fromstring("<root>café</root>")

    result = xml_element_to_string(
        elem, encoding=encoding, pretty_print=False, xml_declaration=False
    )

    assert result == "<root>café</root>"


def test_write_output_file_produces_parseable_utf8(tmp_path):
    root = etree.fromstring("<root>café</root>")
    output = tmp_path / "output.xml"

    xml_modifier.write_output_file(etree.ElementTree(root), output)

    data = output.read_bytes()
    assert b"caf\xc3\xa9" in data
    assert etree.parse(str(output)).getroot().text == "café"
