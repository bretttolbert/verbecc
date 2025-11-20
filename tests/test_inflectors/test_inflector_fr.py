import pytest
from lxml import etree

from verbecc.src.conjugator.complete_conjugator import CompleteConjugator
from verbecc.src.conjugator.mood_conjugator import MoodConjugator
from verbecc.src.conjugator.tense_conjugator import TenseConjugator
from verbecc.src.defs.types.conjugation import Conjugation
from verbecc.src.defs.types.conjugation import TenseConjugation
from verbecc.src.defs.types.exceptions import ConjugatorError
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tenses
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser
from verbecc.src.defs.types.pronoun import Pronoun, Pronouns


@pytest.fixture(scope="module")
def ccg():
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


def test_all_verbs_have_templates(ccg):
    verbs = ccg.get_verbs()
    template_names = ccg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


def test_add_subjunctive_relative_prounoun(ccg):
    assert (
        ccg._inflector.add_subjunctive_relative_pronoun("tu manges", "")
        == "que tu manges"
    )
    assert (
        ccg._inflector.add_subjunctive_relative_pronoun("il mange", "") == "qu'il mange"
    )
    assert (
        ccg._inflector.add_subjunctive_relative_pronoun("elles mangent", "")
        == "qu'elles mangent"
    )


def testadd_reflexive_pronoun(ccg):
    assert ccg._inflector.add_reflexive_pronoun("lever") == "se lever"
    assert ccg._inflector.add_reflexive_pronoun("écrouler") == "s'écrouler"


def testsplit_reflexive(ccg):
    assert ccg._inflector.split_reflexive("se lever") == (True, "lever")
    assert ccg._inflector.split_reflexive("s'écrouler") == (True, "écrouler")
    assert ccg._inflector.split_reflexive("secouer") == (False, "secouer")


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        ("être", False),
        ("lever", True),
        ("pleuvoir", False),
        ("manger", True),
    ],
)
def test_inflector_fr_verb_can_be_reflexive(ccg, infinitive, expected_result):
    assert ccg._inflector.verb_can_be_reflexive(infinitive) == expected_result


def test_inflector_fr_impersonal_verbs(ccg):
    impersonal_verbs = [
        v.infinitive
        for v in ccg._inflector._verbs
        if ccg._inflector._is_impersonal_verb(v.infinitive)
    ]
    assert set(impersonal_verbs) == set(
        [
            "advenir",
            "apparoir",
            "bruiner",
            "bruire",
            "chaloir",
            "clore",
            "déclore",
            "échoir",
            "éclore",
            "enclore",
            "falloir",
            "forclore",
            "frire",
            "grêler",
            "messeoir",
            "neiger",
            "pleuvoir",
            "seoir",
            "sourdre",
        ]
    )


def test_inflector_fr_conjugate_simple_mood_tense(tcg):
    infinitive = "manger"
    mood = Moods.fr.Indicatif
    tense = Tenses.fr.Présent
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == "man"
    tense_elem = etree.fromstring(
        """<présent>
        <p><i>ge</i></p>
        <p><i>ges</i></p>
        <p><i>ge</i></p>
        <p><i>geons</i></p>
        <p><i>gez</i></p>
        <p><i>gent</i></p>
        </présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem, mood, tense, tense_template
    )
    assert tc == TenseConjugation(
        tense,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.fr.je, ["je mange"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.fr.tu, ["tu manges"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.fr.il, ["il mange"]
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.fr.elle,
                ["elle mange"],
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.fr.on, ["on mange"]
            ),
            Conjugation(
                Person.First, Number.Plural, None, Pronouns.fr.nous, ["nous mangeons"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, Pronouns.fr.vous, ["vous mangez"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.fr.ils, ["ils mangent"]
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.fr.elles,
                ["elles mangent"],
            ),
        ],
    )


def test_inflector_fr_get_verb_stem_from_template_name(ccg):
    verb_stem = ccg._inflector.get_verb_stem_from_template_name("manger", "man:ger")
    assert verb_stem == "man"
    verb_stem = ccg._inflector.get_verb_stem_from_template_name("téléphoner", "aim:er")
    assert verb_stem == "téléphon"
    verb_stem = ccg._inflector.get_verb_stem_from_template_name("vendre", "ten:dre")
    assert verb_stem == "ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = ccg._inflector.get_verb_stem_from_template_name("aller", ":aller")
    assert verb_stem == ""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = ccg._inflector.get_verb_stem_from_template_name("vendre", "man:ger")


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, Pronouns.fr.je),
        (Person.First, Number.Singular, Gender.m, True, "je me"),
        (Person.Second, Number.Singular, Gender.m, False, Pronouns.fr.tu),
        (Person.Second, Number.Singular, Gender.m, True, "tu te"),
        (Person.Third, Number.Singular, Gender.m, False, Pronouns.fr.il),
        (Person.Third, Number.Singular, Gender.m, True, "il se"),
        (Person.Third, Number.Singular, Gender.f, False, Pronouns.fr.elle),
        (Person.Third, Number.Singular, Gender.f, True, "elle se"),
        (Person.First, Number.Plural, Gender.m, False, Pronouns.fr.nous),
        (Person.First, Number.Plural, Gender.m, True, "nous nous"),
        (Person.Second, Number.Plural, Gender.m, False, Pronouns.fr.vous),
        (Person.Second, Number.Plural, Gender.m, True, "vous vous"),
        (Person.Third, Number.Plural, Gender.m, False, Pronouns.fr.ils),
        (Person.Third, Number.Plural, Gender.m, True, "ils se"),
        (Person.Third, Number.Plural, Gender.f, False, Pronouns.fr.elles),
        (Person.Third, Number.Plural, Gender.f, True, "elles se"),
    ],
)
def test_inflector_fr_get_pronouns(
    ccg,
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    pronoun = ccg._inflector.get_pronouns(person, number, gender)[0]
    if is_reflexive:
        pronoun = ccg._inflector.make_pronoun_reflexive(pronoun)
    assert pronoun == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avoir",
            [
                "j'ai",
                "tu as",
                "il a",
                "elle a",
                "on a",
                "nous avons",
                "vous avez",
                "ils ont",
                "elles ont",
            ],
        ),
        (
            "habiter",
            [
                "j'habite",
                "tu habites",
                "il habite",
                "elle habite",
                "on habite",
                "nous habitons",
                "vous habitez",
                "ils habitent",
                "elles habitent",
            ],
        ),
        (
            "s'habiller",
            [
                "je m'habille",
                "tu t'habilles",
                "il s'habille",
                "elle s'habille",
                "on s'habille",
                "nous nous habillons",
                "vous vous habillez",
                "ils s'habillent",
                "elles s'habillent",
            ],
        ),
    ],
)
def test_pronoun_combined_vowel_h_non_aspiré(ccg, infinitive, expected_result):
    cc = ccg.conjugate(infinitive)
    moods_conj = cc.get_moods()
    mood_conj = moods_conj[Moods.fr.Indicatif]
    tense_conj = mood_conj[Tenses.fr.Présent]
    assert [c[0] for c in tense_conj] == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "habiter",
            [
                "que j'habite",
                "que tu habites",
                "qu'il habite",
                "qu'elle habite",
                "qu'on habite",
                "que nous habitions",
                "que vous habitiez",
                "qu'ils habitent",
                "qu'elles habitent",
            ],
        )
    ],
)
def test_subjonctif_vowel_h_non_aspiré(ccg, infinitive, expected_result):
    cc = ccg.conjugate(infinitive)
    moods_conj = cc.get_moods()
    mood_conj = moods_conj[Moods.fr.Subjonctif]
    tense_conj = mood_conj[Tenses.fr.Présent]
    assert [c[0] for c in tense_conj] == expected_result


def test_fr_get_str_id(ccg):
    cc = ccg.conjugate("parler")
    assert cc.get_str_id() == "fr:parler"
    mc = cc[Moods.fr.Indicatif]
    assert mc.get_str_id() == "fr:parler:indicatif"
    tc = mc[Tenses.fr.Présent]
    assert tc.get_str_id() == "fr:parler:indicatif:présent"
    assert tc[0].get_str_id() == "fr:parler:indicatif:présent:1:s::je"
    assert tc[1].get_str_id() == "fr:parler:indicatif:présent:2:s::tu"


def test_can_conjugate_all_verbs(ccg):
    verbs = ccg.get_verbs()
    all_conjugations = {}
    for verb in verbs:
        conjugation = ccg.conjugate(verb.infinitive)
        all_conjugations[verb] = conjugation
    assert len(all_conjugations) == len(verbs)


def test_inflector_fr_conjugate_compound_raser(tcg):
    infinitive = "raser"
    co = tcg._get_conj_obs(infinitive)
    tc = tcg._tense_conjugator_compound._conjugate_compound_mood_tense(
        co,
        Moods.fr.Subjonctif,
        Tenses.fr.Passé,
        Moods.fr.Subjonctif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert tc == TenseConjugation(
        Tenses.fr.Passé,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.fr.je, ["que j'aie rasé"]
            ),
            Conjugation(
                Person.Second,
                Number.Singular,
                None,
                Pronouns.fr.tu,
                ["que tu aies rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.m,
                Pronouns.fr.il,
                ["qu'il ait rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.fr.elle,
                ["qu'elle ait rasé"],
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.fr.on, ["qu'on ait rasé"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.fr.nous,
                ["que nous ayons rasé"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.fr.vous,
                ["que vous ayez rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.fr.ils,
                ["qu'ils aient rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.fr.elles,
                ["qu'elles aient rasé"],
            ),
        ],
    )


def test_inflector_fr_conjugate_compound_se_raser(tcg):
    """
    test targeting:
        - reflexive verb conjugation
        - compound verb conjugation with a verb conjugated with être (inflected participle)
        - Note: In French, all reflexive verbs are conjugated with être
    """
    infinitive = "se raser"
    co = tcg._get_conj_obs(infinitive)
    tc = tcg._tense_conjugator_compound._conjugate_compound_mood_tense(
        co,
        Moods.fr.Subjonctif,
        Tenses.fr.Passé,
        Moods.fr.Subjonctif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert tc == TenseConjugation(
        Tenses.fr.Passé,
        [
            Conjugation(
                Person.First,
                Number.Singular,
                Gender.f,
                Pronouns.fr.je,
                ["que je me sois rasée"],
            ),
            Conjugation(
                Person.First,
                Number.Singular,
                Gender.m,
                Pronouns.fr.je,
                ["que je me sois rasé"],
            ),
            Conjugation(
                Person.Second,
                Number.Singular,
                Gender.f,
                Pronouns.fr.tu,
                ["que tu te sois rasée"],
            ),
            Conjugation(
                Person.Second,
                Number.Singular,
                Gender.m,
                Pronouns.fr.tu,
                ["que tu te sois rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.m,
                Pronouns.fr.il,
                ["qu'il se soit rasé"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.fr.elle,
                ["qu'elle se soit rasée"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.fr.on,
                ["qu'on se soit rasée"],
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.m,
                Pronouns.fr.on,
                ["qu'on se soit rasé"],
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                Gender.f,
                Pronouns.fr.nous,
                ["que nous nous soyons rasées"],
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                Gender.m,
                Pronouns.fr.nous,
                ["que nous nous soyons rasés"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                Gender.f,
                Pronouns.fr.vous,
                ["que vous vous soyez rasées"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                Gender.m,
                Pronouns.fr.vous,
                ["que vous vous soyez rasés"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.fr.ils,
                ["qu'ils se soient rasés"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.fr.elles,
                ["qu'elles se soient rasées"],
            ),
        ],
    )


def test_inflector_fr_conjugate_compound_parler_indicative_passé_composé(tcg):
    """
    test targeting:
        - compound verb conjugation with a verb not conjugated with être (non-inflected participle)
    """
    infinitive = "parler"
    co = tcg._get_conj_obs(infinitive)
    tc = tcg._tense_conjugator_compound._conjugate_compound_mood_tense(
        co,
        Moods.fr.Indicatif,
        Tenses.fr.PasséComposé,
        Moods.fr.Indicatif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert tc == TenseConjugation(
        Tenses.fr.PasséComposé,
        [
            Conjugation(
                Person.First, Number.Singular, None, Pronouns.fr.je, ["j'ai parlé"]
            ),
            Conjugation(
                Person.Second, Number.Singular, None, Pronouns.fr.tu, ["tu as parlé"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, Pronouns.fr.il, ["il a parlé"]
            ),
            Conjugation(
                Person.Third,
                Number.Singular,
                Gender.f,
                Pronouns.fr.elle,
                ["elle a parlé"],
            ),
            Conjugation(
                Person.Third, Number.Singular, None, Pronouns.fr.on, ["on a parlé"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                None,
                Pronouns.fr.nous,
                ["nous avons parlé"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                None,
                Pronouns.fr.vous,
                ["vous avez parlé"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.m,
                Pronouns.fr.ils,
                ["ils ont parlé"],
            ),
            Conjugation(
                Person.Third,
                Number.Plural,
                Gender.f,
                Pronouns.fr.elles,
                ["elles ont parlé"],
            ),
        ],
    )


def test_inflector_fr_conjugate_simple_avoir_indicatif_présent_nopronouns(tcg):
    """
    Given:
    a verb in infinitive form
    When:
    I conjugate with conjugate_pronouns=False
    Then:
    The result is Pronouns.fr.je, ["ai"] etc. instead of Pronouns.fr.je, ["j'ai"] etc.
    """
    infinitive = "avoir"
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == ""
    mood = Moods.fr.Indicatif
    tense = Tenses.fr.Présent
    tense_elem = etree.fromstring(
        """<présent>
			<p><i>ai</i></p>
			<p><i>as</i></p>
			<p><i>a</i></p>
			<p><i>avons</i></p>
			<p><i>avez</i></p>
			<p><i>ont</i></p>
		</présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,
        modify_stem_strip_accents=False,
    )
    assert tc == TenseConjugation(
        Tenses.fr.Présent,
        [
            Conjugation(Person.First, Number.Singular, None, Pronouns.fr.je, ["ai"]),
            Conjugation(Person.Second, Number.Singular, None, Pronouns.fr.tu, ["as"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, Pronouns.fr.il, ["a"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, Pronouns.fr.elle, ["a"]
            ),
            Conjugation(Person.Third, Number.Singular, None, Pronouns.fr.on, ["a"]),
            Conjugation(Person.First, Number.Plural, None, Pronouns.fr.nous, ["avons"]),
            Conjugation(Person.Second, Number.Plural, None, Pronouns.fr.vous, ["avez"]),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, Pronouns.fr.ils, ["ont"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, Pronouns.fr.elles, ["ont"]
            ),
        ],
    )


def test_inflector_fr_conjugate_simple_avoir_participe_participe_passé(tcg):
    infinitive = "avoir"
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == ""
    mood = Moods.fr.Participe
    tense = Tenses.fr.ParticipePassé
    tense_elem = etree.fromstring(
        """<participe-passé>
			<p><i>eu</i></p>
			<p><i>eus</i></p>
			<p><i>eue</i></p>
			<p><i>eues</i></p>
		</participe-passé>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    # TODO: Support "ayant eu" ?
    assert tc == TenseConjugation(
        Tenses.fr.ParticipePassé,
        [
            Conjugation(None, Number.Singular, Gender.m, None, ["eu"]),
            Conjugation(None, Number.Plural, Gender.m, None, ["eus"]),
            Conjugation(None, Number.Singular, Gender.f, None, ["eue"]),
            Conjugation(None, Number.Plural, Gender.f, None, ["eues"]),
        ],
    )


def test_inflector_fr_conjugate_simple_avoir_particpe_participe_présent(tcg):
    infinitive = "avoir"
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == ""
    mood = Moods.fr.Participe
    tense = Tenses.fr.ParticipePresent
    tense_elem = etree.fromstring(
        """<participe-présent>
			<p><i>ayant</i></p>
		</participe-présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    assert tc == TenseConjugation(
        Tenses.fr.ParticipePresent,
        [
            Conjugation(None, None, None, None, ["ayant"]),
        ],
    )


def test_inflector_fr_conjugate_simple_avoir_infinitif_présent(tcg):
    """
    Test infinitif because it's the only one with neither
    person, number, gender nor pronoun.
    """
    infinitive = "avoir"
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == ""
    mood = Moods.fr.Infinitif
    tense = Tenses.fr.InfinitifPrésent
    tense_elem = etree.fromstring(
        """<infinitif-présent>
			<p><i>avoir</i></p>
		</infinitif-présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    assert tc == TenseConjugation(
        Tenses.fr.InfinitifPrésent,
        [
            Conjugation(None, None, None, None, ["avoir"]),
        ],
    )


def test_inflector_fr_conjugate_simple_avoir_imperatif_présent(tcg):
    infinitive = "avoir"
    co = tcg._get_conj_obs(infinitive)
    assert co.verb_stem == ""
    mood = Moods.fr.Imperatif
    tense = Tenses.fr.ImperatifPrésent
    tense_elem = etree.fromstring(
        """<imperatif-présent>
			<p><i>aie</i></p>
			<p><i>ayons</i></p>
			<p><i>ayez</i></p>
		</imperatif-présent>""",
        parser=None,
    )
    tense_template = TenseTemplateParser(Lang.fr, mood).parse(tense_elem)
    tc = tcg._tense_conjugator_simple._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    # see IMPERATIVE_PERSONS_FR
    expected_value = TenseConjugation(
        Tenses.fr.ImperatifPrésent,
        [
            Conjugation(Person.Second, Number.Singular, None, Pronouns.fr.tu, ["aie"]),
            Conjugation(Person.First, Number.Plural, None, Pronouns.fr.nous, ["ayons"]),
            Conjugation(Person.Second, Number.Plural, None, Pronouns.fr.vous, ["ayez"]),
        ],
    )
    assert tc == expected_value


# TODO: Write a test for imperatif-passé (compound)
