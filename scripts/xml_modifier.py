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

from typing import Optional
from pathlib import Path
from lxml import etree, objectify
import os
from typing import Sequence, Tuple
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.utils.logging_utils import LoggingUtils

INPUT_PATH = "../verbecc/data/xml/conjugations/conjugations-es.xml"
OUTPUT_PATH = "../verbecc/data/xml/conjugations/conjugations-es.mod.xml"

logger = LoggingUtils.get_logger(__name__)


def remove_tenses(root: etree._Element, tenses_to_remove: list[Tense]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                for tense_elem in mood_elem:
                    if tense_elem.tag in tenses_to_remove:
                        mood_elem.remove(tense_elem)
                        removed_elem_cnt += 1
    logger.info("removed {} elements".format(removed_elem_cnt))


def remove_mood(root: etree._Element, moods_to_remove: list[Mood]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                if mood_elem.tag in moods_to_remove:
                    template_elem.remove(mood_elem)
                    removed_elem_cnt += 1
    logger.info("removed {} elements".format(removed_elem_cnt))


def find_tense(
    template_elem: etree._Element,
    mood: Mood,
    tense: Tense,
    should_remove_mood: bool = False,
) -> Optional[etree._Element]:
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
    root: etree._Element,
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


def read_input_file(path: Path) -> etree._ElementTree:
    parser = etree.XMLParser(dtd_validation=False, encoding="utf-8")
    tree = etree.parse(path, parser)
    return tree


def elem_tobytes(elem: etree._Element) -> bytes:
    return etree.tostring(
        elem,
        encoding="utf-8",
        method="xml",
        pretty_print=True,
        xml_declaration=True,
    )


def elem_tostring(elem: etree._Element) -> str:
    return elem_tobytes(elem).decode("utf-8")


def repr_elem(elem: etree._Element) -> str:
    return f"{elem.tag}: {elem} {elem_tostring(elem)}"


def write_output_file(tree: etree._ElementTree, path: Path) -> None:
    root = tree.getroot()
    with open(path, "wb") as f:
        objectify.deannotate(root, cleanup_namespaces=True)
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
    root: etree._Element,
    great_grandparent_elem_tag: str,
    grandparent_elem_tag: str,
    parent_elem_tag: str,
    elem_to_remove_tag: str,
    n: int,
    dry_run: bool = True,
) -> int:
    """
    n = the (1-based) indice of the element to remove

    returns number of elements removed
    """
    if n < 1:
        raise ValueError("n must be nonzero")
    cnt = 0
    for great_grandparent_elem in root:
        # E.g. template
        if great_grandparent_elem.tag == great_grandparent_elem_tag:
            # E.g. mood
            for grandparent_elem in great_grandparent_elem:
                if grandparent_elem.tag.lower() == grandparent_elem_tag:
                    # E.g. tense
                    for parent_elem in grandparent_elem:
                        if parent_elem.tag == parent_elem_tag:
                            elem_n = 1
                            # E.g. <p> elem
                            for elem in parent_elem:
                                if elem.tag == elem_to_remove_tag:
                                    if elem_n == n:
                                        if dry_run is False:
                                            parent_elem.remove(elem)
                                            logger.info(
                                                f"Removed elem {repr_elem(elem)}"
                                            )
                                        else:
                                            logger.info(
                                                f"Would have removed elem {repr_elem(elem)}"
                                            )
                                        cnt += 1
                                    elem_n += 1
    qualifier = ""
    if dry_run:
        qualifier = "would have "
    logger.info(
        f"{qualifier}removed {cnt} <{elem_to_remove_tag}> elements "
        + f"descendent from parent element {parent_elem_tag}, "
        + f"from grandparent element {grandparent_elem_tag}, "
        + f"from great-grandparent element {great_grandparent_elem_tag}, "
    )
    return cnt


def remove_second_p_element_from_every_matching_template(
    root: etree._Element, mood: Mood, tense: Tense, dry_run: bool = True
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
