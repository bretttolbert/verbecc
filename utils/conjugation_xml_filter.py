# -*- coding: utf-8 -*-

from lxml import etree, objectify
import os

"""
This script was used to remove unwanted tense elements
(e.g. compound tenses) from the mlconjug conjugation XML files
"""

working_dir = '../verbecc/data'
in_file = "conjugations-pt.xml"
out_file = "conjugations-pt.mod.xml"
tenses_to_remove = ['Conjuntivo--Subjuntivo-Futuro-Composto']

def remove_mood_tense():
    removed_elem_cnt = 0
    tenses = set()
    parser = etree.XMLParser(dtd_validation=True, encoding='utf-8')
    tree = etree.parse(os.path.join(working_dir, in_file), parser)
    root = tree.getroot()
    for template_elem in root:
        if template_elem.tag == 'template':
            for mood_elem in template_elem:
                for tense_elem in mood_elem:
                    tenses.add(tense_elem.tag)
                    if tense_elem.tag in tenses_to_remove:
                        mood_elem.remove(tense_elem)
                        removed_elem_cnt += 1

    with open(os.path.join(working_dir, out_file), 'wb') as f:
        objectify.deannotate(root, cleanup_namespaces=True)
        xml = etree.tostring(tree, encoding='utf-8', method='xml', pretty_print=True, xml_declaration=True)
        f.write(xml)
        print("removed {} elements".format(removed_elem_cnt))
    
remove_mood_tense()
