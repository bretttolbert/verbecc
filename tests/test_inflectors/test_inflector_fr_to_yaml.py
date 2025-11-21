# coding: utf-8
import pytest

from verbecc.src.defs.types.conjugation import CompleteConjugation
from verbecc.src.conjugator.complete_conjugator import CompleteConjugator
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


@pytest.fixture(scope="module")
def ccg():
    ccg = CompleteConjugator(lang=Lang.fr)
    yield ccg


expected_value_conj_se_lever = """moods:
  conditionnel:
    passé:
    - c:
      - je me serais levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - je me serais levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - tu te serais levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - tu te serais levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - il se serait levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se serait levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se serait levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - on se serait levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous serions levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - nous nous serions levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous seriez levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - vous vous seriez levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - ils se seraient levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se seraient levées
      g: f
      n: p
      p: 3
      pr: elles
    présent:
    - c:
      - je me lèverais
      n: s
      p: 1
      pr: je
    - c:
      - tu te lèverais
      n: s
      p: 2
      pr: tu
    - c:
      - il se lèverait
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se lèverait
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se lèverait
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous lèverions
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous lèveriez
      n: p
      p: 2
      pr: vous
    - c:
      - ils se lèveraient
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se lèveraient
      g: f
      n: p
      p: 3
      pr: elles
  imperatif:
    imperatif-passé: []
    imperatif-présent:
    - c:
      - lève-toi
      n: s
      p: 2
      pr: tu
    - c:
      - levons-nous
      n: p
      p: 1
      pr: nous
    - c:
      - levez-vous
      n: p
      p: 2
      pr: vous
  indicatif:
    futur-antérieur:
    - c:
      - je me serai levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - je me serai levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - tu te seras levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - tu te seras levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - il se sera levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se sera levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se sera levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - on se sera levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous serons levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - nous nous serons levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous serez levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - vous vous serez levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - ils se seront levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se seront levées
      g: f
      n: p
      p: 3
      pr: elles
    futur-simple:
    - c:
      - je me lèverai
      n: s
      p: 1
      pr: je
    - c:
      - tu te lèveras
      n: s
      p: 2
      pr: tu
    - c:
      - il se lèvera
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se lèvera
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se lèvera
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous lèverons
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous lèverez
      n: p
      p: 2
      pr: vous
    - c:
      - ils se lèveront
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se lèveront
      g: f
      n: p
      p: 3
      pr: elles
    imparfait:
    - c:
      - je me levais
      n: s
      p: 1
      pr: je
    - c:
      - tu te levais
      n: s
      p: 2
      pr: tu
    - c:
      - il se levait
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se levait
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se levait
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous levions
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous leviez
      n: p
      p: 2
      pr: vous
    - c:
      - ils se levaient
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se levaient
      g: f
      n: p
      p: 3
      pr: elles
    passé-antérieur:
    - c:
      - je me fus levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - je me fus levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - tu te fus levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - tu te fus levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - il se fut levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se fut levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se fut levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - on se fut levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous fûmes levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - nous nous fûmes levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous fûtes levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - vous vous fûtes levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - ils se furent levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se furent levées
      g: f
      n: p
      p: 3
      pr: elles
    passé-composé:
    - c:
      - je me suis levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - je me suis levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - tu t'es levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - tu t'es levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - il s'est levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle s'est levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on s'est levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - on s'est levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous sommes levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - nous nous sommes levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous êtes levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - vous vous êtes levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - ils se sont levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se sont levées
      g: f
      n: p
      p: 3
      pr: elles
    passé-simple:
    - c:
      - je me levai
      n: s
      p: 1
      pr: je
    - c:
      - tu te levas
      n: s
      p: 2
      pr: tu
    - c:
      - il se leva
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se leva
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se leva
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous levâmes
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous levâtes
      n: p
      p: 2
      pr: vous
    - c:
      - ils se levèrent
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se levèrent
      g: f
      n: p
      p: 3
      pr: elles
    plus-que-parfait:
    - c:
      - je m'étais levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - je m'étais levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - tu t'étais levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - tu t'étais levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - il s'était levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle s'était levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on s'était levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - on s'était levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous étions levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - nous nous étions levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous étiez levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - vous vous étiez levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - ils s'étaient levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles s'étaient levées
      g: f
      n: p
      p: 3
      pr: elles
    présent:
    - c:
      - je me lève
      n: s
      p: 1
      pr: je
    - c:
      - tu te lèves
      n: s
      p: 2
      pr: tu
    - c:
      - il se lève
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - elle se lève
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - on se lève
      n: s
      p: 3
      pr: 'on'
    - c:
      - nous nous levons
      n: p
      p: 1
      pr: nous
    - c:
      - vous vous levez
      n: p
      p: 2
      pr: vous
    - c:
      - ils se lèvent
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - elles se lèvent
      g: f
      n: p
      p: 3
      pr: elles
  infinitif:
    infinitif-présent:
    - c:
      - lever
  participe:
    participe-passé:
    - c:
      - étant levé
      g: m
      n: s
    - c:
      - étant levés
      g: m
      n: p
    - c:
      - étant levée
      g: f
      n: s
    - c:
      - étant levées
      g: f
      n: p
    participe-présent:
    - c:
      - levant
  subjonctif:
    imparfait:
    - c:
      - que je me levasse
      n: s
      p: 1
      pr: je
    - c:
      - que tu te levasses
      n: s
      p: 2
      pr: tu
    - c:
      - qu'il se levât
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - qu'elle se levât
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - qu'on se levât
      n: s
      p: 3
      pr: 'on'
    - c:
      - que nous nous levassions
      n: p
      p: 1
      pr: nous
    - c:
      - que vous vous levassiez
      n: p
      p: 2
      pr: vous
    - c:
      - qu'ils se levassent
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - qu'elles se levassent
      g: f
      n: p
      p: 3
      pr: elles
    passé:
    - c:
      - que je me sois levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - que je me sois levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - que tu te sois levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - que tu te sois levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - qu'il se soit levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - qu'elle se soit levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - qu'on se soit levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - qu'on se soit levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - que nous nous soyons levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - que nous nous soyons levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - que vous vous soyez levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - que vous vous soyez levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - qu'ils se soient levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - qu'elles se soient levées
      g: f
      n: p
      p: 3
      pr: elles
    plus-que-parfait:
    - c:
      - que je me fusse levée
      g: f
      n: s
      p: 1
      pr: je
    - c:
      - que je me fusse levé
      g: m
      n: s
      p: 1
      pr: je
    - c:
      - que tu te fusses levée
      g: f
      n: s
      p: 2
      pr: tu
    - c:
      - que tu te fusses levé
      g: m
      n: s
      p: 2
      pr: tu
    - c:
      - qu'il se fût levé
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - qu'elle se fût levée
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - qu'on se fût levée
      g: f
      n: s
      p: 3
      pr: 'on'
    - c:
      - qu'on se fût levé
      g: m
      n: s
      p: 3
      pr: 'on'
    - c:
      - que nous nous fussions levées
      g: f
      n: p
      p: 1
      pr: nous
    - c:
      - que nous nous fussions levés
      g: m
      n: p
      p: 1
      pr: nous
    - c:
      - que vous vous fussiez levées
      g: f
      n: p
      p: 2
      pr: vous
    - c:
      - que vous vous fussiez levés
      g: m
      n: p
      p: 2
      pr: vous
    - c:
      - qu'ils se fussent levés
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - qu'elles se fussent levées
      g: f
      n: p
      p: 3
      pr: elles
    présent:
    - c:
      - que je me lève
      n: s
      p: 1
      pr: je
    - c:
      - que tu te lèves
      n: s
      p: 2
      pr: tu
    - c:
      - qu'il se lève
      g: m
      n: s
      p: 3
      pr: il
    - c:
      - qu'elle se lève
      g: f
      n: s
      p: 3
      pr: elle
    - c:
      - qu'on se lève
      n: s
      p: 3
      pr: 'on'
    - c:
      - que nous nous levions
      n: p
      p: 1
      pr: nous
    - c:
      - que vous vous leviez
      n: p
      p: 2
      pr: vous
    - c:
      - qu'ils se lèvent
      g: m
      n: p
      p: 3
      pr: ils
    - c:
      - qu'elles se lèvent
      g: f
      n: p
      p: 3
      pr: elles
verb:
  infinitive: lever
  lang: fr
  predicted: false
  stem: l
  template: l:ever
  translation_en: lift
"""


def run_test_conjugate_to_yaml(
    ccg: CompleteConjugator, infinitive: str, expected_value: str
):
    cc = ccg.conjugate(infinitive)
    conj_yaml = cc.to_yaml()
    assert conj_yaml == expected_value


def test_conjugate_to_yaml_Se_lever(ccg):
    run_test_conjugate_to_yaml(ccg, "Se lever", expected_value_conj_se_lever)
