"""
This script has been used to modify the mlconjug conjugation XML files

It is called by the test stubs in tests/scripts/test_xml_modifier.py (if unmarked as @skip)

It could be repurposed by anyone who needs to perform batch
modifications on XML files that are too large to edit by manually.

E.g.
- rename, move or delete elements
- remove unwanted tense elements (e.g. compound tenses)
- move tense elements from one mood to another
- remove second <p> element from every tense element

"""

from typing import Optional, cast
from pathlib import Path
from typing import Sequence, Tuple

from verbecc.core.defs.types.data.xml_types import XmlElement, XmlElementTree, XmlParser
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.utils.logging_utils import LoggingUtils
from verbecc.core.utils.xml_utils import xml_element_remove, xml_element_repr, xml_element_to_string, xml_element_deannotate, xml_element_xpath, xml_parse

INPUT_PATH = "../verbecc/data/xml/conjugations/conjugations-es.xml"
OUTPUT_PATH = "../verbecc/data/xml/conjugations/conjugations-es.mod.xml"

logger = LoggingUtils.get_logger(__name__)

def remove_tenses(root: XmlElement, tenses_to_remove: list[Tense]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                for tense_elem in mood_elem:
                    if tense_elem.tag in tenses_to_remove:
                        mood_elem.remove(tense_elem)
                        removed_elem_cnt += 1
    logger.info("removed {} elements".format(removed_elem_cnt))


def remove_mood(root: XmlElement, moods_to_remove: list[Mood]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                if mood_elem.tag in moods_to_remove:
                    template_elem.remove(mood_elem)
                    removed_elem_cnt += 1
    logger.info("removed {} elements".format(removed_elem_cnt))


def find_tense(
    template_elem: XmlElement,
    mood: Mood,
    tense: Tense,
    should_remove_mood: bool = False,
) -> Optional[XmlElement]:
    # find tense to move
    for mood_elem in template_elem:
        if mood_elem.tag == mood:
            for tense_elem in mood_elem:
                if tense_elem.tag == tense:
                    tense_elem_to_move = tense_elem
                    mood_elem.remove(tense_elem)
                    if should_remove_mood:
                        parent = mood_elem.getparent()
                        if parent is not None:
                            parent.remove(mood_elem)
                            logger.info(f"removed mood element {mood_elem.tag}")
                        else:
                            logger.info("parent is None!")
                    return tense_elem_to_move
    return None


def move_tense(
    root: XmlElement,
    tense: Tense,
    old_mood: Mood,
    new_mood: Mood,
    remove_old_mood: bool,
) -> None:
    """
    moves a tense element from one mood to another
    """
    moved_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            tense_elem_to_move = None

            # Now move it
            if tense_elem_to_move is not None:
                for mood_elem in template_elem:
                    if mood_elem.tag == new_mood:
                        mood_elem.append(tense_elem_to_move)
                        moved_elem_cnt += 1
    logger.info("moved {} elements".format(moved_elem_cnt))


def read_input_file(path: Path) -> XmlElementTree:
    parser = XmlParser(dtd_validation=False, encoding="utf-8")
    tree = xml_parse(path, parser)
    return tree


def elem_tobytes(elem: XmlElement) -> bytes:
    return xml_element_to_string(
        elem,
        encoding="utf-8",
        method="xml",
        pretty_print=True,
        xml_declaration=True,
    ).encode("utf-8")


def write_output_file(tree: XmlElementTree, path: Path) -> None:
    root = tree.getroot()
    with open(path, "wb") as f:
        xml_element_deannotate(root)
        xml = elem_tobytes(root)
        f.write(xml)


def do_romanian_mods(input_path: Path, output_path: Path) -> None:
    tree = read_input_file(input_path)
    root = tree.getroot()
    remove_tenses(root, ["perfect"])  # type: ignore
    move_tense(root, "Viitor-II-popular", "Viitor", "Indicativ", True)  # type: ignore
    remove_mood(root, [Moods.en.Conditional])
    write_output_file(tree, output_path)


"""
Italian has infinito gerundio which is in the following format:
    <Infinito>
        <gerundio>
            <p><i>essere</i></p>
            <p><i>stato</i></p>
            <p><i>essendo</i></p>
            <p><i>stato</i></p>
        </gerundio>
    </Infinito>

The French and Romanian templates for infinitif have only one <p> element:

Catalan:
    <infinitif-présent>
        <p><i>avoir</i></p>
    </infinitif-présent>

Romanian:
    <Infinitiv>
        <afirmativ>
            <p><i>fi</i></p>
        </afirmativ>
    </Infinitiv>

Catalan has one <p> element with two conjugations (default and alternate):
    <Infinitiu>
        <infinitiu-present>
            <p><i>ser</i>
            <i>ésser</i></p>
        </infinitiu-present>
    </Infinitiu>


Spanish and Portuguese templates have two <p> elements:

Spanish:
    <Infinitivo>
        <infinitivo>
            <p><i>ser</i></p>
            <p><i>sido</i></p>
        </infinitivo>
    </Infinitivo>

Portuguese:
    <Infinitivo>
        ...
        <infinitivo>
            <p><i>ser</i></p>
            <p><i>sido</i></p>
        </infinitivo>
    </Infinitivo>

Spanish gerundio also has two elements.


"""


def remove_nth_element_of_every_matching_great_grandchild(
    root: XmlElement,
    great_grandparent_elem_tag: str,
    grandparent_elem_tag: str,
    parent_elem_tag: str,
    elem_to_remove_tag: str,
    n: int,
    dry_run: bool = True,
) -> int:
    """
    n = the 1-based index of the element to remove.
    Returns the number of elements removed.
    """
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")

    # Construct XPath path leading directly to parent elements.
    # Note: Using translate() handles case-insensitivity for the grandparent tag.
    xpath_query = (
        f"./{great_grandparent_elem_tag}/"
        f"*[translate(name(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{grandparent_elem_tag.lower()}']/"
        f"{parent_elem_tag}"
    )

    cnt = 0
    # This XPath selects elements, but lxml's type stubs model ``xpath`` as
    # potentially returning scalar XPath results as well.
    parents = cast(list[XmlElement], xml_element_xpath(root, xpath_query))  # type: ignore
    for parent in parents:
        # Filter children matching the target tag
        matching_children = [
            child for child in parent if child.tag == elem_to_remove_tag
        ]

        # Check if the 1-based index exists
        if len(matching_children) >= n:
            target_elem = matching_children[n - 1]
            action_str = "Would have removed" if dry_run else "Removed"

            if not dry_run:
                xml_element_remove(parent, target_elem)

            logger.info(f"{action_str} elem {xml_element_repr(target_elem)}")
            cnt += 1

    qualifier = "would have " if dry_run else ""
    logger.info(
        f"{qualifier}removed {cnt} <{elem_to_remove_tag}> elements "
        f"descendent from parent element {parent_elem_tag}, "
        f"from grandparent element {grandparent_elem_tag}, "
        f"from great-grandparent element {great_grandparent_elem_tag}."
    )
    return cnt


def remove_second_p_element_from_every_matching_template(
    root: XmlElement, mood: Mood, tense: Tense, dry_run: bool = True
) -> int:
    return remove_nth_element_of_every_matching_great_grandchild(
        root,
        great_grandparent_elem_tag="template",
        grandparent_elem_tag=str(mood),
        parent_elem_tag=str(tense),
        elem_to_remove_tag="p",
        n=2,
        dry_run=dry_run,
    )


def do_remove_second_p_elem_mods(
    input_path: Path,
    output_path: Path,
    mood_tenses: Sequence[Tuple[Mood, Tense]],
    dry_run: bool = True,
) -> None:
    tree = read_input_file(input_path)
    root = tree.getroot()
    cnt = 0
    for mood, tense in mood_tenses:
        cnt += remove_second_p_element_from_every_matching_template(
            root, mood, tense, dry_run
        )
    if dry_run:
        logger.info("Total elements that would have been removed: %d", cnt)
    else:
        logger.info("Total elements removed: %d", cnt)
    write_output_file(tree, output_path)


def do_spanish_mods(input_path: Path, output_path: Path, dry_run: bool = True) -> None:
    mood_tenses = [
        (Moods.es.Infinitivo, Tenses.es.Infinitivo),
        (Moods.es.Gerundio, Tenses.es.Gerundio),
    ]
    do_remove_second_p_elem_mods(input_path, output_path, mood_tenses, dry_run)


def do_portuguese_mods(
    input_path: Path, output_path: Path, dry_run: bool = True
) -> None:
    mood_tenses = [
        (Moods.pt.Infinitivo, Tenses.pt.Infinitivo),
        (Moods.pt.Gerúndio, Tenses.pt.Gerúndio),
    ]
    do_remove_second_p_elem_mods(input_path, output_path, mood_tenses, dry_run)
