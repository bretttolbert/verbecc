import pytest
from typing import Generator

from verbecc.core.conjugator.complete_conjugator import CompleteConjugator
from verbecc.core.conjugator.mood_conjugator import MoodConjugator
from verbecc.core.conjugator.tense_conjugator import TenseConjugator
from verbecc.core.defs.types.exceptions import InvalidMoodError
from verbecc.core.defs.types.exceptions import InvalidTenseError
from verbecc.core.defs.types.exceptions import TemplateNotFoundError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.utils.config.verbecc_config_util import VerbeccConfigUtil
from verbecc.core.defs.types.tense import Tenses
from verbecc.core.defs.types.mood import Moods

config = VerbeccConfigUtil().load_config()


@pytest.fixture(scope="module")
def ccg() -> Generator[CompleteConjugator, None, None]:
    ccg = CompleteConjugator(lang=Lang.fr)
    yield ccg


@pytest.fixture(scope="module")
def mcg():
    mcg = MoodConjugator(lang=Lang.fr)
    yield mcg


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.fr)
    yield tcg


def test_get_infinitives(ccg: CompleteConjugator):
    infinitives = ccg.get_infinitives()
    assert len(infinitives) > 7000
    assert "parler" in infinitives


def test_get_template_names(ccg: CompleteConjugator):
    template_names = ccg.get_template_names()
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
def test_conjugate_basic(ccg: CompleteConjugator, infinitive: str):
    cc = ccg.conjugate(infinitive)
    assert cc


def test_conjugator_predict_conjugation_er_verb_indicative_present(ccg: CompleteConjugator):
    if config.ENABLE_ML_PREDICTION:
        tc = ccg.conjugate_mood_tense("ubériser", Moods.fr.Indicatif, Tenses.fr.Présent)
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


def test_conjugator_predict_conjugation_re_verb_indicative_present(ccg: CompleteConjugator):
    if config.ENABLE_ML_PREDICTION:
        tc = ccg.conjugate_mood_tense("brettre", Moods.fr.Indicatif, Tenses.fr.Présent)
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


def test_conjugate_passe_compose_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("manger", Moods.fr.Indicatif, Tenses.fr.PasséComposé)
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


def test_conjugate_passe_compose_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Indicatif, Tenses.fr.PasséComposé)
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


def test_conjugate_subjonctif_passe_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("manger", Moods.fr.Subjonctif, Tenses.fr.Passé)
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


def test_conjugate_subjonctif_passe_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Subjonctif, Tenses.fr.Passé)
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


def test_conjugate_conditionnel_passe_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("manger", Moods.fr.Conditionnel, Tenses.fr.Passé)
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


def test_conjugate_conditionnel_passe_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Conditionnel, Tenses.fr.Passé)
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


def test_conjugate_plusqueparfait_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "manger", Moods.fr.Indicatif, Tenses.fr.PlusQueParfait
    )
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


def test_conjugate_plusqueparfait_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Indicatif, Tenses.fr.PlusQueParfait)
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


def test_conjugate_subjonctif_plusqueparfait_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "manger", Moods.fr.Subjonctif, Tenses.fr.PlusQueParfait
    )
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


def test_conjugate_subjonctif_plusqueparfait_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "aller", Moods.fr.Subjonctif, Tenses.fr.PlusQueParfait
    )
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


def test_conjugate_futur_anterieur_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "manger", Moods.fr.Indicatif, Tenses.fr.FuturAntérieur
    )
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


def test_conjugate_futur_anterieur_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Indicatif, Tenses.fr.FuturAntérieur)
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


def test_conjugate_passe_anterieur_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "manger", Moods.fr.Indicatif, Tenses.fr.PasséAntérieur
    )
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


def test_conjugate_passe_anterieur_with_être(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Indicatif, Tenses.fr.PasséAntérieur)
    assert [c[0] for c in tc] == [
        "je fus allée",
        "je fus allé",
        "tu fus allée",
        "tu fus allé",
        "il fut allé",
        "elle fut allée",
        "on fut allée",
        "on fut allé",
        "nous fûmes allées",
        "nous fûmes allés",
        "vous fûtes allées",
        "vous fûtes allés",
        "ils furent allés",
        "elles furent allées",
    ]


def test_conjugate_imperatif_passe_with_avoir(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense(
        "manger", Moods.fr.Imperatif, Tenses.fr.ImperatifPassé
    )
    assert [c[0] for c in tc] == [
        "aie mangé",
        "ayons mangé",
        "ayez mangé",
    ]


def test_conjugate_imperatif_passe_with_etre(ccg: CompleteConjugator):
    tc = ccg.conjugate_mood_tense("aller", Moods.fr.Imperatif, Tenses.fr.ImperatifPassé)
    assert [c[0] for c in tc] == [
        "sois allée",
        "sois allé",
        "soyons allées",
        "soyons allés",
        "soyez allées",
        "soyez allés",
    ]


def test_conjugate_invalid_mood(ccg: CompleteConjugator):
    with pytest.raises(InvalidMoodError):
        ccg.conjugate_mood("manger", "oops")


def test_conjugate_invalid_tense(ccg: CompleteConjugator):
    with pytest.raises(InvalidTenseError):
        ccg.conjugate_mood_tense("manger", Moods.fr.Indicatif, "oops")


def test_conjugator_find_template_template_not_found(ccg: CompleteConjugator):
    with pytest.raises(TemplateNotFoundError):
        ccg.find_template("oops")


@pytest.mark.parametrize(
    "query,expected_value",
    [
        ("lev", ["lever", "léviger", "levretter"]),
        ("Se lev", ["se lever", "se léviger", "se levretter"]),
        ("s'aim", ["s'aimanter", "s'aimer"]),
    ],
)
def test_conjugator_get_verbs_that_start_with(
    ccg: CompleteConjugator, query: str, expected_value: list[str]
):
    assert set(ccg.get_verbs_that_start_with(query, max_results=10)) == set(
        expected_value
    )


def test_conjugator_construct():
    CompleteConjugator(lang=Lang.fr)
