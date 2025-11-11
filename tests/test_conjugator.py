import pytest
import json

from tests.common import assert_json_str_equal

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.exceptions import (
    InvalidMoodError,
    InvalidTenseError,
    TemplateNotFoundError,
)
from verbecc.src.defs.constants import config


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang=Lang.fr)
    yield cg


def test_get_infinitives(cg):
    infinitives = cg.get_infinitives()
    assert len(infinitives) > 7000
    assert "parler" in infinitives


def test_get_template_names(cg):
    template_names = cg.get_template_names()
    assert len(template_names) >= 146
    assert "aim:er" in template_names


test_verbs = [
    ("manger"),
    ("venir"),
    ("être"),
    ("aller"),
    ("pouvoir"),
    ("finir"),
    ("pleuvoir"),
]


@pytest.mark.parametrize("infinitive", test_verbs)
def test_conjugator_conjugate_basic(cg, infinitive):
    output = cg.conjugate(infinitive)
    assert output


def test_conjugator_predict_conjugation_er_verb_indicative_present(cg):
    if config.ENABLE_ML_PREDICTION:
        tc = cg.conjugate_mood_tense("ubériser", "indicatif", "présent")
        assert [c[0] for c in tc] == [
            "j'ubérise",
            "tu ubérises",
            "il ubérise",
            "nous ubérisons",
            "vous ubérisez",
            "ils ubérisent",
        ]


def test_conjugator_predict_conjugation_re_verb_indicative_present(cg):
    if config.ENABLE_ML_PREDICTION:
        tc = cg.conjugate_mood_tense("brettre", "indicatif", "présent")
        assert [c[0] for c in tc] == [
            "je brets",
            "tu brets",
            "il bret",
            "nous brettons",
            "vous brettez",
            "ils brettent",
        ]


def test_conjugator_conjugate_passe_compose_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "passé-composé")
    assert [c[0] for c in tc] == [
        "j'ai mangé",
        "tu as mangé",
        "il a mangé",
        "nous avons mangé",
        "vous avez mangé",
        "ils ont mangé",
    ]


def test_conjugator_conjugate_passe_compose_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "passé-composé")
    assert [c[0] for c in tc] == [
        "je suis allé",
        "tu es allé",
        "il est allé",
        "nous sommes allés",
        "vous êtes allés",
        "ils sont allés",
    ]


def test_conjugator_conjugate_subjonctif_passe_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "subjonctif", "passé")
    assert [c[0] for c in tc] == [
        "que j'aie mangé",
        "que tu aies mangé",
        "qu'il ait mangé",
        "que nous ayons mangé",
        "que vous ayez mangé",
        "qu'ils aient mangé",
    ]


def test_conjugator_conjugate_subjonctif_passe_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "subjonctif", "passé")
    assert [c[0] for c in tc] == [
        "que je sois allé",
        "que tu sois allé",
        "qu'il soit allé",
        "que nous soyons allés",
        "que vous soyez allés",
        "qu'ils soient allés",
    ]


def test_conjugator_conjugate_conditionnel_passe_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "conditionnel", "passé")
    assert [c[0] for c in tc] == [
        "j'aurais mangé",
        "tu aurais mangé",
        "il aurait mangé",
        "nous aurions mangé",
        "vous auriez mangé",
        "ils auraient mangé",
    ]


def test_conjugator_conjugate_conditionnel_passe_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "conditionnel", "passé")
    assert [c[0] for c in tc] == [
        "je serais allé",
        "tu serais allé",
        "il serait allé",
        "nous serions allés",
        "vous seriez allés",
        "ils seraient allés",
    ]


def test_conjugator_conjugate_plusqueparfait_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "j'avais mangé",
        "tu avais mangé",
        "il avait mangé",
        "nous avions mangé",
        "vous aviez mangé",
        "ils avaient mangé",
    ]


def test_conjugator_conjugate_plusqueparfait_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "j'étais allé",
        "tu étais allé",
        "il était allé",
        "nous étions allés",
        "vous étiez allés",
        "ils étaient allés",
    ]


def test_conjugator_conjugate_subjonctif_plusqueparfait_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "subjonctif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "que j'eusse mangé",
        "que tu eusses mangé",
        "qu'il eût mangé",
        "que nous eussions mangé",
        "que vous eussiez mangé",
        "qu'ils eussent mangé",
    ]


def test_conjugator_conjugate_subjonctif_plusqueparfait_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "subjonctif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "que je fusse allé",
        "que tu fusses allé",
        "qu'il fût allé",
        "que nous fussions allés",
        "que vous fussiez allés",
        "qu'ils fussent allés",
    ]


def test_conjugator_conjugate_futur_anterieur_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "futur-antérieur")
    assert [c[0] for c in tc] == [
        "j'aurai mangé",
        "tu auras mangé",
        "il aura mangé",
        "nous aurons mangé",
        "vous aurez mangé",
        "ils auront mangé",
    ]


def test_conjugator_conjugate_futur_anterieur_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "futur-antérieur")
    assert [c[0] for c in tc] == [
        "je serai allé",
        "tu seras allé",
        "il sera allé",
        "nous serons allés",
        "vous serez allés",
        "ils seront allés",
    ]


def test_conjugator_conjugate_passe_anterieur_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "passé-antérieur")
    assert [c[0] for c in tc] == [
        "j'eus mangé",
        "tu eus mangé",
        "il eut mangé",
        "nous eûmes mangé",
        "vous eûtes mangé",
        "ils eurent mangé",
    ]


def test_conjugator_conjugate_passe_anterieur_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "passé-antérieur")
    assert [c[0] for c in tc] == [
        "je fus allé",
        "tu fus allé",
        "il fut allé",
        "nous fûmes allés",
        "vous fûtes allés",
        "ils furent allés",
    ]


def test_conjugator_conjugate_imperatif_passe_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "imperatif", "imperatif-passé")
    assert [c[0] for c in tc] == [
        "aie mangé",
        "ayons mangé",
        "ayez mangé",
    ]


def test_conjugator_conjugate_imperatif_passe_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "imperatif", "imperatif-passé")
    assert [c[0] for c in tc] == [
        "sois allé",
        "soyons allés",
        "soyez allés",
    ]


expected_resp_conj_manger = {
    "moods": {
        "conditionnel": {
            "passé": [
                ["1", "s", "m", "je", ["j'aurais mangé"]],
                ["2", "s", "m", "tu", ["tu aurais mangé"]],
                ["3", "s", "m", "il", ["il aurait mangé"]],
                ["1", "p", "m", "nous", ["nous aurions mangé"]],
                ["2", "p", "m", "vous", ["vous auriez mangé"]],
                ["3", "p", "m", "ils", ["ils auraient mangé"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je mangerais"]],
                ["2", "s", "m", "tu", ["tu mangerais"]],
                ["3", "s", "m", "il", ["il mangerait"]],
                ["1", "p", "m", "nous", ["nous mangerions"]],
                ["2", "p", "m", "vous", ["vous mangeriez"]],
                ["3", "p", "m", "ils", ["ils mangeraient"]],
            ],
        },
        "imperatif": {
            "imperatif-passé": [
                ["2", "s", "m", "tu", ["aie mangé"]],
                ["1", "p", "m", "nous", ["ayons mangé"]],
                ["2", "p", "m", "vous", ["ayez mangé"]],
            ],
            "imperatif-présent": [
                ["2", "s", "m", "tu", ["mange"]],
                ["1", "p", "m", "nous", ["mangeons"]],
                ["2", "p", "m", "vous", ["mangez"]],
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", "m", "je", ["j'aurai mangé"]],
                ["2", "s", "m", "tu", ["tu auras mangé"]],
                ["3", "s", "m", "il", ["il aura mangé"]],
                ["1", "p", "m", "nous", ["nous aurons mangé"]],
                ["2", "p", "m", "vous", ["vous aurez mangé"]],
                ["3", "p", "m", "ils", ["ils auront mangé"]],
            ],
            "futur-simple": [
                ["1", "s", "m", "je", ["je mangerai"]],
                ["2", "s", "m", "tu", ["tu mangeras"]],
                ["3", "s", "m", "il", ["il mangera"]],
                ["1", "p", "m", "nous", ["nous mangerons"]],
                ["2", "p", "m", "vous", ["vous mangerez"]],
                ["3", "p", "m", "ils", ["ils mangeront"]],
            ],
            "imparfait": [
                ["1", "s", "m", "je", ["je mangeais"]],
                ["2", "s", "m", "tu", ["tu mangeais"]],
                ["3", "s", "m", "il", ["il mangeait"]],
                ["1", "p", "m", "nous", ["nous mangions"]],
                ["2", "p", "m", "vous", ["vous mangiez"]],
                ["3", "p", "m", "ils", ["ils mangeaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", "m", "je", ["j'eus mangé"]],
                ["2", "s", "m", "tu", ["tu eus mangé"]],
                ["3", "s", "m", "il", ["il eut mangé"]],
                ["1", "p", "m", "nous", ["nous eûmes mangé"]],
                ["2", "p", "m", "vous", ["vous eûtes mangé"]],
                ["3", "p", "m", "ils", ["ils eurent mangé"]],
            ],
            "passé-composé": [
                ["1", "s", "m", "je", ["j'ai mangé"]],
                ["2", "s", "m", "tu", ["tu as mangé"]],
                ["3", "s", "m", "il", ["il a mangé"]],
                ["1", "p", "m", "nous", ["nous avons mangé"]],
                ["2", "p", "m", "vous", ["vous avez mangé"]],
                ["3", "p", "m", "ils", ["ils ont mangé"]],
            ],
            "passé-simple": [
                ["1", "s", "m", "je", ["je mangeai"]],
                ["2", "s", "m", "tu", ["tu mangeas"]],
                ["3", "s", "m", "il", ["il mangea"]],
                ["1", "p", "m", "nous", ["nous mangeâmes"]],
                ["2", "p", "m", "vous", ["vous mangeâtes"]],
                ["3", "p", "m", "ils", ["ils mangèrent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["j'avais mangé"]],
                ["2", "s", "m", "tu", ["tu avais mangé"]],
                ["3", "s", "m", "il", ["il avait mangé"]],
                ["1", "p", "m", "nous", ["nous avions mangé"]],
                ["2", "p", "m", "vous", ["vous aviez mangé"]],
                ["3", "p", "m", "ils", ["ils avaient mangé"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je mange"]],
                ["2", "s", "m", "tu", ["tu manges"]],
                ["3", "s", "m", "il", ["il mange"]],
                ["1", "p", "m", "nous", ["nous mangeons"]],
                ["2", "p", "m", "vous", ["vous mangez"]],
                ["3", "p", "m", "ils", ["ils mangent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", "m", "je", ["manger"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", "je", ["mangé"]],
                [None, "p", "m", "nous", ["mangés"]],
                [None, "s", "m", "je", ["mangée"]],
                [None, "p", "m", "nous", ["mangées"]],
            ],
            "participe-présent": [[None, "s", "m", "je", ["mangeant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", "m", "je", ["que je mangeasse"]],
                ["2", "s", "m", "tu", ["que tu mangeasses"]],
                ["3", "s", "m", "il", ["qu'il mangeât"]],
                ["1", "p", "m", "nous", ["que nous mangeassions"]],
                ["2", "p", "m", "vous", ["que vous mangeassiez"]],
                ["3", "p", "m", "ils", ["qu'ils mangeassent"]],
            ],
            "passé": [
                ["1", "s", "m", "je", ["que j'aie mangé"]],
                ["2", "s", "m", "tu", ["que tu aies mangé"]],
                ["3", "s", "m", "il", ["qu'il ait mangé"]],
                ["1", "p", "m", "nous", ["que nous ayons mangé"]],
                ["2", "p", "m", "vous", ["que vous ayez mangé"]],
                ["3", "p", "m", "ils", ["qu'ils aient mangé"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["que j'eusse mangé"]],
                ["2", "s", "m", "tu", ["que tu eusses mangé"]],
                ["3", "s", "m", "il", ["qu'il eût mangé"]],
                ["1", "p", "m", "nous", ["que nous eussions mangé"]],
                ["2", "p", "m", "vous", ["que vous eussiez mangé"]],
                ["3", "p", "m", "ils", ["qu'ils eussent mangé"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["que je mange"]],
                ["2", "s", "m", "tu", ["que tu manges"]],
                ["3", "s", "m", "il", ["qu'il mange"]],
                ["1", "p", "m", "nous", ["que nous mangions"]],
                ["2", "p", "m", "vous", ["que vous mangiez"]],
                ["3", "p", "m", "ils", ["qu'ils mangent"]],
            ],
        },
    },
    "verb": {
        "infinitive": "manger",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "man",
        "template": "man:ger",
        "translation_en": "eat",
    },
}

expected_resp_conj_pouvoir = {
    "moods": {
        "conditionnel": {
            "passé": [
                ["1", "s", "m", "je", ["j'aurais pu"]],
                ["2", "s", "m", "tu", ["tu aurais pu"]],
                ["3", "s", "m", "il", ["il aurait pu"]],
                ["1", "p", "m", "nous", ["nous aurions pu"]],
                ["2", "p", "m", "vous", ["vous auriez pu"]],
                ["3", "p", "m", "ils", ["ils auraient pu"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je pourrais"]],
                ["2", "s", "m", "tu", ["tu pourrais"]],
                ["3", "s", "m", "il", ["il pourrait"]],
                ["1", "p", "m", "nous", ["nous pourrions"]],
                ["2", "p", "m", "vous", ["vous pourriez"]],
                ["3", "p", "m", "ils", ["ils pourraient"]],
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", "m", "je", ["j'aurai pu"]],
                ["2", "s", "m", "tu", ["tu auras pu"]],
                ["3", "s", "m", "il", ["il aura pu"]],
                ["1", "p", "m", "nous", ["nous aurons pu"]],
                ["2", "p", "m", "vous", ["vous aurez pu"]],
                ["3", "p", "m", "ils", ["ils auront pu"]],
            ],
            "futur-simple": [
                ["1", "s", "m", "je", ["je pourrai"]],
                ["2", "s", "m", "tu", ["tu pourras"]],
                ["3", "s", "m", "il", ["il pourra"]],
                ["1", "p", "m", "nous", ["nous pourrons"]],
                ["2", "p", "m", "vous", ["vous pourrez"]],
                ["3", "p", "m", "ils", ["ils pourront"]],
            ],
            "imparfait": [
                ["1", "s", "m", "je", ["je pouvais"]],
                ["2", "s", "m", "tu", ["tu pouvais"]],
                ["3", "s", "m", "il", ["il pouvait"]],
                ["1", "p", "m", "nous", ["nous pouvions"]],
                ["2", "p", "m", "vous", ["vous pouviez"]],
                ["3", "p", "m", "ils", ["ils pouvaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", "m", "je", ["j'eus pu"]],
                ["2", "s", "m", "tu", ["tu eus pu"]],
                ["3", "s", "m", "il", ["il eut pu"]],
                ["1", "p", "m", "nous", ["nous eûmes pu"]],
                ["2", "p", "m", "vous", ["vous eûtes pu"]],
                ["3", "p", "m", "ils", ["ils eurent pu"]],
            ],
            "passé-composé": [
                ["1", "s", "m", "je", ["j'ai pu"]],
                ["2", "s", "m", "tu", ["tu as pu"]],
                ["3", "s", "m", "il", ["il a pu"]],
                ["1", "p", "m", "nous", ["nous avons pu"]],
                ["2", "p", "m", "vous", ["vous avez pu"]],
                ["3", "p", "m", "ils", ["ils ont pu"]],
            ],
            "passé-simple": [
                ["1", "s", "m", "je", ["je pus"]],
                ["2", "s", "m", "tu", ["tu pus"]],
                ["3", "s", "m", "il", ["il put"]],
                ["1", "p", "m", "nous", ["nous pûmes"]],
                ["2", "p", "m", "vous", ["vous pûtes"]],
                ["3", "p", "m", "ils", ["ils purent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["j'avais pu"]],
                ["2", "s", "m", "tu", ["tu avais pu"]],
                ["3", "s", "m", "il", ["il avait pu"]],
                ["1", "p", "m", "nous", ["nous avions pu"]],
                ["2", "p", "m", "vous", ["vous aviez pu"]],
                ["3", "p", "m", "ils", ["ils avaient pu"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je peux", "je puis"]],
                ["2", "s", "m", "tu", ["tu peux"]],
                ["3", "s", "m", "il", ["il peut"]],
                ["1", "p", "m", "nous", ["nous pouvons"]],
                ["2", "p", "m", "vous", ["vous pouvez"]],
                ["3", "p", "m", "ils", ["ils peuvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", "m", "je", ["pouvoir"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", "je", ["pu"]],
                [None, "p", "m", "nous", ["pus"]],
                [None, "s", "m", "je", ["pue"]],
                [None, "p", "m", "nous", ["pues"]],
            ],
            "participe-présent": [[None, "s", "m", "je", ["pouvant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", "m", "je", ["que je pusse"]],
                ["2", "s", "m", "tu", ["que tu pusses"]],
                ["3", "s", "m", "il", ["qu'il pût"]],
                ["1", "p", "m", "nous", ["que nous pussions"]],
                ["2", "p", "m", "vous", ["que vous pussiez"]],
                ["3", "p", "m", "ils", ["qu'ils pussent"]],
            ],
            "passé": [
                ["1", "s", "m", "je", ["que j'aie pu"]],
                ["2", "s", "m", "tu", ["que tu aies pu"]],
                ["3", "s", "m", "il", ["qu'il ait pu"]],
                ["1", "p", "m", "nous", ["que nous ayons pu"]],
                ["2", "p", "m", "vous", ["que vous ayez pu"]],
                ["3", "p", "m", "ils", ["qu'ils aient pu"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["que j'eusse pu"]],
                ["2", "s", "m", "tu", ["que tu eusses pu"]],
                ["3", "s", "m", "il", ["qu'il eût pu"]],
                ["1", "p", "m", "nous", ["que nous eussions pu"]],
                ["2", "p", "m", "vous", ["que vous eussiez pu"]],
                ["3", "p", "m", "ils", ["qu'ils eussent pu"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["que je puisse"]],
                ["2", "s", "m", "tu", ["que tu puisses"]],
                ["3", "s", "m", "il", ["qu'il puisse"]],
                ["1", "p", "m", "nous", ["que nous puissions"]],
                ["2", "p", "m", "vous", ["que vous puissiez"]],
                ["3", "p", "m", "ils", ["qu'ils puissent"]],
            ],
        },
    },
    "verb": {
        "infinitive": "pouvoir",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "p",
        "template": "p:ouvoir",
        "translation_en": "power",
    },
}


expected_resp_conj_pleuvoir = {
    "moods": {
        "conditionnel": {
            "passé": [
                ["3", "s", "m", "il", ["il aurait plu"]],
                ["3", "p", "m", "ils", ["ils auraient plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["il pleuvrait"]],
                ["3", "p", "m", "ils", ["ils pleuvraient"]],
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                ["3", "s", "m", "il", ["il aura plu"]],
                ["3", "p", "m", "ils", ["ils auront plu"]],
            ],
            "futur-simple": [
                ["3", "s", "m", "il", ["il pleuvra"]],
                ["3", "p", "m", "ils", ["ils pleuvront"]],
            ],
            "imparfait": [
                ["3", "s", "m", "il", ["il pleuvait"]],
                ["3", "p", "m", "ils", ["ils pleuvaient"]],
            ],
            "passé-antérieur": [
                ["3", "s", "m", "il", ["il eut plu"]],
                ["3", "p", "m", "ils", ["ils eurent plu"]],
            ],
            "passé-composé": [
                ["3", "s", "m", "il", ["il a plu"]],
                ["3", "p", "m", "ils", ["ils ont plu"]],
            ],
            "passé-simple": [
                ["3", "s", "m", "il", ["il plut"]],
                ["3", "p", "m", "ils", ["ils plurent"]],
            ],
            "plus-que-parfait": [
                ["3", "s", "m", "il", ["il avait plu"]],
                ["3", "p", "m", "ils", ["ils avaient plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["il pleut"]],
                ["3", "p", "m", "ils", ["ils pleuvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", "m", "je", ["pleuvoir"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", "je", ["plu"]],
                [None, "p", "m", "nous", ["plus"]],
                [None, "s", "m", "je", ["plue"]],
                [None, "p", "m", "nous", ["plues"]],
            ],
            "participe-présent": [[None, "s", "m", "je", ["pleuvant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["3", "s", "m", "il", ["qu'il plût"]],
                ["3", "p", "m", "ils", ["qu'ils plussent"]],
            ],
            "passé": [
                ["3", "s", "m", "il", ["qu'il ait plu"]],
                ["3", "p", "m", "ils", ["qu'ils aient plu"]],
            ],
            "plus-que-parfait": [
                ["3", "s", "m", "il", ["qu'il eût plu"]],
                ["3", "p", "m", "ils", ["qu'ils eussent plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["qu'il pleuve"]],
                ["3", "p", "m", "ils", ["qu'ils pleuvent"]],
            ],
        },
    },
    "verb": {
        "infinitive": "pleuvoir",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "pl",
        "template": "pl:euvoir",
        "translation_en": "rain",
    },
}

expected_resp_conj_se_lever = {
    "moods": {
        "conditionnel": {
            "passé": [
                ["1", "s", "m", "je", ["je me serais levé"]],
                ["2", "s", "m", "tu", ["tu te serais levé"]],
                ["3", "s", "m", "il", ["il se serait levé"]],
                ["1", "p", "m", "nous", ["nous nous serions levés"]],
                ["2", "p", "m", "vous", ["vous vous seriez levés"]],
                ["3", "p", "m", "ils", ["ils se seraient levés"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je me lèverais"]],
                ["2", "s", "m", "tu", ["tu te lèverais"]],
                ["3", "s", "m", "il", ["il se lèverait"]],
                ["1", "p", "m", "nous", ["nous nous lèverions"]],
                ["2", "p", "m", "vous", ["vous vous lèveriez"]],
                ["3", "p", "m", "ils", ["ils se lèveraient"]],
            ],
        },
        "imperatif": {
            "imperatif-passé": [],
            "imperatif-présent": [
                ["2", "s", "m", "tu", ["lève-toi"]],
                ["1", "p", "m", "nous", ["levons-nous"]],
                ["2", "p", "m", "vous", ["levez-vous"]],
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", "m", "je", ["je me serai levé"]],
                ["2", "s", "m", "tu", ["tu te seras levé"]],
                ["3", "s", "m", "il", ["il se sera levé"]],
                ["1", "p", "m", "nous", ["nous nous serons levés"]],
                ["2", "p", "m", "vous", ["vous vous serez levés"]],
                ["3", "p", "m", "ils", ["ils se seront levés"]],
            ],
            "futur-simple": [
                ["1", "s", "m", "je", ["je me lèverai"]],
                ["2", "s", "m", "tu", ["tu te lèveras"]],
                ["3", "s", "m", "il", ["il se lèvera"]],
                ["1", "p", "m", "nous", ["nous nous lèverons"]],
                ["2", "p", "m", "vous", ["vous vous lèverez"]],
                ["3", "p", "m", "ils", ["ils se lèveront"]],
            ],
            "imparfait": [
                ["1", "s", "m", "je", ["je me levais"]],
                ["2", "s", "m", "tu", ["tu te levais"]],
                ["3", "s", "m", "il", ["il se levait"]],
                ["1", "p", "m", "nous", ["nous nous levions"]],
                ["2", "p", "m", "vous", ["vous vous leviez"]],
                ["3", "p", "m", "ils", ["ils se levaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", "m", "je", ["je me fus levé"]],
                ["2", "s", "m", "tu", ["tu te fus levé"]],
                ["3", "s", "m", "il", ["il se fut levé"]],
                ["1", "p", "m", "nous", ["nous nous fûmes levés"]],
                ["2", "p", "m", "vous", ["vous vous fûtes levés"]],
                ["3", "p", "m", "ils", ["ils se furent levés"]],
            ],
            "passé-composé": [
                ["1", "s", "m", "je", ["je me suis levé"]],
                ["2", "s", "m", "tu", ["tu t'es levé"]],
                ["3", "s", "m", "il", ["il s'est levé"]],
                ["1", "p", "m", "nous", ["nous nous sommes levés"]],
                ["2", "p", "m", "vous", ["vous vous êtes levés"]],
                ["3", "p", "m", "ils", ["ils se sont levés"]],
            ],
            "passé-simple": [
                ["1", "s", "m", "je", ["je me levai"]],
                ["2", "s", "m", "tu", ["tu te levas"]],
                ["3", "s", "m", "il", ["il se leva"]],
                ["1", "p", "m", "nous", ["nous nous levâmes"]],
                ["2", "p", "m", "vous", ["vous vous levâtes"]],
                ["3", "p", "m", "ils", ["ils se levèrent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["je m'étais levé"]],
                ["2", "s", "m", "tu", ["tu t'étais levé"]],
                ["3", "s", "m", "il", ["il s'était levé"]],
                ["1", "p", "m", "nous", ["nous nous étions levés"]],
                ["2", "p", "m", "vous", ["vous vous étiez levés"]],
                ["3", "p", "m", "ils", ["ils s'étaient levés"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["je me lève"]],
                ["2", "s", "m", "tu", ["tu te lèves"]],
                ["3", "s", "m", "il", ["il se lève"]],
                ["1", "p", "m", "nous", ["nous nous levons"]],
                ["2", "p", "m", "vous", ["vous vous levez"]],
                ["3", "p", "m", "ils", ["ils se lèvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", "m", "je", ["se lever"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", "je", ["étant levé"]],
                [None, "p", "m", "nous", ["étant levés"]],
                [None, "s", "m", "je", ["étant levée"]],
                [None, "p", "m", "nous", ["étant levées"]],
            ],
            "participe-présent": [[None, "s", "m", "je", ["levant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", "m", "je", ["que je me levasse"]],
                ["2", "s", "m", "tu", ["que tu te levasses"]],
                ["3", "s", "m", "il", ["qu'il se levât"]],
                ["1", "p", "m", "nous", ["que nous nous levassions"]],
                ["2", "p", "m", "vous", ["que vous vous levassiez"]],
                ["3", "p", "m", "ils", ["qu'ils se levassent"]],
            ],
            "passé": [
                ["1", "s", "m", "je", ["que je me sois levé"]],
                ["2", "s", "m", "tu", ["que tu te sois levé"]],
                ["3", "s", "m", "il", ["qu'il se soit levé"]],
                ["1", "p", "m", "nous", ["que nous nous soyons levés"]],
                ["2", "p", "m", "vous", ["que vous vous soyez levés"]],
                ["3", "p", "m", "ils", ["qu'ils se soient levés"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "m", "je", ["que je me fusse levé"]],
                ["2", "s", "m", "tu", ["que tu te fusses levé"]],
                ["3", "s", "m", "il", ["qu'il se fût levé"]],
                ["1", "p", "m", "nous", ["que nous nous fussions levés"]],
                ["2", "p", "m", "vous", ["que vous vous fussiez levés"]],
                ["3", "p", "m", "ils", ["qu'ils se fussent levés"]],
            ],
            "présent": [
                ["1", "s", "m", "je", ["que je me lève"]],
                ["2", "s", "m", "tu", ["que tu te lèves"]],
                ["3", "s", "m", "il", ["qu'il se lève"]],
                ["1", "p", "m", "nous", ["que nous nous levions"]],
                ["2", "p", "m", "vous", ["que vous vous leviez"]],
                ["3", "p", "m", "ils", ["qu'ils se lèvent"]],
            ],
        },
    },
    "verb": {
        "infinitive": "lever",
        "pred_score": 1.0,
        "predicted": False,
        "stem": "l",
        "template": "l:ever",
        "translation_en": "lift",
    },
}


@pytest.mark.parametrize(
    "infinitive,expected_resp",
    [
        ("manger", expected_resp_conj_manger),
        ("pouvoir", expected_resp_conj_pouvoir),
        ("Pouvoir", expected_resp_conj_pouvoir),
        ("pleuvoir", expected_resp_conj_pleuvoir),
        ("Se lever", expected_resp_conj_se_lever),
    ],
)
def test_conjugator_conjugate(cg, infinitive, expected_resp):
    assert_json_str_equal(str(cg.conjugate(infinitive)), json.dumps(expected_resp))


def test_conjugator_conjugate_invalid_mood(cg):
    with pytest.raises(InvalidMoodError):
        cg.conjugate_mood("manger", "oops")


def test_conjugator_conjugate_invalid_tense(cg):
    with pytest.raises(InvalidTenseError):
        cg.conjugate_mood_tense("manger", "indicatif", "oops")


def test_conjugator_find_template_template_not_found(cg):
    with pytest.raises(TemplateNotFoundError):
        cg.find_template("oops")


@pytest.mark.parametrize(
    "query,expected_resp",
    [
        ("lev", ["lever", "léviger", "levretter"]),
        ("Se lev", ["se lever", "se léviger", "se levretter"]),
        ("s'aim", ["s'aimanter", "s'aimer"]),
    ],
)
def test_conjugator_get_verbs_that_start_with(cg, query, expected_resp):
    assert set(cg.get_verbs_that_start_with(query, max_results=10)) == set(
        expected_resp
    )
