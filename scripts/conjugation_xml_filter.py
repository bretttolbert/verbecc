"""
This script was used to remove unwanted tense elements
(e.g. compound tenses) from the mlconjug conjugation XML files
"""

from lxml import etree, objectify
import os
from typing import List
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.mood import Mood

working_dir = "../verbecc/data"
in_file = "conjugations-ro.xml"
out_file = "conjugations-ro.mod.xml"


def remove_mood_tense(root: etree._Element, tenses_to_remove: List[Tense]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                for tense_elem in mood_elem:
                    if tense_elem.tag in tenses_to_remove:
                        mood_elem.remove(tense_elem)
                        removed_elem_cnt += 1
    print("removed {} elements".format(removed_elem_cnt))


def remove_mood(root: etree._Element, moods_to_remove: List[Mood]) -> None:
    removed_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            for mood_elem in template_elem:
                if mood_elem.tag in moods_to_remove:
                    template_elem.remove(mood_elem)
                    removed_elem_cnt += 1
    print("removed {} elements".format(removed_elem_cnt))


def move_tense(
    root: etree._Element,
    tense_name: Tense,
    old_mood: Mood,
    new_mood: Mood,
    remove_old_mood: bool,
) -> None:
    moved_elem_cnt = 0
    for template_elem in root:
        if template_elem.tag == "template":
            tense_elem_to_move = None
            # find tense to move
            for mood_elem in template_elem:
                if mood_elem.tag == old_mood:
                    for tense_elem in mood_elem:
                        if tense_elem.tag == tense_name:
                            tense_elem_to_move = tense_elem
                            mood_elem.remove(tense_elem)
                            if remove_old_mood:
                                mood_elem.getparent().remove(mood_elem)
                            break
            # Now move it
            if tense_elem_to_move is not None:
                for mood_elem in template_elem:
                    if mood_elem.tag == new_mood:
                        mood_elem.append(tense_elem)
                        moved_elem_cnt += 1
    print("moved {} elements".format(moved_elem_cnt))


def main() -> None:
    parser = etree.XMLParser(dtd_validation=False, encoding="utf-8")
    tree = etree.parse(os.path.join(working_dir, in_file), parser)
    root = tree.getroot()

    remove_mood(root, ["Conditional"])
    # remove_mood_tense(root, ['perfect'])
    # move_tense(root, 'Viitor-II-popular', 'Viitor', 'Indicativ', True)

    with open(os.path.join(working_dir, out_file), "wb") as f:
        objectify.deannotate(root, cleanup_namespaces=True)
        xml = etree.tostring(
            tree,
            encoding="utf-8",
            method="xml",
            pretty_print=True,
            xml_declaration=True,
        )
        f.write(xml)


if __name__ == "__main__":
    main()
