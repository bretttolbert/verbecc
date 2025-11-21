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
                    "n": "s",
                    "p": "1",
                    "pr": "jo",
                },
                {
                    "c": ["tu series", "tu fores"],
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
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres seríeu", "vosaltres fóreu"],
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
        "gerundi": {"gerundi": [{"c": ["sent", "essent"]}]},
        "imperatiu": {
            "imperatiu-present": [
                {"c": ["sigues"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "indicatiu": {
            "futur": [
                {"c": ["jo seré"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu seràs"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell serà"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella serà"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["nosaltres serem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["vosaltres sereu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["ells seran"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles seran"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imperfet": [
                {"c": ["jo era"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu eres"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell era"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella era"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres érem"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres éreu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells eren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles eren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passat-simple": [
                {"c": ["jo fui"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu fores"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell fou"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella fou"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres fórem"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres fóreu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["jo sóc"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu ets"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell és"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella és"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres som"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres sou"],
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells són"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles són"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitiu": {"infinitiu-present": [{"c": ["ser", "ésser"]}]},
        "participi": {
            "participi": [
                {"c": ["estat", "sigut"], "g": "m", "n": "s"},
                {"c": ["estada", "siguda"], "g": "m", "n": "p"},
                {"c": ["estats", "siguts"], "g": "f", "n": "s"},
                {
                    "c": ["estades", "sigudes"],
                    "g": "f",
                    "n": "p",
                },
            ]
        },
        "subjuntiu": {
            "imperfet": [
                {"c": ["jo fos"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu fossis"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell fos"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella fos"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres fóssim"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres fóssiu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["ells fossin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["elles fossin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["jo sigui"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["tu siguis"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ell sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["ella sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["nosaltres siguem"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["vosaltres sigueu"],
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
                {"c": ["seria", "fora"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["series", "fores"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["seria", "fora"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["seria", "fora"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {
                    "c": ["seríem", "fórem"],
                    "n": "p",
                    "p": "1",
                    "pr": "nosaltres",
                },
                {
                    "c": ["seríeu", "fóreu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vosaltres",
                },
                {"c": ["serien", "foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["serien", "foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "gerundi": {"gerundi": [{"c": ["sent", "essent"]}]},
        "imperatiu": {
            "imperatiu-present": [
                {"c": ["sigues"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["siguin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["siguin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ]
        },
        "indicatiu": {
            "futur": [
                {"c": ["seré"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["seràs"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["serà"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["serà"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["serem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sereu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["seran"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["seran"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imperfet": [
                {"c": ["era"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["eres"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["era"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["era"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["érem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["éreu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["eren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["eren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passat-simple": [
                {"c": ["fui"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["fores"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["fou"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["fou"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["fórem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["fóreu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["foren"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["foren"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["sóc"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["ets"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["és"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["és"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["som"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sou"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["són"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["són"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitiu": {"infinitiu-present": [{"c": ["ser", "ésser"]}]},
        "participi": {
            "participi": [
                {"c": ["estat", "sigut"], "g": "m", "n": "s"},
                {"c": ["estada", "siguda"], "g": "m", "n": "p"},
                {"c": ["estats", "siguts"], "g": "f", "n": "s"},
                {"c": ["estades", "sigudes"], "g": "f", "n": "p"},
            ]
        },
        "subjuntiu": {
            "imperfet": [
                {"c": ["fos"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["fossis"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["fos"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["fos"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["fóssim"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["fóssiu"], "n": "p", "p": "2", "pr": "vosaltres"},
                {"c": ["fossin"], "g": "m", "n": "p", "p": "3", "pr": "ells"},
                {"c": ["fossin"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "present": [
                {"c": ["sigui"], "n": "s", "p": "1", "pr": "jo"},
                {"c": ["siguis"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["sigui"], "g": "m", "n": "s", "p": "3", "pr": "ell"},
                {"c": ["sigui"], "g": "f", "n": "s", "p": "3", "pr": "ella"},
                {"c": ["siguem"], "n": "p", "p": "1", "pr": "nosaltres"},
                {"c": ["sigueu"], "n": "p", "p": "2", "pr": "vosaltres"},
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
