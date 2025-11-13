import pytest
from lxml import etree
from typing import cast

from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.number import Number
from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.conjugation import (
    TenseConjugation,
    Conjugation,
)
from verbecc.src.defs.types.mood import Moods
from verbecc.src.defs.types.tense import Tenses
from verbecc.src.parsers.tense_template_parser import TenseTemplateParser
from verbecc.src.defs.types.exceptions import ConjugatorError
from verbecc.src.defs.types.conjugation import (
    MoodConjugation,
    MoodsConjugation,
    TenseConjugation,
)


@pytest.fixture(scope="module")
def cg():
    cg = Conjugator(lang=Lang.fr)
    yield cg


def test_all_verbs_have_templates(cg):
    verbs = cg.get_verbs()
    template_names = cg.get_template_names()
    missing_templates = set()
    for verb in verbs:
        if verb.template not in template_names:
            missing_templates.add(verb.template)
    assert len(missing_templates) == 0


def test_add_subjunctive_relative_prounoun(cg):
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("tu manges", "")
        == "que tu manges"
    )
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("il mange", "") == "qu'il mange"
    )
    assert (
        cg._inflector.add_subjunctive_relative_pronoun("elles mangent", "")
        == "qu'elles mangent"
    )


def testadd_reflexive_pronoun(cg):
    assert cg._inflector.add_reflexive_pronoun("lever") == "se lever"
    assert cg._inflector.add_reflexive_pronoun("écrouler") == "s'écrouler"


def testsplit_reflexive(cg):
    assert cg._inflector.split_reflexive("se lever") == (True, "lever")
    assert cg._inflector.split_reflexive("s'écrouler") == (True, "écrouler")
    assert cg._inflector.split_reflexive("secouer") == (False, "secouer")


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        ("être", False),
        ("lever", True),
        ("pleuvoir", False),
        ("manger", True),
    ],
)
def test_inflector_fr_verb_can_be_reflexive(cg, infinitive, expected_result):
    assert cg._inflector.verb_can_be_reflexive(infinitive) == expected_result


def test_inflector_fr_impersonal_verbs(cg):
    impersonal_verbs = [
        v.infinitive
        for v in cg._inflector._verbs
        if cg._inflector._is_impersonal_verb(v.infinitive)
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


def test_inflector_fr_conjugate_simple_mood_tense(cg):
    infinitive = "manger"
    mood = Moods.fr.Indicatif
    tense = Tenses.fr.Présent
    co = cg._get_conj_obs(infinitive)
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
    out = cg._conjugate_simple_mood_tense(co.verb_stem, mood, tense, tense_template)
    assert len(out) == 6
    assert out == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, Gender.m, "je", ["je mange"]),
            Conjugation(Person.Second, Number.Singular, Gender.m, "tu", ["tu manges"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "il", ["il mange"]),
            Conjugation(
                Person.First, Number.Plural, Gender.m, "nous", ["nous mangeons"]
            ),
            Conjugation(
                Person.Second, Number.Plural, Gender.m, "vous", ["vous mangez"]
            ),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ils", ["ils mangent"]),
        ]
    )


def test_inflector_fr_get_verb_stem_from_template_name(cg):
    verb_stem = cg._inflector.get_verb_stem_from_template_name("manger", "man:ger")
    assert verb_stem == "man"
    verb_stem = cg._inflector.get_verb_stem_from_template_name("téléphoner", "aim:er")
    assert verb_stem == "téléphon"
    verb_stem = cg._inflector.get_verb_stem_from_template_name("vendre", "ten:dre")
    assert verb_stem == "ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = cg._inflector.get_verb_stem_from_template_name("aller", ":aller")
    assert verb_stem == ""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = cg._inflector.get_verb_stem_from_template_name("vendre", "man:ger")


@pytest.mark.parametrize(
    "person,number,gender,is_reflexive,expected_result",
    [
        (Person.First, Number.Singular, Gender.m, False, "je"),
        (Person.First, Number.Singular, Gender.m, True, "je me"),
        (Person.Second, Number.Singular, Gender.m, False, "tu"),
        (Person.Second, Number.Singular, Gender.m, True, "tu te"),
        (Person.Third, Number.Singular, Gender.m, False, "il"),
        (Person.Third, Number.Singular, Gender.m, True, "il se"),
        (Person.Third, Number.Singular, Gender.f, False, "elle"),
        (Person.Third, Number.Singular, Gender.f, True, "elle se"),
        (Person.First, Number.Plural, Gender.m, False, "nous"),
        (Person.First, Number.Plural, Gender.m, True, "nous nous"),
        (Person.Second, Number.Plural, Gender.m, False, "vous"),
        (Person.Second, Number.Plural, Gender.m, True, "vous vous"),
        (Person.Third, Number.Plural, Gender.m, False, "ils"),
        (Person.Third, Number.Plural, Gender.m, True, "ils se"),
        (Person.Third, Number.Plural, Gender.f, False, "elles"),
        (Person.Third, Number.Plural, Gender.f, True, "elles se"),
    ],
)
def test_inflector_fr_get_pronouns(
    cg,
    person: Person,
    number: Number,
    gender: Gender,
    is_reflexive: bool,
    expected_result: str,
):
    pronoun = cg._inflector.get_pronouns(person, number, gender)[0]
    if is_reflexive:
        pronoun = cg._inflector.make_pronoun_reflexive(pronoun)
    assert pronoun == expected_result


@pytest.mark.parametrize(
    "infinitive,expected_result",
    [
        (
            "avoir",
            ["j'ai", "tu as", "il a", "nous avons", "vous avez", "ils ont"],
        ),
        (
            "habiter",
            [
                "j'habite",
                "tu habites",
                "il habite",
                "nous habitons",
                "vous habitez",
                "ils habitent",
            ],
        ),
        (
            "s'habiller",
            [
                "je m'habille",
                "tu t'habilles",
                "il s'habille",
                "nous nous habillons",
                "vous vous habillez",
                "ils s'habillent",
            ],
        ),
    ],
)
def test_pronoun_combined_vowel_h_non_aspiré(cg, infinitive, expected_result):
    cc = cg.conjugate(infinitive)
    moods_conj = cc.moods
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
def test_subjonctif_vowel_h_non_aspiré(cg, infinitive, expected_result):
    cc = cg.conjugate(infinitive)
    moods_conj = cc.moods
    mood_conj = moods_conj[Moods.fr.Subjonctif]
    tense_conj = mood_conj[Tenses.fr.Présent]
    assert [c[0] for c in tense_conj] == expected_result


def test_can_conjugate_all_verbs(cg):
    verbs = cg.get_verbs()
    all_conjugations = {}
    for verb in verbs:
        conjugation = cg.conjugate(verb.infinitive)
        all_conjugations[verb] = conjugation
    assert len(all_conjugations) == len(verbs)


def test_inflector_fr_conjugate_compound_raser(cg):
    infinitive = "raser"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        Moods.fr.Subjonctif,
        Tenses.fr.Passé,
        Moods.fr.Subjonctif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, None, "je", ["que j'aie rasé"]),
            Conjugation(
                Person.Second, Number.Singular, None, "tu", ["que tu aies rasé"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, "il", ["qu'il ait rasé"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, "elle", ["qu'elle ait rasé"]
            ),
            Conjugation(Person.Third, Number.Singular, None, "on", ["qu'on ait rasé"]),
            Conjugation(
                Person.First, Number.Plural, None, "nous", ["que nous ayons rasé"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, "vous", ["que vous ayez rasé"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ils", ["qu'ils aient rasé"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, "elles", ["qu'elles aient rasé"]
            ),
        ]
    )


def test_inflector_fr_conjugate_compound_se_raser(cg):
    """
    test targeting:
        - reflexive verb conjugation
        - compound verb conjugation with a verb conjugated with être (inflected participle)
        - Note: In French, all reflexive verbs are conjugated with être
    """
    infinitive = "se raser"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        Moods.fr.Subjonctif,
        Tenses.fr.Passé,
        Moods.fr.Subjonctif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(
                Person.First, Number.Singular, Gender.m, "je", ["que je me sois rasé"]
            ),
            Conjugation(
                Person.Second, Number.Singular, Gender.m, "tu", ["que tu te sois rasé"]
            ),
            Conjugation(
                Person.Third, Number.Singular, Gender.m, "il", ["qu'il se soit rasé"]
            ),
            Conjugation(
                Person.First,
                Number.Plural,
                Gender.m,
                "nous",
                ["que nous nous soyons rasés"],
            ),
            Conjugation(
                Person.Second,
                Number.Plural,
                Gender.m,
                "vous",
                ["que vous vous soyez rasés"],
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ils", ["qu'ils se soient rasés"]
            ),
        ]
    )


def test_inflector_fr_conjugate_compound_parler_indicative_passé_composé(cg):
    """
    test targeting:
        - compound verb conjugation with a verb not conjugated with être (non-inflected participle)
    """
    infinitive = "parler"
    co = cg._get_conj_obs(infinitive)
    ret = cg._conjugate_compound(
        co,
        Moods.fr.Indicatif,
        Tenses.fr.PasséCompose,
        Moods.fr.Indicatif,
        Tenses.fr.Présent,
        aux_uses_alternate=False,
        conjugate_pronouns=True,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, None, "je", ["j'ai parlé"]),
            Conjugation(Person.Second, Number.Singular, None, "tu", ["tu as parlé"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "il", ["il a parlé"]),
            Conjugation(
                Person.Third, Number.Singular, Gender.f, "elle", ["elle a parlé"]
            ),
            Conjugation(Person.Third, Number.Singular, None, "on", ["on a parlé"]),
            Conjugation(
                Person.First, Number.Plural, None, "nous", ["nous avons parlé"]
            ),
            Conjugation(
                Person.Second, Number.Plural, None, "vous", ["vous avez parlé"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.m, "ils", ["ils ont parlé"]
            ),
            Conjugation(
                Person.Third, Number.Plural, Gender.f, "elles", ["elles ont parlé"]
            ),
        ]
    )


def test_inflector_fr_conjugate_simple_avoir_indicatif_présent_nopronouns(cg):
    """
    Given:
    a verb in infinitive form
    When:
    I conjugate with conjugate_pronouns=False
    Then:
    The result is "je", ["ai"] etc. instead of "je", ["j'ai"] etc.
    """
    infinitive = "avoir"
    co = cg._get_conj_obs(infinitive)
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
    ret = cg._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,
        modify_stem_strip_accents=False,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(Person.First, Number.Singular, None, "je", ["ai"]),
            Conjugation(Person.Second, Number.Singular, None, "tu", ["as"]),
            Conjugation(Person.Third, Number.Singular, Gender.m, "il", ["a"]),
            Conjugation(Person.Third, Number.Singular, Gender.f, "elle", ["a"]),
            Conjugation(Person.Third, Number.Singular, None, "on", ["a"]),
            Conjugation(Person.First, Number.Plural, None, "nous", ["avons"]),
            Conjugation(Person.Second, Number.Plural, None, "vous", ["avez"]),
            Conjugation(Person.Third, Number.Plural, Gender.m, "ils", ["ont"]),
            Conjugation(Person.Third, Number.Plural, Gender.f, "elles", ["ont"]),
        ]
    )


def test_inflector_fr_conjugate_simple_avoir_participe_participe_passé(cg):
    infinitive = "avoir"
    co = cg._get_conj_obs(infinitive)
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
    ret = cg._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    # TODO: Support "ayant eu" ?
    assert ret == TenseConjugation(
        [
            Conjugation(None, Number.Singular, Gender.m, None, ["eu"]),
            Conjugation(None, Number.Plural, Gender.m, None, ["eus"]),
            Conjugation(None, Number.Singular, Gender.f, None, ["eue"]),
            Conjugation(None, Number.Plural, Gender.f, None, ["eues"]),
        ]
    )


def test_inflector_fr_conjugate_simple_avoir_particpe_participe_présent(cg):
    infinitive = "avoir"
    co = cg._get_conj_obs(infinitive)
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
    ret = cg._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(None, None, None, None, ["ayant"]),
        ]
    )


def test_inflector_fr_conjugate_simple_avoir_infinitif_présent(cg):
    """
    Test infinitif because it's the only one with neither
    person, number, gender nor pronoun.
    """
    infinitive = "avoir"
    co = cg._get_conj_obs(infinitive)
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
    ret = cg._conjugate_simple_mood_tense(
        co.verb_stem,
        mood,
        tense,
        tense_template,
        is_reflexive=False,
        conjugate_pronouns=False,  # this tense is conjugated without pronouns in any case
        modify_stem_strip_accents=False,
    )
    assert ret == TenseConjugation(
        [
            Conjugation(None, None, None, None, ["avoir"]),
        ]
    )


def test_inflector_fr_conjugate_simple_avoir_imperatif_présent(cg):
    infinitive = "avoir"
    co = cg._get_conj_obs(infinitive)
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
    ret = cg._conjugate_simple_mood_tense(
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
        [
            Conjugation(Person.Second, Number.Singular, None, "tu", ["aie"]),
            Conjugation(Person.First, Number.Plural, None, "nous", ["ayons"]),
            Conjugation(Person.Second, Number.Plural, None, "vous", ["ayez"]),
        ]
    )
    assert ret == expected_value


# TODO: Write a test for imperatif-passé (compound)
