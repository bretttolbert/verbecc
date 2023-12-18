# -*- coding: utf-8 -*-

import pytest

from verbecc.conjugator import Conjugator

cg = Conjugator(lang="ro")


def test_all_verbs_have_templates():
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


test_ro_conjugate_mood_tense_data = [
    ("avea", "participiu", "participiu", False, ["avut"]),
    ("face", "participiu", "participiu", False, ["făcut"]),
    (
        "avea",
        "indicativ",
        "prezent",
        False,
        ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"],
    ),
    (
        "avea",
        "indicativ",
        "prezent",
        True,
        ["eu am", "tu ai", "el are", "noi avem", "voi aveţi", "ei au"],
    ),
    (
        "avea",
        "indicativ",
        "imperfect",
        False,
        ["eu aveam", "tu aveai", "el avea", "noi aveam", "voi aveaţi", "ei aveau"],
    ),
    (
        "avea",
        "indicativ",
        "perfect-simplu",
        False,
        ["eu avui", "tu avuși", "el avu", "noi avurăm", "voi avurăţi", "ei avură"],
    ),
    (
        "avea",
        "indicativ",
        "perfect-compus",
        False,
        [
            "eu am avut",
            "tu ai avut",
            "el a avut",
            "noi am avut",
            "voi aţi avut",
            "ei au avut",
        ],
    ),
    (
        "avea",
        "indicativ",
        "mai-mult-ca-perfect",
        False,
        [
            "eu avusem",
            "tu avuseși",
            "el avuse",
            "noi avuserăm",
            "voi avuserăţi",
            "ei avuseră",
        ],
    ),
    (
        "face",
        "indicativ",
        "prezent",
        False,
        ["eu fac", "tu faci", "el face", "noi facem", "voi faceţi", "ei fac"],
    ),
    (
        "face",
        "indicativ",
        "imperfect",
        False,
        [
            "eu făceam",
            "tu făceai",
            "el făcea",
            "noi făceam",
            "voi făceaţi",
            "ei făceau",
        ],
    ),
    (
        "face",
        "indicativ",
        "perfect-simplu",
        False,
        [
            "eu făcui",
            "tu făcuși",
            "el făcu",
            "noi făcurăm",
            "voi făcurăţi",
            "ei făcură",
        ],
    ),
    (
        "face",
        "indicativ",
        "perfect-compus",
        False,
        [
            "eu am făcut",
            "tu ai făcut",
            "el a făcut",
            "noi am făcut",
            "voi aţi făcut",
            "ei au făcut",
        ],
    ),
    (
        "face",
        "indicativ",
        "mai-mult-ca-perfect",
        False,
        [
            "eu făcusem",
            "tu făcuseși",
            "el făcuse",
            "noi făcuserăm",
            "voi făcuserăţi",
            "ei făcuseră",
        ],
    ),
    (
        "voi",
        "indicativ",
        "prezent",
        False,
        ["eu voiesc", "tu voiești", "el voiește", "noi voim", "voi voiţi", "ei voiesc"],
    ),
    (
        "voi",
        "indicativ",
        "prezent",
        True,
        ["eu voi", "tu vei", "el va", "noi vom", "voi veţi", "ei vor"],
    ),
    (
        "face",
        "indicativ",
        "viitor-1",
        False,
        [
            "eu voi face",
            "tu vei face",
            "el va face",
            "noi vom face",
            "voi veţi face",
            "ei vor face",
        ],
    ),
    (
        "face",
        "indicativ",
        "viitor-2",
        False,
        [
            "eu voi fi făcut",
            "tu vei fi făcut",
            "el va fi făcut",
            "noi vom fi făcut",
            "voi veţi fi făcut",
            "ei vor fi făcut",
        ],
    ),
    (
        "face",
        "conjunctiv",
        "prezent",
        False,
        [
            "eu să fac",
            "tu să faci",
            "el să facă",
            "noi să facem",
            "voi să faceţi",
            "ei să facă",
        ],
    ),
    (
        "face",
        "conjunctiv",
        "perfect",
        False,
        [
            "eu să fi făcut",
            "tu să fi făcut",
            "el să fi făcut",
            "noi să fi făcut",
            "voi să fi făcut",
            "ei să fi făcut",
        ],
    ),
    (
        "face",
        "indicativ",
        "viitor-1-popular",
        False,
        [
            "eu o să fac",
            "tu o să faci",
            "el o să facă",
            "noi o să facem",
            "voi o să faceţi",
            "ei o să facă",
        ],
    ),
    (
        "face",
        "indicativ",
        "viitor-2-popular",
        False,
        [
            "eu am să fi făcut",
            "tu ai să fi făcut",
            "el are să fi făcut",
            "noi avem să fi făcut",
            "voi aveţi să fi făcut",
            "ei au să fi făcut",
        ],
    ),
    (
        "avea",
        "conjunctiv",
        "prezent",
        False,
        [
            "eu să am",
            "tu să ai",
            "el să aibă",
            "noi să avem",
            "voi să aveţi",
            "ei să aibă",
        ],
    ),
    (
        "avea",
        "conditional",
        "prezent",
        False,
        [
            "eu aş avea",
            "tu ai avea",
            "el ar avea",
            "noi am avea",
            "voi aţi avea",
            "ei ar avea",
        ],
    ),
    (
        "avea",
        "conditional",
        "perfect",
        False,
        [
            "eu aş fi avut",
            "tu ai fi avut",
            "el ar fi avut",
            "noi am fi avut",
            "voi aţi fi avut",
            "ei ar fi avut",
        ],
    ),
]


@pytest.mark.parametrize(
    "infinitive,mood,tense,alternate,expected_result", test_ro_conjugate_mood_tense_data
)
def test_inflector_ro_conjugate_mood_tense(
    infinitive, mood, tense, alternate, expected_result
):
    assert (
        cg.conjugate_mood_tense(infinitive, mood, tense, alternate) == expected_result
    )


test_inflector_ro_get_default_pronoun_data = [
    ("1s", "m", False, "eu"),
    ("1s", "m", True, "eu mă"),
    ("2s", "m", False, "tu"),
    ("2s", "m", True, "tu te"),
    ("3s", "m", False, "el"),
    ("3s", "m", True, "el se"),
    ("3s", "f", False, "ea"),
    ("3s", "f", True, "ea se"),
    ("1p", "m", False, "noi"),
    ("1p", "m", True, "noi ne"),
    ("2p", "m", False, "voi"),
    ("2p", "m", True, "voi vă"),
    ("3p", "m", False, "ei"),
    ("3p", "m", True, "ei se"),
    ("3p", "f", False, "ele"),
    ("3p", "f", True, "ele se"),
]


@pytest.mark.parametrize(
    "person,gender,is_reflexive,expected_result",
    test_inflector_ro_get_default_pronoun_data,
)
def test_inflector_ro_get_default_pronoun(
    person, gender, is_reflexive, expected_result
):
    assert (
        cg._inflector._get_default_pronoun(person, gender, is_reflexive=is_reflexive)
        == expected_result
    )
