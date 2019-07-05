# -*- coding: utf-8 -*-

import pytest
from lxml import etree
from mock import patch
from verbecc.conjugator import (
    Conjugator,
    get_verb_stem,
    ConjugatorError,
    InvalidMoodError)
from verbecc.tense_template import TenseTemplate
from verbecc.string_utils import prepend_with_que
from verbecc.verbs_parser import (
    VerbNotFoundError
)

conj = Conjugator()

test_verbs = [
    (u"manger"), 
    (u"venir"), 
    (u"être"), 
    (u"aller"), 
    (u"pouvoir"), 
    (u"finir"),
    (u"pleuvoir")
]

@pytest.mark.parametrize("infinitif", test_verbs)
def test_conjugator_conjugate(infinitive):
    for infinitive in test_verbs:
        output = conj.conjugate(infinitive)
        assert output

def test_conjugator_conjugate_specific_tense():
    verb_stem = u"man"
    tense_elem = etree.fromstring(
        u"""<present>
        <p><i>ge</i></p>
        <p><i>ges</i></p>
        <p><i>ge</i></p>
        <p><i>geons</i></p>
        <p><i>gez</i></p>
        <p><i>gent</i></p>
        </present>""")
    tense_name = 'present'
    tense = TenseTemplate(tense_elem)
    out = conj._conjugate_specific_tense(verb_stem, 'indicative', tense)
    assert len(out) == 6
    assert out == [u"je mange", u"tu manges", u"il mange", u"nous mangeons", u"vous mangez", u"ils mangent"]

def test_conjugator_conjugate_passe_compose_with_avoir():
    assert conj.conjugate_passe_compose('manger') == [
    "j'ai mangé",
    "tu as mangé",
    "il a mangé",
    "nous avons mangé",
    "vous avez mangé",
    "ils ont mangé"
    ]

def test_conjugator_conjugate_passe_compose_with_etre():
    assert conj.conjugate_passe_compose('aller') == [
    "je suis allé",
    "tu es allé",
    "il est allé",
    "nous sommes allés",
    "vous êtes allés",
    "ils sont allés"
    ]

def test_conjugator_conjugate_subjunctive_past_with_avoir():
    assert conj.conjugate_subjunctive_past('manger') == [
    "que j'aie mangé",
    "que tu aies mangé",
    "qu'il ait mangé",
    "que nous ayons mangé",
    "que vous ayez mangé",
    "qu'ils aient mangé"
    ]

def test_conjugator_conjugate_subjunctive_past_with_etre():
    assert conj.conjugate_subjunctive_past('aller') == [
    "que je sois allé",
    "que tu sois allé",
    "qu'il soit allé",
    "que nous soyons allés",
    "que vous soyez allés",
    "qu'ils soient allés"
    ]

def test_conjugator_conjugate_conditional_past_with_avoir():
    assert conj.conjugate_conditional_past('manger') == [
    "j'aurais mangé",
    "tu aurais mangé",
    "il aurait mangé",
    "nous aurions mangé",
    "vous auriez mangé",
    "ils auraient mangé"
    ]

def test_conjugator_conjugate_conditional_past_with_etre():
    assert conj.conjugate_conditional_past('aller') == [
    "je serais allé",
    "tu serais allé",
    "il serait allé",
    "nous serions allés",
    "vous seriez allés",
    "ils seraient allés"
    ]

def test_conjugator_conjugate_pluperfect_with_avoir():
    assert conj.conjugate_pluperfect('manger') == [
    "j'avais mangé",
    "tu avais mangé",
    "il avait mangé",
    "nous avions mangé",
    "vous aviez mangé",
    "ils avaient mangé"
    ]

def test_conjugator_conjugate_pluperfect_with_etre():
    assert conj.conjugate_pluperfect('aller') == [
    "j'étais allé",
    "tu étais allé",
    "il était allé",
    "nous étions allés",
    "vous étiez allés",
    "ils étaient allés"
    ]

def test_conjugator_conjugate_subjunctive_pluperfect_with_avoir():
    assert conj.conjugate_subjunctive_pluperfect('manger') == [
    "que j'eusse mangé",
    "que tu eusses mangé",
    "qu'il eût mangé",
    "que nous eussions mangé",
    "que vous eussiez mangé",
    "qu'ils eussent mangé"
    ]

def test_conjugator_conjugate_subjunctive_pluperfect_with_etre():
    assert conj.conjugate_subjunctive_pluperfect('aller') == [
    "que je fusse allé",
    "que tu fusses allé",
    "qu'il fût allé",
    "que nous fussions allés",
    "que vous fussiez allés",
    "qu'ils fussent allés"
    ]

def test_conjugator_conjugate_future_perfect_with_avoir():
    assert conj.conjugate_future_perfect('manger') == [
    "j'aurai mangé",
    "tu auras mangé",
    "il aura mangé",
    "nous aurons mangé",
    "vous aurez mangé",
    "ils auront mangé"
    ]

def test_conjugator_conjugate_future_perfect_with_etre():
    assert conj.conjugate_future_perfect('aller') == [
    "je serai allé",
    "tu seras allé",
    "il sera allé",
    "nous serons allés",
    "vous serez allés",
    "ils seront allés"
    ]

def test_conjugator_conjugate_anterior_past_with_avoir():
    assert conj.conjugate_anterior_past('manger') == [
    "j'eus mangé",
    "tu eus mangé",
    "il eut mangé",
    "nous eûmes mangé",
    "vous eûtes mangé",
    "ils eurent mangé"
    ]

def test_conjugator_conjugate_anterior_past_with_etre():
    assert conj.conjugate_anterior_past('aller') == [
    "je fus allé",
    "tu fus allé",
    "il fut allé",
    "nous fûmes allés",
    "vous fûtes allés",
    "ils furent allés"
    ]

def test_conjugator_conjugate_imperative_past_with_avoir():
    assert conj.conjugate_imperative_past('manger') == [
    "aie mangé",
    "ayons mangé",
    "ayez mangé"
    ]

def test_conjugator_conjugate_imperative_past_with_etre():
    assert conj.conjugate_imperative_past('aller') == [
    "sois allé",
    "soyons allés",
    "soyez allés"
    ]

@patch('verbecc.person_ending.PersonEnding')
def test_conjugator_conjugate_specific_tense_pronoun(mock_person):
    verb_stem = u"man"
    pronoun = u"je"
    ending = u"ge"
    conjugation = conj._conjugate_specific_tense_pronoun(verb_stem, ending, pronoun)
    assert conjugation == u"je mange"

def test_conjugator_prepend_with_que():
    assert prepend_with_que("tu manges") == "que tu manges"
    assert prepend_with_que("il mange") == "qu'il mange"
    assert prepend_with_que("elles mangent") == "qu'elles mangent"

def test_conjugator_get_verb_stem():
    verb_stem = get_verb_stem(u"manger", u"man:ger")
    assert verb_stem == u"man"
    verb_stem = get_verb_stem(u"téléphoner", u"aim:er")
    assert verb_stem == u"téléphon"
    verb_stem = get_verb_stem(u"vendre", u"ten:dre")
    assert verb_stem == u"ven"
    # In the case of irregular verbs, the verb stem is empty string
    verb_stem = get_verb_stem(u"aller", u":aller")
    assert verb_stem == u""
    # The infinitive ending must match the template ending
    with pytest.raises(ConjugatorError):
        verb_stem = get_verb_stem(u"vendre", u"man:ger")

def test_conjugator_impersonal_verbs():
    impersonal_verbs = \
        [v.infinitive for v in conj.verb_parser.verbs 
        if conj.is_impersonal_verb(v.infinitive)]
    assert impersonal_verbs == [
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
    "sourdre"]

test_conjugator_verb_can_be_reflexive_data = [
    ("être", False),
    ("lever", True),
    ("pleuvoir", False),
    ("manger", True)
]
@pytest.mark.parametrize("infinitive,expected_result", 
                         test_conjugator_verb_can_be_reflexive_data)
def test_conjugator_verb_can_be_reflexive(infinitive, expected_result):
    assert conj.verb_can_be_reflexive(infinitive) == expected_result

expected_resp_conj_manger = {
"verb": {
  "infinitive": "manger",
  "template": "man:ger",
  "translation_en": "eat",
  "stem": "man"
},
"moods": {
  "infinitif": {
    "infinitif-présent": [
      "manger"
    ]
  },
  "indicative": {
    "present": [
      "je mange",
      "tu manges",
      "il mange",
      "nous mangeons",
      "vous mangez",
      "ils mangent"
    ],
    "imperfect": [
      "je mangeais",
      "tu mangeais",
      "il mangeait",
      "nous mangions",
      "vous mangiez",
      "ils mangeaient"
    ],
    "future": [
      "je mangerai",
      "tu mangeras",
      "il mangera",
      "nous mangerons",
      "vous mangerez",
      "ils mangeront"
    ],
    "simple-past": [
      "je mangeai",
      "tu mangeas",
      "il mangea",
      "nous mangeâmes",
      "vous mangeâtes",
      "ils mangèrent"
    ],
    "passé-composé": [
      "j'ai mangé",
      "tu as mangé",
      "il a mangé",
      "nous avons mangé",
      "vous avez mangé",
      "ils ont mangé"
    ],
    "pluperfect": [
      "j'avais mangé",
      "tu avais mangé",
      "il avait mangé",
      "nous avions mangé",
      "vous aviez mangé",
      "ils avaient mangé"
    ],
    "future-perfect": [
      "j'aurai mangé",
      "tu auras mangé",
      "il aura mangé",
      "nous aurons mangé",
      "vous aurez mangé",
      "ils auront mangé"
    ],
    "anterior-past": [
      "j'eus mangé",
      "tu eus mangé",
      "il eut mangé",
      "nous eûmes mangé",
      "vous eûtes mangé",
      "ils eurent mangé"
    ]
  },
  "conditional": {
    "present": [
      "je mangerais",
      "tu mangerais",
      "il mangerait",
      "nous mangerions",
      "vous mangeriez",
      "ils mangeraient"
    ],
    "past": [
      "j'aurais mangé",
      "tu aurais mangé",
      "il aurait mangé",
      "nous aurions mangé",
      "vous auriez mangé",
      "ils auraient mangé"
    ]
  },
  "subjunctive": {
    "present": [
      "que je mange",
      "que tu manges",
      "qu'il mange",
      "que nous mangions",
      "que vous mangiez",
      "qu'ils mangent"
    ],
    "imperfect": [
      "que je mangeasse",
      "que tu mangeasses",
      "qu'il mangeât",
      "que nous mangeassions",
      "que vous mangeassiez",
      "qu'ils mangeassent"
    ],
    "past": [
      "que j'aie mangé",
      "que tu aies mangé",
      "qu'il ait mangé",
      "que nous ayons mangé",
      "que vous ayez mangé",
      "qu'ils aient mangé"
    ],
    "pluperfect": [
      "que j'eusse mangé",
      "que tu eusses mangé",
      "qu'il eût mangé",
      "que nous eussions mangé",
      "que vous eussiez mangé",
      "qu'ils eussent mangé"
    ]
  },
  "imperative": {
    "imperative-present": [
      "mange",
      "mangeons",
      "mangez"
    ],
    "imperative-past": [
      "aie mangé",
      "ayons mangé",
      "ayez mangé"
    ]
  },
  "participle": {
    "present-participle": [
      "mangeant"
    ],
    "past-participle": [
      "mangé",
      "mangés",
      "mangée",
      "mangées"
    ]
  }
}
}

expected_resp_conj_pouvoir = {
"verb": {
  "infinitive": "pouvoir",
  "template": "p:ouvoir",
  "translation_en": "power",
  "stem": "p"
},
"moods": {
  "infinitif": {
    "infinitif-présent": [
      "pouvoir"
    ]
  },
  "indicative": {
    "present": [
      "je peux",
      "tu peux",
      "il peut",
      "nous pouvons",
      "vous pouvez",
      "ils peuvent"
    ],
    "imperfect": [
      "je pouvais",
      "tu pouvais",
      "il pouvait",
      "nous pouvions",
      "vous pouviez",
      "ils pouvaient"
    ],
    "future": [
      "je pourrai",
      "tu pourras",
      "il pourra",
      "nous pourrons",
      "vous pourrez",
      "ils pourront"
    ],
    "simple-past": [
      "je pus",
      "tu pus",
      "il put",
      "nous pûmes",
      "vous pûtes",
      "ils purent"
    ],
    "passé-composé": [
      "j'ai pu",
      "tu as pu",
      "il a pu",
      "nous avons pu",
      "vous avez pu",
      "ils ont pu"
    ],
    "pluperfect": [
      "j'avais pu",
      "tu avais pu",
      "il avait pu",
      "nous avions pu",
      "vous aviez pu",
      "ils avaient pu"
    ],
    "future-perfect": [
      "j'aurai pu",
      "tu auras pu",
      "il aura pu",
      "nous aurons pu",
      "vous aurez pu",
      "ils auront pu"
    ],
    "anterior-past": [
      "j'eus pu",
      "tu eus pu",
      "il eut pu",
      "nous eûmes pu",
      "vous eûtes pu",
      "ils eurent pu"
    ]
  },
  "conditional": {
    "present": [
      "je pourrais",
      "tu pourrais",
      "il pourrait",
      "nous pourrions",
      "vous pourriez",
      "ils pourraient"
    ],
    "past": [
      "j'aurais pu",
      "tu aurais pu",
      "il aurait pu",
      "nous aurions pu",
      "vous auriez pu",
      "ils auraient pu"
    ]
  },
  "subjunctive": {
    "present": [
      "que je puisse",
      "que tu puisses",
      "qu'il puisse",
      "que nous puissions",
      "que vous puissiez",
      "qu'ils puissent"
    ],
    "imperfect": [
      "que je pusse",
      "que tu pusses",
      "qu'il pût",
      "que nous pussions",
      "que vous pussiez",
      "qu'ils pussent"
    ],
    "past": [
      "que j'aie pu",
      "que tu aies pu",
      "qu'il ait pu",
      "que nous ayons pu",
      "que vous ayez pu",
      "qu'ils aient pu"
    ],
    "pluperfect": [
      "que j'eusse pu",
      "que tu eusses pu",
      "qu'il eût pu",
      "que nous eussions pu",
      "que vous eussiez pu",
      "qu'ils eussent pu"
    ]
  },
  "imperative": {
    "imperative-present": [],
    "imperative-past": []
  },
  "participle": {
    "present-participle": [
      "pouvant"
    ],
    "past-participle": [
      "pu",
      "pus",
      "pue",
      "pues"
    ]
  }
}
}

expected_resp_conj_pleuvoir = {
"verb": {
  "infinitive": "pleuvoir",
  "template": "pl:euvoir",
  "translation_en": "rain",
  "stem": "pl"
},
"moods": {
  "infinitif": {
    "infinitif-présent": [
      "pleuvoir"
    ]
  },
  "indicative": {
    "present": [
      "il pleut",
      "ils pleuvent"
    ],
    "imperfect": [
      "il pleuvait",
      "ils pleuvaient"
    ],
    "future": [
      "il pleuvra",
      "ils pleuvront"
    ],
    "simple-past": [
      "il plut",
      "ils plurent"
    ],
    "passé-composé": [
      "il a plu",
      "ils ont plu"
    ],
    "pluperfect": [
      "il avait plu",
      "ils avaient plu"
    ],
    "future-perfect": [
      "il aura plu",
      "ils auront plu"
    ],
    "anterior-past": [
      "il eut plu",
      "ils eurent plu"
    ]
  },
  "conditional": {
    "present": [
      "il pleuvrait",
      "ils pleuvraient"
    ],
    "past": [
      "il aurait plu",
      "ils auraient plu"
    ]
  },
  "subjunctive": {
    "present": [
      "qu'il pleuve",
      "qu'ils pleuvent"
    ],
    "imperfect": [
      "qu'il plût",
      "qu'ils plussent"
    ],
    "past": [
      "qu'il ait plu",
      "qu'ils aient plu"
    ],
    "pluperfect": [
      "qu'il eût plu",
      "qu'ils eussent plu"
    ]
  },
  "imperative": {
    "imperative-present": [],
    "imperative-past": []
  },
  "participle": {
    "present-participle": [
      "pleuvant"
    ],
    "past-participle": [
      "plu",
      "plus",
      "plue",
      "plues"
    ]
  }
}
}

expected_resp_conj_se_lever = {
"verb": {
  "infinitive": "lever",
  "template": "l:ever",
  "translation_en": "lift",
  "stem": "l"
},
"moods": {
  "infinitif": {
    "infinitif-présent": [
      "se lever"
    ]
  },
  "indicative": {
    "present": [
      "je me lève",
      "tu te lèves",
      "il se lève",
      "nous nous levons",
      "vous vous levez",
      "ils se lèvent"
    ],
    "imperfect": [
      "je me levais",
      "tu te levais",
      "il se levait",
      "nous nous levions",
      "vous vous leviez",
      "ils se levaient"
    ],
    "future": [
      "je me lèverai",
      "tu te lèveras",
      "il se lèvera",
      "nous nous lèverons",
      "vous vous lèverez",
      "ils se lèveront"
    ],
    "simple-past": [
      "je me levai",
      "tu te levas",
      "il se leva",
      "nous nous levâmes",
      "vous vous levâtes",
      "ils se levèrent"
    ],
    "passé-composé": [
      "je me suis levé",
      "tu t'es levé",
      "il s'est levé",
      "nous nous sommes levés",
      "vous vous êtes levés",
      "ils se sont levés"
    ],
    "pluperfect": [
      "je m'étais levé",
      "tu t'étais levé",
      "il s'était levé",
      "nous nous étions levés",
      "vous vous étiez levés",
      "ils s'étaient levés"
    ],
    "future-perfect": [
      "je me serai levé",
      "tu te seras levé",
      "il se sera levé",
      "nous nous serons levés",
      "vous vous serez levés",
      "ils se seront levés"
    ],
    "anterior-past": [
      "je me fus levé",
      "tu te fus levé",
      "il se fut levé",
      "nous nous fûmes levés",
      "vous vous fûtes levés",
      "ils se furent levés"
    ]
  },
  "conditional": {
    "present": [
      "je me lèverais",
      "tu te lèverais",
      "il se lèverait",
      "nous nous lèverions",
      "vous vous lèveriez",
      "ils se lèveraient"
    ],
    "past": [
      "je me serais levé",
      "tu te serais levé",
      "il se serait levé",
      "nous nous serions levés",
      "vous vous seriez levés",
      "ils se seraient levés"
    ]
  },
  "subjunctive": {
    "present": [
      "que je me lève",
      "que tu te lèves",
      "qu'il se lève",
      "que nous nous levions",
      "que vous vous leviez",
      "qu'ils se lèvent"
    ],
    "imperfect": [
      "que je me levasse",
      "que tu te levasses",
      "qu'il se levât",
      "que nous nous levassions",
      "que vous vous levassiez",
      "qu'ils se levassent"
    ],
    "past": [
      "que je me sois levé",
      "que tu te sois levé",
      "qu'il se soit levé",
      "que nous nous soyons levés",
      "que vous vous soyez levés",
      "qu'ils se soient levés"
    ],
    "pluperfect": [
      "que je me fusse levé",
      "que tu te fusses levé",
      "qu'il se fût levé",
      "que nous nous fussions levés",
      "que vous vous fussiez levés",
      "qu'ils se fussent levés"
    ]
  },
  "imperative": {
    "imperative-present": [
      "lève-toi",
      "levons-nous",
      "levez-vous"
    ],
    "imperative-past": []
  },
  "participle": {
    "present-participle": [
      "se levant"
    ],
    "past-participle": [
      "s'étant levé",
      "s'étant levés",
      "s'étant levée",
      "s'étant levées"
    ]
  }
}
}

test_conj_data = [
    ("manger", expected_resp_conj_manger),
    ("pouvoir", expected_resp_conj_pouvoir),
    ("Pouvoir", expected_resp_conj_pouvoir),
    ("pleuvoir", expected_resp_conj_pleuvoir),
    ("Se lever", expected_resp_conj_se_lever),
]

@pytest.mark.parametrize("infinitive,expected_resp", 
                         test_conj_data)
def test_conjugator_conjugate(infinitive, expected_resp):
    assert conj.conjugate(infinitive) == expected_resp

def test_conjugator_conjugate_vert_not_found():
    with pytest.raises(VerbNotFoundError):
        conj.conjugate("abcdefg")
