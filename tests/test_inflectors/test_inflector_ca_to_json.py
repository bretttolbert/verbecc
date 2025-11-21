import pytest
import json

from tests.common import assert_json_str_equal

from verbecc.src.conjugator.complete_conjugator import CompleteConjugator
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


@pytest.fixture(scope="module")
def ccg():
    ccg = CompleteConjugator(lang=Lang.ca)
    yield ccg


expected_value_conj_ser = {
    "moods": {
        "condicional": {
            "present": [
                {
                    "c": ["jo seria", "jo fora"],
                    "g": None,
                    "n": "s",
                    "p": "1",
                    "pr": "jo",
                },
                {
                    "c": ["tu series", "tu fores"],
                    "g": None,
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {
                    "c": ["ell seria", "ell fora"],
                    "g": "m",
                    "n": "s",
                    "p": "3",
                    "pr": "ell",
                },
                {
                    "c": ["ella seria", "ella fora"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "ella",
                },
                {
                    "c": ["nosaltres seríem", "nosaltres fórem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres seríeu", "vosaltres fóreu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {
                    "c": ["ells serien", "ells foren"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ells",
                },
                {
                    "c": ["elles serien", "elles foren"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ]
        },
        "gerundi": {
            "gerundi": [
                {"c": ["sent", "essent"], "g": None, "n": None, "p": None, "pr": None}
            ]
        },
        "imperatiu": {
            "imperatiu-present": [
                {"c": ["sigues"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "indicatiu": {
            "futur": [
                {"c": ["jo seré"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu seràs"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell serà"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella serà"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres serem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres sereu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells seran"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles seran"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imperfet": [
                {"c": ["jo era"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu eres"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell era"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella era"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres érem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres éreu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells eren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles eren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passat-simple": [
                {"c": ["jo fui"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu fores"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell fou"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella fou"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres fórem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres fóreu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["jo sóc"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu ets"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell és"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella és"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres som"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres sou"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells són"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles són"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitiu": {
            "infinitiu-present": [
                {"c": ["ser", "ésser"], "g": None, "n": None, "p": None, "pr": None}
            ]
        },
        "participi": {
            "participi": [
                {"c": ["estat", "sigut"], "g": "m", "n": "s", "p": None, "pr": None},
                {"c": ["estada", "siguda"], "g": "m", "n": "p", "p": None, "pr": None},
                {"c": ["estats", "siguts"], "g": "f", "n": "s", "p": None, "pr": None},
                {
                    "c": ["estades", "sigudes"],
                    "g": "f",
                    "n": "p",
                    "p": None,
                    "pr": None,
                },
            ]
        },
        "subjuntiu": {
            "imperfet": [
                {"c": ["jo fos"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu fossis"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell fos"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella fos"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres fóssim"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres fóssiu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells fossin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles fossin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["jo sigui"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu siguis"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres siguem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres sigueu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
    },
    "verb": {
        "infinitive": "ser",
        "lang": "ca",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "",
        "template": "és:ser",
        "translation_en": "be",
    },
}

expected_value_conj_ser_nopronouns = {
    "moods": {
        "condicional": {
            "present": [
                {"c": ["seria", "fora"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["series", "fores"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["seria", "fora"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["seria", "fora"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["seríem", "fórem"],
                    "g": None,
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["seríeu", "fóreu"],
                    "g": None,
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["serien", "foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["serien", "foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "gerundi": {
            "gerundi": [
                {"c": ["sent", "essent"], "g": None, "n": None, "p": None, "pr": None}
            ]
        },
        "imperatiu": {
            "imperatiu-present": [
                {"c": ["sigues"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "indicatiu": {
            "futur": [
                {"c": ["seré"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["seràs"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["serà"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["serà"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["serem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sereu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["seran"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["seran"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imperfet": [
                {"c": ["era"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["eres"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["era"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["era"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["érem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["éreu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["eren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["eren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passat-simple": [
                {"c": ["fui"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["fores"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["fou"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["fou"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["fórem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["fóreu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["sóc"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["ets"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["és"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["és"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["som"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sou"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["són"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["són"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitiu": {
            "infinitiu-present": [
                {"c": ["ser", "ésser"], "g": None, "n": None, "p": None, "pr": None}
            ]
        },
        "participi": {
            "participi": [
                {"c": ["estat", "sigut"], "g": "m", "n": "s", "p": None, "pr": None},
                {"c": ["estada", "siguda"], "g": "m", "n": "p", "p": None, "pr": None},
                {"c": ["estats", "siguts"], "g": "f", "n": "s", "p": None, "pr": None},
                {
                    "c": ["estades", "sigudes"],
                    "g": "f",
                    "n": "p",
                    "p": None,
                    "pr": None,
                },
            ]
        },
        "subjuntiu": {
            "imperfet": [
                {"c": ["fos"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["fossis"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["fos"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["fos"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["fóssim"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["fóssiu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["fossin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["fossin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["sigui"], "g": None, "n": "s", "p": "1", "pr": "jo"},
                {"c": ["siguis"], "g": None, "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "g": None, "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "g": None, "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
    },
    "verb": {
        "infinitive": "ser",
        "lang": "ca",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "",
        "template": "és:ser",
        "translation_en": "be",
    },
}


def test_inflector_ca_conjugate_ser_to_json(ccg):
    cc = ccg.conjugate("ser")
    assert_json_str_equal(str(cc), json.dumps(expected_value_conj_ser))


def test_inflector_conjugate_ser_noconjpronouns_to_json(ccg):
    cc = ccg.conjugate("ser", conjugate_pronouns=False)
    assert_json_str_equal(str(cc), json.dumps(expected_value_conj_ser_nopronouns))
