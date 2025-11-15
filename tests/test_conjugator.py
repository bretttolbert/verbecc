import pytest
import json

from tests.common import assert_json_str_equal

from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.constants import config
from verbecc.src.defs.types.exceptions import InvalidMoodError
from verbecc.src.defs.types.exceptions import InvalidTenseError
from verbecc.src.defs.types.exceptions import TemplateNotFoundError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


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
            "elle ubérise",
            "on ubérise",
            "nous ubérisons",
            "vous ubérisez",
            "ils ubérisent",
            "elles ubérisent",
        ]


def test_conjugator_predict_conjugation_re_verb_indicative_present(cg):
    if config.ENABLE_ML_PREDICTION:
        tc = cg.conjugate_mood_tense("brettre", "indicatif", "présent")
        assert [c[0] for c in tc] == [
            "je brets",
            "tu brets",
            "il bret",
            "elle bret",
            "on bret",
            "nous brettons",
            "vous brettez",
            "ils brettent",
            "elles brettent",
        ]


def test_conjugator_conjugate_passe_compose_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "passé-composé")
    assert [c[0] for c in tc] == [
        "j'ai mangé",
        "tu as mangé",
        "il a mangé",
        "elle a mangé",
        "on a mangé",
        "nous avons mangé",
        "vous avez mangé",
        "ils ont mangé",
        "elles ont mangé",
    ]


def test_conjugator_conjugate_passe_compose_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "passé-composé")
    assert [c[0] for c in tc] == [
        "je suis allée",
        "je suis allé",
        "tu es allée",
        "tu es allé",
        "il est allé",
        "elle est allée",
        "on est allée",
        "on est allé",
        "nous sommes allées",
        "nous sommes allés",
        "vous êtes allées",
        "vous êtes allés",
        "ils sont allés",
        "elles sont allées",
    ]


def test_conjugator_conjugate_subjonctif_passe_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "subjonctif", "passé")
    assert [c[0] for c in tc] == [
        "que j'aie mangé",
        "que tu aies mangé",
        "qu'il ait mangé",
        "qu'elle ait mangé",
        "qu'on ait mangé",
        "que nous ayons mangé",
        "que vous ayez mangé",
        "qu'ils aient mangé",
        "qu'elles aient mangé",
    ]


def test_conjugator_conjugate_subjonctif_passe_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "subjonctif", "passé")
    assert [c[0] for c in tc] == [
        "que je sois allée",
        "que je sois allé",
        "que tu sois allée",
        "que tu sois allé",
        "qu'il soit allé",
        "qu'elle soit allée",
        "qu'on soit allée",
        "qu'on soit allé",
        "que nous soyons allées",
        "que nous soyons allés",
        "que vous soyez allées",
        "que vous soyez allés",
        "qu'ils soient allés",
        "qu'elles soient allées",
    ]


def test_conjugator_conjugate_conditionnel_passe_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "conditionnel", "passé")
    assert [c[0] for c in tc] == [
        "j'aurais mangé",
        "tu aurais mangé",
        "il aurait mangé",
        "elle aurait mangé",
        "on aurait mangé",
        "nous aurions mangé",
        "vous auriez mangé",
        "ils auraient mangé",
        "elles auraient mangé",
    ]


def test_conjugator_conjugate_conditionnel_passe_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "conditionnel", "passé")
    assert [c[0] for c in tc] == [
        "je serais allée",
        "je serais allé",
        "tu serais allée",
        "tu serais allé",
        "il serait allé",
        "elle serait allée",
        "on serait allée",
        "on serait allé",
        "nous serions allées",
        "nous serions allés",
        "vous seriez allées",
        "vous seriez allés",
        "ils seraient allés",
        "elles seraient allées",
    ]


def test_conjugator_conjugate_plusqueparfait_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "j'avais mangé",
        "tu avais mangé",
        "il avait mangé",
        "elle avait mangé",
        "on avait mangé",
        "nous avions mangé",
        "vous aviez mangé",
        "ils avaient mangé",
        "elles avaient mangé",
    ]


def test_conjugator_conjugate_plusqueparfait_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "j'étais allée",
        "j'étais allé",
        "tu étais allée",
        "tu étais allé",
        "il était allé",
        "elle était allée",
        "on était allée",
        "on était allé",
        "nous étions allées",
        "nous étions allés",
        "vous étiez allées",
        "vous étiez allés",
        "ils étaient allés",
        "elles étaient allées",
    ]


def test_conjugator_conjugate_subjonctif_plusqueparfait_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "subjonctif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "que j'eusse mangé",
        "que tu eusses mangé",
        "qu'il eût mangé",
        "qu'elle eût mangé",
        "qu'on eût mangé",
        "que nous eussions mangé",
        "que vous eussiez mangé",
        "qu'ils eussent mangé",
        "qu'elles eussent mangé",
    ]


def test_conjugator_conjugate_subjonctif_plusqueparfait_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "subjonctif", "plus-que-parfait")
    assert [c[0] for c in tc] == [
        "que je fusse allée",
        "que je fusse allé",
        "que tu fusses allée",
        "que tu fusses allé",
        "qu'il fût allé",
        "qu'elle fût allée",
        "qu'on fût allée",
        "qu'on fût allé",
        "que nous fussions allées",
        "que nous fussions allés",
        "que vous fussiez allées",
        "que vous fussiez allés",
        "qu'ils fussent allés",
        "qu'elles fussent allées",
    ]


def test_conjugator_conjugate_futur_anterieur_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "futur-antérieur")
    assert [c[0] for c in tc] == [
        "j'aurai mangé",
        "tu auras mangé",
        "il aura mangé",
        "elle aura mangé",
        "on aura mangé",
        "nous aurons mangé",
        "vous aurez mangé",
        "ils auront mangé",
        "elles auront mangé",
    ]


def test_conjugator_conjugate_futur_anterieur_with_etre(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "futur-antérieur")
    assert [c[0] for c in tc] == [
        "je serai allée",
        "je serai allé",
        "tu seras allée",
        "tu seras allé",
        "il sera allé",
        "elle sera allée",
        "on sera allée",
        "on sera allé",
        "nous serons allées",
        "nous serons allés",
        "vous serez allées",
        "vous serez allés",
        "ils seront allés",
        "elles seront allées",
    ]


def test_conjugator_conjugate_passe_anterieur_with_avoir(cg):
    tc = cg.conjugate_mood_tense("manger", "indicatif", "passé-antérieur")
    assert [c[0] for c in tc] == [
        "j'eus mangé",
        "tu eus mangé",
        "il eut mangé",
        "elle eut mangé",
        "on eut mangé",
        "nous eûmes mangé",
        "vous eûtes mangé",
        "ils eurent mangé",
        "elles eurent mangé",
    ]


def test_conjugator_conjugate_passe_anterieur_with_être(cg):
    tc = cg.conjugate_mood_tense("aller", "indicatif", "passé-antérieur")
    assert [c[0] for c in tc] == [
        "je fus allée",
        "je fus allé",
        "tu fus allée",
        "tu fus allé",
        "elle fut allée",
        "il fut allé",
        "on fut allée",
        "on fut allé",
        "nous fûmes allées",
        "nous fûmes allés",
        "vous fûtes allées",
        "vous fûtes allés",
        "elles furent allées",
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
        "sois allée",
        "sois allé",
        "soyons allées",
        "soyons allés",
        "soyez allées",
        "soyez allés",
    ]


expected_resp_conj_manger = {
    "moods": {
        "conditionnel": {
            "passé": [
                ["1", "s", None, "je", ["j'aurais mangé"]],
                ["2", "s", None, "tu", ["tu aurais mangé"]],
                ["3", "s", "m", "il", ["il aurait mangé"]],
                ["3", "s", "f", "elle", ["elle aurait mangé"]],
                ["3", "s", None, "on", ["on aurait mangé"]],
                ["1", "p", None, "nous", ["nous aurions mangé"]],
                ["2", "p", None, "vous", ["vous auriez mangé"]],
                ["3", "p", "m", "ils", ["ils auraient mangé"]],
                ["3", "p", "f", "elles", ["elles auraient mangé"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je mangerais"]],
                ["2", "s", None, "tu", ["tu mangerais"]],
                ["3", "s", "m", "il", ["il mangerait"]],
                ["3", "s", "f", "elle", ["elle mangerait"]],
                ["3", "s", None, "on", ["on mangerait"]],
                ["1", "p", None, "nous", ["nous mangerions"]],
                ["2", "p", None, "vous", ["vous mangeriez"]],
                ["3", "p", "m", "ils", ["ils mangeraient"]],
                ["3", "p", "f", "elles", ["elles mangeraient"]],
            ],
        },
        "imperatif": {
            "imperatif-passé": [
                ["2", "s", None, "tu", ["aie mangé"]],
                ["1", "p", None, "nous", ["ayons mangé"]],
                ["2", "p", None, "vous", ["ayez mangé"]],
            ],
            "imperatif-présent": [
                ["2", "s", None, "tu", ["mange"]],
                ["1", "p", None, "nous", ["mangeons"]],
                ["2", "p", None, "vous", ["mangez"]],
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", None, "je", ["j'aurai mangé"]],
                ["2", "s", None, "tu", ["tu auras mangé"]],
                ["3", "s", "m", "il", ["il aura mangé"]],
                ["3", "s", "f", "elle", ["elle aura mangé"]],
                ["3", "s", None, "on", ["on aura mangé"]],
                ["1", "p", None, "nous", ["nous aurons mangé"]],
                ["2", "p", None, "vous", ["vous aurez mangé"]],
                ["3", "p", "m", "ils", ["ils auront mangé"]],
                ["3", "p", "f", "elles", ["elles auront mangé"]],
            ],
            "futur-simple": [
                ["1", "s", None, "je", ["je mangerai"]],
                ["2", "s", None, "tu", ["tu mangeras"]],
                ["3", "s", "m", "il", ["il mangera"]],
                ["3", "s", "f", "elle", ["elle mangera"]],
                ["3", "s", None, "on", ["on mangera"]],
                ["1", "p", None, "nous", ["nous mangerons"]],
                ["2", "p", None, "vous", ["vous mangerez"]],
                ["3", "p", "m", "ils", ["ils mangeront"]],
                ["3", "p", "f", "elles", ["elles mangeront"]],
            ],
            "imparfait": [
                ["1", "s", None, "je", ["je mangeais"]],
                ["2", "s", None, "tu", ["tu mangeais"]],
                ["3", "s", "m", "il", ["il mangeait"]],
                ["3", "s", "f", "elle", ["elle mangeait"]],
                ["3", "s", None, "on", ["on mangeait"]],
                ["1", "p", None, "nous", ["nous mangions"]],
                ["2", "p", None, "vous", ["vous mangiez"]],
                ["3", "p", "m", "ils", ["ils mangeaient"]],
                ["3", "p", "f", "elles", ["elles mangeaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", None, "je", ["j'eus mangé"]],
                ["2", "s", None, "tu", ["tu eus mangé"]],
                ["3", "s", "m", "il", ["il eut mangé"]],
                ["3", "s", "f", "elle", ["elle eut mangé"]],
                ["3", "s", None, "on", ["on eut mangé"]],
                ["1", "p", None, "nous", ["nous eûmes mangé"]],
                ["2", "p", None, "vous", ["vous eûtes mangé"]],
                ["3", "p", "m", "ils", ["ils eurent mangé"]],
                ["3", "p", "f", "elles", ["elles eurent mangé"]],
            ],
            "passé-composé": [
                ["1", "s", None, "je", ["j'ai mangé"]],
                ["2", "s", None, "tu", ["tu as mangé"]],
                ["3", "s", "m", "il", ["il a mangé"]],
                ["3", "s", "f", "elle", ["elle a mangé"]],
                ["3", "s", None, "on", ["on a mangé"]],
                ["1", "p", None, "nous", ["nous avons mangé"]],
                ["2", "p", None, "vous", ["vous avez mangé"]],
                ["3", "p", "m", "ils", ["ils ont mangé"]],
                ["3", "p", "f", "elles", ["elles ont mangé"]],
            ],
            "passé-simple": [
                ["1", "s", None, "je", ["je mangeai"]],
                ["2", "s", None, "tu", ["tu mangeas"]],
                ["3", "s", "m", "il", ["il mangea"]],
                ["3", "s", "f", "elle", ["elle mangea"]],
                ["3", "s", None, "on", ["on mangea"]],
                ["1", "p", None, "nous", ["nous mangeâmes"]],
                ["2", "p", None, "vous", ["vous mangeâtes"]],
                ["3", "p", "m", "ils", ["ils mangèrent"]],
                ["3", "p", "f", "elles", ["elles mangèrent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", None, "je", ["j'avais mangé"]],
                ["2", "s", None, "tu", ["tu avais mangé"]],
                ["3", "s", "m", "il", ["il avait mangé"]],
                ["3", "s", "f", "elle", ["elle avait mangé"]],
                ["3", "s", None, "on", ["on avait mangé"]],
                ["1", "p", None, "nous", ["nous avions mangé"]],
                ["2", "p", None, "vous", ["vous aviez mangé"]],
                ["3", "p", "m", "ils", ["ils avaient mangé"]],
                ["3", "p", "f", "elles", ["elles avaient mangé"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je mange"]],
                ["2", "s", None, "tu", ["tu manges"]],
                ["3", "s", "m", "il", ["il mange"]],
                ["3", "s", "f", "elle", ["elle mange"]],
                ["3", "s", None, "on", ["on mange"]],
                ["1", "p", None, "nous", ["nous mangeons"]],
                ["2", "p", None, "vous", ["vous mangez"]],
                ["3", "p", "m", "ils", ["ils mangent"]],
                ["3", "p", "f", "elles", ["elles mangent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", None, "je", ["manger"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", None, ["mangé"]],
                [None, "p", "m", None, ["mangés"]],
                [None, "s", "f", None, ["mangée"]],
                [None, "p", "f", None, ["mangées"]],
            ],
            "participe-présent": [[None, "s", "m", None, ["mangeant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", None, "je", ["que je mangeasse"]],
                ["2", "s", None, "tu", ["que tu mangeasses"]],
                ["3", "s", "m", "il", ["qu'il mangeât"]],
                ["3", "s", "f", "elle", ["qu'elle mangeât"]],
                ["3", "s", None, "on", ["qu'on mangeât"]],
                ["1", "p", None, "nous", ["que nous mangeassions"]],
                ["2", "p", None, "vous", ["que vous mangeassiez"]],
                ["3", "p", "m", "ils", ["qu'ils mangeassent"]],
                ["3", "p", "f", "elles", ["qu'elles mangeassent"]],
            ],
            "passé": [
                ["1", "s", None, "je", ["que j'aie mangé"]],
                ["2", "s", None, "tu", ["que tu aies mangé"]],
                ["3", "s", "m", "il", ["qu'il ait mangé"]],
                ["3", "s", "f", "elle", ["qu'elle ait mangé"]],
                ["3", "s", None, "on", ["qu'on ait mangé"]],
                ["1", "p", None, "nous", ["que nous ayons mangé"]],
                ["2", "p", None, "vous", ["que vous ayez mangé"]],
                ["3", "p", "m", "ils", ["qu'ils aient mangé"]],
                ["3", "p", "f", "elles", ["qu'elles aient mangé"]],
            ],
            "plus-que-parfait": [
                ["1", "s", None, "je", ["que j'eusse mangé"]],
                ["2", "s", None, "tu", ["que tu eusses mangé"]],
                ["3", "s", "m", "il", ["qu'il eût mangé"]],
                ["3", "s", "f", "elle", ["qu'elle eût mangé"]],
                ["3", "s", None, "on", ["qu'on eût mangé"]],
                ["1", "p", None, "nous", ["que nous eussions mangé"]],
                ["2", "p", None, "vous", ["que vous eussiez mangé"]],
                ["3", "p", "m", "ils", ["qu'ils eussent mangé"]],
                ["3", "p", "f", "elles", ["qu'elles eussent mangé"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["que je mange"]],
                ["2", "s", None, "tu", ["que tu manges"]],
                ["3", "s", "m", "il", ["qu'il mange"]],
                ["3", "s", "f", "elle", ["qu'elle mange"]],
                ["3", "s", None, "on", ["qu'on mange"]],
                ["1", "p", None, "nous", ["que nous mangions"]],
                ["2", "p", None, "vous", ["que vous mangiez"]],
                ["3", "p", "m", "ils", ["qu'ils mangent"]],
                ["3", "p", "f", "elles", ["qu'elles mangent"]],
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
                ["1", "s", None, "je", ["j'aurais pu"]],
                ["2", "s", None, "tu", ["tu aurais pu"]],
                ["3", "s", "m", "il", ["il aurait pu"]],
                ["3", "s", "f", "elle", ["elle aurait pu"]],
                ["3", "s", None, "on", ["on aurait pu"]],
                ["1", "p", None, "nous", ["nous aurions pu"]],
                ["2", "p", None, "vous", ["vous auriez pu"]],
                ["3", "p", "m", "ils", ["ils auraient pu"]],
                ["3", "p", "f", "elles", ["elles auraient pu"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je pourrais"]],
                ["2", "s", None, "tu", ["tu pourrais"]],
                ["3", "s", "m", "il", ["il pourrait"]],
                ["3", "s", "f", "elle", ["elle pourrait"]],
                ["3", "s", None, "on", ["on pourrait"]],
                ["1", "p", None, "nous", ["nous pourrions"]],
                ["2", "p", None, "vous", ["vous pourriez"]],
                ["3", "p", "m", "ils", ["ils pourraient"]],
                ["3", "p", "f", "elles", ["elles pourraient"]],
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", None, "je", ["j'aurai pu"]],
                ["2", "s", None, "tu", ["tu auras pu"]],
                ["3", "s", "m", "il", ["il aura pu"]],
                ["3", "s", "f", "elle", ["elle aura pu"]],
                ["3", "s", None, "on", ["on aura pu"]],
                ["1", "p", None, "nous", ["nous aurons pu"]],
                ["2", "p", None, "vous", ["vous aurez pu"]],
                ["3", "p", "m", "ils", ["ils auront pu"]],
                ["3", "p", "f", "elles", ["elles auront pu"]],
            ],
            "futur-simple": [
                ["1", "s", None, "je", ["je pourrai"]],
                ["2", "s", None, "tu", ["tu pourras"]],
                ["3", "s", "m", "il", ["il pourra"]],
                ["3", "s", "f", "elle", ["elle pourra"]],
                ["3", "s", None, "on", ["on pourra"]],
                ["1", "p", None, "nous", ["nous pourrons"]],
                ["2", "p", None, "vous", ["vous pourrez"]],
                ["3", "p", "m", "ils", ["ils pourront"]],
                ["3", "p", "f", "elles", ["elles pourront"]],
            ],
            "imparfait": [
                ["1", "s", None, "je", ["je pouvais"]],
                ["2", "s", None, "tu", ["tu pouvais"]],
                ["3", "s", "m", "il", ["il pouvait"]],
                ["3", "s", "f", "elle", ["elle pouvait"]],
                ["3", "s", None, "on", ["on pouvait"]],
                ["1", "p", None, "nous", ["nous pouvions"]],
                ["2", "p", None, "vous", ["vous pouviez"]],
                ["3", "p", "m", "ils", ["ils pouvaient"]],
                ["3", "p", "f", "elles", ["elles pouvaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", None, "je", ["j'eus pu"]],
                ["2", "s", None, "tu", ["tu eus pu"]],
                ["3", "s", "m", "il", ["il eut pu"]],
                ["3", "s", "f", "elle", ["elle eut pu"]],
                ["3", "s", None, "on", ["on eut pu"]],
                ["1", "p", None, "nous", ["nous eûmes pu"]],
                ["2", "p", None, "vous", ["vous eûtes pu"]],
                ["3", "p", "m", "ils", ["ils eurent pu"]],
                ["3", "p", "f", "elles", ["elles eurent pu"]],
            ],
            "passé-composé": [
                ["1", "s", None, "je", ["j'ai pu"]],
                ["2", "s", None, "tu", ["tu as pu"]],
                ["3", "s", "m", "il", ["il a pu"]],
                ["3", "s", "f", "elle", ["elle a pu"]],
                ["3", "s", None, "on", ["on a pu"]],
                ["1", "p", None, "nous", ["nous avons pu"]],
                ["2", "p", None, "vous", ["vous avez pu"]],
                ["3", "p", "m", "ils", ["ils ont pu"]],
                ["3", "p", "f", "elles", ["elles ont pu"]],
            ],
            "passé-simple": [
                ["1", "s", None, "je", ["je pus"]],
                ["2", "s", None, "tu", ["tu pus"]],
                ["3", "s", "m", "il", ["il put"]],
                ["3", "s", "f", "elle", ["elle put"]],
                ["3", "s", None, "on", ["on put"]],
                ["1", "p", None, "nous", ["nous pûmes"]],
                ["2", "p", None, "vous", ["vous pûtes"]],
                ["3", "p", "m", "ils", ["ils purent"]],
                ["3", "p", "f", "elles", ["elles purent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", None, "je", ["j'avais pu"]],
                ["2", "s", None, "tu", ["tu avais pu"]],
                ["3", "s", "m", "il", ["il avait pu"]],
                ["3", "s", "f", "elle", ["elle avait pu"]],
                ["3", "s", None, "on", ["on avait pu"]],
                ["1", "p", None, "nous", ["nous avions pu"]],
                ["2", "p", None, "vous", ["vous aviez pu"]],
                ["3", "p", "m", "ils", ["ils avaient pu"]],
                ["3", "p", "f", "elles", ["elles avaient pu"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je peux", "je puis"]],
                ["2", "s", None, "tu", ["tu peux"]],
                ["3", "s", "m", "il", ["il peut"]],
                ["3", "s", "f", "elle", ["elle peut"]],
                ["3", "s", None, "on", ["on peut"]],
                ["1", "p", None, "nous", ["nous pouvons"]],
                ["2", "p", None, "vous", ["vous pouvez"]],
                ["3", "p", "m", "ils", ["ils peuvent"]],
                ["3", "p", "f", "elles", ["elles peuvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", None, "je", ["pouvoir"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", None, ["pu"]],
                [None, "p", "m", None, ["pus"]],
                [None, "s", "f", None, ["pue"]],
                [None, "p", "f", None, ["pues"]],
            ],
            "participe-présent": [[None, "s", "m", None, ["pouvant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", None, "je", ["que je pusse"]],
                ["2", "s", None, "tu", ["que tu pusses"]],
                ["3", "s", "m", "il", ["qu'il pût"]],
                ["3", "s", "f", "elle", ["qu'elle pût"]],
                ["3", "s", None, "on", ["qu'on pût"]],
                ["1", "p", None, "nous", ["que nous pussions"]],
                ["2", "p", None, "vous", ["que vous pussiez"]],
                ["3", "p", "m", "ils", ["qu'ils pussent"]],
                ["3", "p", "f", "elles", ["qu'elles pussent"]],
            ],
            "passé": [
                ["1", "s", None, "je", ["que j'aie pu"]],
                ["2", "s", None, "tu", ["que tu aies pu"]],
                ["3", "s", "m", "il", ["qu'il ait pu"]],
                ["3", "s", "f", "elle", ["qu'elle ait pu"]],
                ["3", "s", None, "on", ["qu'on ait pu"]],
                ["1", "p", None, "nous", ["que nous ayons pu"]],
                ["2", "p", None, "vous", ["que vous ayez pu"]],
                ["3", "p", "m", "ils", ["qu'ils aient pu"]],
                ["3", "p", "f", "elles", ["qu'elles aient pu"]],
            ],
            "plus-que-parfait": [
                ["1", "s", None, "je", ["que j'eusse pu"]],
                ["2", "s", None, "tu", ["que tu eusses pu"]],
                ["3", "s", "m", "il", ["qu'il eût pu"]],
                ["3", "s", "f", "elle", ["qu'elle eût pu"]],
                ["3", "s", None, "on", ["qu'on eût pu"]],
                ["1", "p", None, "nous", ["que nous eussions pu"]],
                ["2", "p", None, "vous", ["que vous eussiez pu"]],
                ["3", "p", "m", "ils", ["qu'ils eussent pu"]],
                ["3", "p", "f", "elles", ["qu'elles eussent pu"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["que je puisse"]],
                ["2", "s", None, "tu", ["que tu puisses"]],
                ["3", "s", "m", "il", ["qu'il puisse"]],
                ["3", "s", "f", "elle", ["qu'elle puisse"]],
                ["3", "s", None, "on", ["qu'on puisse"]],
                ["1", "p", None, "nous", ["que nous puissions"]],
                ["2", "p", None, "vous", ["que vous puissiez"]],
                ["3", "p", "m", "ils", ["qu'ils puissent"]],
                ["3", "p", "f", "elles", ["qu'elles puissent"]],
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
                ["3", "s", "f", "elle", ["elle aurait plu"]],
                ["3", "s", None, "on", ["on aurait plu"]],
                ["3", "p", "m", "ils", ["ils auraient plu"]],
                ["3", "p", "f", "elles", ["elles auraient plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["il pleuvrait"]],
                ["3", "s", "f", "elle", ["elle pleuvrait"]],
                ["3", "s", None, "on", ["on pleuvrait"]],
                ["3", "p", "m", "ils", ["ils pleuvraient"]],
                ["3", "p", "f", "elles", ["elles pleuvraient"]],
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                ["3", "s", "m", "il", ["il aura plu"]],
                ["3", "s", "f", "elle", ["elle aura plu"]],
                ["3", "s", None, "on", ["on aura plu"]],
                ["3", "p", "m", "ils", ["ils auront plu"]],
                ["3", "p", "f", "elles", ["elles auront plu"]],
            ],
            "futur-simple": [
                ["3", "s", "m", "il", ["il pleuvra"]],
                ["3", "s", "f", "elle", ["elle pleuvra"]],
                ["3", "s", None, "on", ["on pleuvra"]],
                ["3", "p", "m", "ils", ["ils pleuvront"]],
                ["3", "p", "f", "elles", ["elles pleuvront"]],
            ],
            "imparfait": [
                ["3", "s", "m", "il", ["il pleuvait"]],
                ["3", "s", "f", "elle", ["elle pleuvait"]],
                ["3", "s", None, "on", ["on pleuvait"]],
                ["3", "p", "m", "ils", ["ils pleuvaient"]],
                ["3", "p", "f", "elles", ["elles pleuvaient"]],
            ],
            "passé-antérieur": [
                ["3", "s", "m", "il", ["il eut plu"]],
                ["3", "s", "f", "elle", ["elle eut plu"]],
                ["3", "s", None, "on", ["on eut plu"]],
                ["3", "p", "m", "ils", ["ils eurent plu"]],
                ["3", "p", "f", "elles", ["elles eurent plu"]],
            ],
            "passé-composé": [
                ["3", "s", "m", "il", ["il a plu"]],
                ["3", "s", "f", "elle", ["elle a plu"]],
                ["3", "s", None, "on", ["on a plu"]],
                ["3", "p", "m", "ils", ["ils ont plu"]],
                ["3", "p", "f", "elles", ["elles ont plu"]],
            ],
            "passé-simple": [
                ["3", "s", "m", "il", ["il plut"]],
                ["3", "s", "f", "elle", ["elle plut"]],
                ["3", "s", None, "on", ["on plut"]],
                ["3", "p", "m", "ils", ["ils plurent"]],
                ["3", "p", "f", "elles", ["elles plurent"]],
            ],
            "plus-que-parfait": [
                ["3", "s", "m", "il", ["il avait plu"]],
                ["3", "s", "f", "elle", ["elle avait plu"]],
                ["3", "s", None, "on", ["on avait plu"]],
                ["3", "p", "m", "ils", ["ils avaient plu"]],
                ["3", "p", "f", "elles", ["elles avaient plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["il pleut"]],
                ["3", "s", "f", "elle", ["elle pleut"]],
                ["3", "s", None, "on", ["on pleut"]],
                ["3", "p", "m", "ils", ["ils pleuvent"]],
                ["3", "p", "f", "elles", ["elles pleuvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", None, "je", ["pleuvoir"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", None, ["plu"]],
                [None, "p", "m", None, ["plus"]],
                [None, "s", "f", None, ["plue"]],
                [None, "p", "f", None, ["plues"]],
            ],
            "participe-présent": [[None, "s", "m", None, ["pleuvant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["3", "s", "m", "il", ["qu'il plût"]],
                ["3", "s", "f", "elle", ["qu'elle plût"]],
                ["3", "s", None, "on", ["qu'on plût"]],
                ["3", "p", "m", "ils", ["qu'ils plussent"]],
                ["3", "p", "f", "elles", ["qu'elles plussent"]],
            ],
            "passé": [
                ["3", "s", "m", "il", ["qu'il ait plu"]],
                ["3", "s", "f", "elle", ["qu'elle ait plu"]],
                ["3", "s", None, "on", ["qu'on ait plu"]],
                ["3", "p", "m", "ils", ["qu'ils aient plu"]],
                ["3", "p", "f", "elles", ["qu'elles aient plu"]],
            ],
            "plus-que-parfait": [
                ["3", "s", "m", "il", ["qu'il eût plu"]],
                ["3", "s", "f", "elle", ["qu'elle eût plu"]],
                ["3", "s", None, "on", ["qu'on eût plu"]],
                ["3", "p", "m", "ils", ["qu'ils eussent plu"]],
                ["3", "p", "f", "elles", ["qu'elles eussent plu"]],
            ],
            "présent": [
                ["3", "s", "m", "il", ["qu'il pleuve"]],
                ["3", "s", "f", "elle", ["qu'elle pleuve"]],
                ["3", "s", None, "on", ["qu'on pleuve"]],
                ["3", "p", "m", "ils", ["qu'ils pleuvent"]],
                ["3", "p", "f", "elles", ["qu'elles pleuvent"]],
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
                ["1", "s", "f", "je", ["je me serais levée"]],
                ["1", "s", "m", "je", ["je me serais levé"]],
                ["2", "s", "f", "tu", ["tu te serais levée"]],
                ["2", "s", "m", "tu", ["tu te serais levé"]],
                ["3", "s", "m", "il", ["il se serait levé"]],
                ["3", "s", "f", "elle", ["elle se serait levée"]],
                ["3", "s", "f", "on", ["on se serait levée"]],
                ["3", "s", "m", "on", ["on se serait levé"]],
                ["1", "p", "f", "nous", ["nous nous serions levées"]],
                ["1", "p", "m", "nous", ["nous nous serions levés"]],
                ["2", "p", "f", "vous", ["vous vous seriez levées"]],
                ["2", "p", "m", "vous", ["vous vous seriez levés"]],
                ["3", "p", "m", "ils", ["ils se seraient levés"]],
                ["3", "p", "f", "elles", ["elles se seraient levées"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je me lèverais"]],
                ["2", "s", None, "tu", ["tu te lèverais"]],
                ["3", "s", "m", "il", ["il se lèverait"]],
                ["3", "s", "f", "elle", ["elle se lèverait"]],
                ["3", "s", None, "on", ["on se lèverait"]],
                ["1", "p", None, "nous", ["nous nous lèverions"]],
                ["2", "p", None, "vous", ["vous vous lèveriez"]],
                ["3", "p", "m", "ils", ["ils se lèveraient"]],
                ["3", "p", "f", "elles", ["elles se lèveraient"]],
            ],
        },
        "imperatif": {
            "imperatif-passé": [],
            "imperatif-présent": [
                ["2", "s", None, "tu", ["lève-toi"]],
                ["1", "p", None, "nous", ["levons-nous"]],
                ["2", "p", None, "vous", ["levez-vous"]],
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                ["1", "s", "f", "je", ["je me serai levée"]],
                ["1", "s", "m", "je", ["je me serai levé"]],
                ["2", "s", "f", "tu", ["tu te seras levée"]],
                ["2", "s", "m", "tu", ["tu te seras levé"]],
                ["3", "s", "m", "il", ["il se sera levé"]],
                ["3", "s", "f", "elle", ["elle se sera levée"]],
                ["3", "s", "f", "on", ["on se sera levée"]],
                ["3", "s", "m", "on", ["on se sera levé"]],
                ["1", "p", "f", "nous", ["nous nous serons levées"]],
                ["1", "p", "m", "nous", ["nous nous serons levés"]],
                ["2", "p", "f", "vous", ["vous vous serez levées"]],
                ["2", "p", "m", "vous", ["vous vous serez levés"]],
                ["3", "p", "m", "ils", ["ils se seront levés"]],
                ["3", "p", "f", "elles", ["elles se seront levées"]],
            ],
            "futur-simple": [
                ["1", "s", None, "je", ["je me lèverai"]],
                ["2", "s", None, "tu", ["tu te lèveras"]],
                ["3", "s", "m", "il", ["il se lèvera"]],
                ["3", "s", "f", "elle", ["elle se lèvera"]],
                ["3", "s", None, "on", ["on se lèvera"]],
                ["1", "p", None, "nous", ["nous nous lèverons"]],
                ["2", "p", None, "vous", ["vous vous lèverez"]],
                ["3", "p", "m", "ils", ["ils se lèveront"]],
                ["3", "p", "f", "elles", ["elles se lèveront"]],
            ],
            "imparfait": [
                ["1", "s", None, "je", ["je me levais"]],
                ["2", "s", None, "tu", ["tu te levais"]],
                ["3", "s", "m", "il", ["il se levait"]],
                ["3", "s", "f", "elle", ["elle se levait"]],
                ["3", "s", None, "on", ["on se levait"]],
                ["1", "p", None, "nous", ["nous nous levions"]],
                ["2", "p", None, "vous", ["vous vous leviez"]],
                ["3", "p", "m", "ils", ["ils se levaient"]],
                ["3", "p", "f", "elles", ["elles se levaient"]],
            ],
            "passé-antérieur": [
                ["1", "s", "f", "je", ["je me fus levée"]],
                ["1", "s", "m", "je", ["je me fus levé"]],
                ["2", "s", "f", "tu", ["tu te fus levée"]],
                ["2", "s", "m", "tu", ["tu te fus levé"]],
                ["3", "s", "m", "il", ["il se fut levé"]],
                ["3", "s", "f", "elle", ["elle se fut levée"]],
                ["3", "s", "f", "on", ["on se fut levée"]],
                ["3", "s", "m", "on", ["on se fut levé"]],
                ["1", "p", "f", "nous", ["nous nous fûmes levées"]],
                ["1", "p", "m", "nous", ["nous nous fûmes levés"]],
                ["2", "p", "f", "vous", ["vous vous fûtes levées"]],
                ["2", "p", "m", "vous", ["vous vous fûtes levés"]],
                ["3", "p", "m", "ils", ["ils se furent levés"]],
                ["3", "p", "f", "elles", ["elles se furent levées"]],
            ],
            "passé-composé": [
                ["1", "s", "f", "je", ["je me suis levée"]],
                ["1", "s", "m", "je", ["je me suis levé"]],
                ["2", "s", "f", "tu", ["tu te es levée"]],
                ["2", "s", "m", "tu", ["tu te es levé"]],
                ["3", "s", "m", "il", ["il se est levé"]],
                ["3", "s", "f", "elle", ["elle se est levée"]],
                ["3", "s", "f", "on", ["on se est levée"]],
                ["3", "s", "m", "on", ["on se est levé"]],
                ["1", "p", "f", "nous", ["nous nous sommes levées"]],
                ["1", "p", "m", "nous", ["nous nous sommes levés"]],
                ["2", "p", "f", "vous", ["vous vous êtes levées"]],
                ["2", "p", "m", "vous", ["vous vous êtes levés"]],
                ["3", "p", "m", "ils", ["ils se sont levés"]],
                ["3", "p", "f", "elles", ["elles se sont levées"]],
            ],
            "passé-simple": [
                ["1", "s", None, "je", ["je me levai"]],
                ["2", "s", None, "tu", ["tu te levas"]],
                ["3", "s", "m", "il", ["il se leva"]],
                ["3", "s", "f", "elle", ["elle se leva"]],
                ["3", "s", None, "on", ["on se leva"]],
                ["1", "p", None, "nous", ["nous nous levâmes"]],
                ["2", "p", None, "vous", ["vous vous levâtes"]],
                ["3", "p", "m", "ils", ["ils se levèrent"]],
                ["3", "p", "f", "elles", ["elles se levèrent"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "f", "je", ["je me étais levée"]],
                ["1", "s", "m", "je", ["je me étais levé"]],
                ["2", "s", "f", "tu", ["tu te étais levée"]],
                ["2", "s", "m", "tu", ["tu te étais levé"]],
                ["3", "s", "m", "il", ["il se était levé"]],
                ["3", "s", "f", "elle", ["elle se était levée"]],
                ["3", "s", "f", "on", ["on se était levée"]],
                ["3", "s", "m", "on", ["on se était levé"]],
                ["1", "p", "f", "nous", ["nous nous étions levées"]],
                ["1", "p", "m", "nous", ["nous nous étions levés"]],
                ["2", "p", "f", "vous", ["vous vous étiez levées"]],
                ["2", "p", "m", "vous", ["vous vous étiez levés"]],
                ["3", "p", "m", "ils", ["ils se étaient levés"]],
                ["3", "p", "f", "elles", ["elles se étaient levées"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["je me lève"]],
                ["2", "s", None, "tu", ["tu te lèves"]],
                ["3", "s", "m", "il", ["il se lève"]],
                ["3", "s", "f", "elle", ["elle se lève"]],
                ["3", "s", None, "on", ["on se lève"]],
                ["1", "p", None, "nous", ["nous nous levons"]],
                ["2", "p", None, "vous", ["vous vous levez"]],
                ["3", "p", "m", "ils", ["ils se lèvent"]],
                ["3", "p", "f", "elles", ["elles se lèvent"]],
            ],
        },
        "infinitif": {"infinitif-présent": [["1", "s", None, "je", ["se lever"]]]},
        "participe": {
            "participe-passé": [
                [None, "s", "m", None, ["étant levé"]],
                [None, "p", "m", None, ["étant levés"]],
                [None, "s", "f", None, ["étant levée"]],
                [None, "p", "f", None, ["étant levées"]],
            ],
            "participe-présent": [[None, "s", "m", None, ["levant"]]],
        },
        "subjonctif": {
            "imparfait": [
                ["1", "s", None, "je", ["que je me levasse"]],
                ["2", "s", None, "tu", ["que tu te levasses"]],
                ["3", "s", "m", "il", ["qu'il se levât"]],
                ["3", "s", "f", "elle", ["qu'elle se levât"]],
                ["3", "s", None, "on", ["qu'on se levât"]],
                ["1", "p", None, "nous", ["que nous nous levassions"]],
                ["2", "p", None, "vous", ["que vous vous levassiez"]],
                ["3", "p", "m", "ils", ["qu'ils se levassent"]],
                ["3", "p", "f", "elles", ["qu'elles se levassent"]],
            ],
            "passé": [
                ["1", "s", "f", "je", ["que je me sois levée"]],
                ["1", "s", "m", "je", ["que je me sois levé"]],
                ["2", "s", "f", "tu", ["que tu te sois levée"]],
                ["2", "s", "m", "tu", ["que tu te sois levé"]],
                ["3", "s", "m", "il", ["qu'il se soit levé"]],
                ["3", "s", "f", "elle", ["qu'elle se soit levée"]],
                ["3", "s", "f", "on", ["qu'on se soit levée"]],
                ["3", "s", "m", "on", ["qu'on se soit levé"]],
                ["1", "p", "f", "nous", ["que nous nous soyons levées"]],
                ["1", "p", "m", "nous", ["que nous nous soyons levés"]],
                ["2", "p", "f", "vous", ["que vous vous soyez levées"]],
                ["2", "p", "m", "vous", ["que vous vous soyez levés"]],
                ["3", "p", "m", "ils", ["qu'ils se soient levés"]],
                ["3", "p", "f", "elles", ["qu'elles se soient levées"]],
            ],
            "plus-que-parfait": [
                ["1", "s", "f", "je", ["que je me fusse levée"]],
                ["1", "s", "m", "je", ["que je me fusse levé"]],
                ["2", "s", "f", "tu", ["que tu te fusses levée"]],
                ["2", "s", "m", "tu", ["que tu te fusses levé"]],
                ["3", "s", "m", "il", ["qu'il se fût levé"]],
                ["3", "s", "f", "elle", ["qu'elle se fût levée"]],
                ["3", "s", "f", "on", ["qu'on se fût levée"]],
                ["3", "s", "m", "on", ["qu'on se fût levé"]],
                ["1", "p", "f", "nous", ["que nous nous fussions levées"]],
                ["1", "p", "m", "nous", ["que nous nous fussions levés"]],
                ["2", "p", "f", "vous", ["que vous vous fussiez levées"]],
                ["2", "p", "m", "vous", ["que vous vous fussiez levés"]],
                ["3", "p", "m", "ils", ["qu'ils se fussent levés"]],
                ["3", "p", "f", "elles", ["qu'elles se fussent levées"]],
            ],
            "présent": [
                ["1", "s", None, "je", ["que je me lève"]],
                ["2", "s", None, "tu", ["que tu te lèves"]],
                ["3", "s", "m", "il", ["qu'il se lève"]],
                ["3", "s", "f", "elle", ["qu'elle se lève"]],
                ["3", "s", None, "on", ["qu'on se lève"]],
                ["1", "p", None, "nous", ["que nous nous levions"]],
                ["2", "p", None, "vous", ["que vous vous leviez"]],
                ["3", "p", "m", "ils", ["qu'ils se lèvent"]],
                ["3", "p", "f", "elles", ["qu'elles se lèvent"]],
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
