# Français

### French `manger` (to eat)
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.fr) 
# If this is the first run, it will take a minute for the model to train, 
# but it should save the model .zip file and run fast subsequently
>>> cc = ccg.conjugate("manger")
>>> print(cc)
{
    "moods":
    {
        "conditionnel":
        {
            "passé": [
                ["1", "s",
                    null, "je",
                    ["j'aurais mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu aurais mangé"]
                ],
                ["3", "s", "m", "il",
                    ["il aurait mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["elle aurait mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["on aurait mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous aurions mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous auriez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["ils auraient mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["elles auraient mangé"]
                ]
            ],
            "présent": [
                ["1", "s",
                    null, "je",
                    ["je mangerais"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu mangerais"]
                ],
                ["3", "s", "m", "il",
                    ["il mangerait"]
                ],
                ["3", "s", "f", "elle",
                    ["elle mangerait"]
                ],
                ["3", "s",
                    null, "on",
                    ["on mangerait"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous mangerions"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous mangeriez"]
                ],
                ["3", "p", "m", "ils",
                    ["ils mangeraient"]
                ],
                ["3", "p", "f", "elles",
                    ["elles mangeraient"]
                ]
            ]
        },
        "imperatif":
        {
            "imperatif-passé": [
                ["2", "s",
                    null, "tu",
                    ["aie mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["ayons mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["ayez mangé"]
                ]
            ],
            "imperatif-présent": [
                ["2", "s",
                    null, "tu",
                    ["mange"]
                ],
                ["1", "p",
                    null, "nous",
                    ["mangeons"]
                ],
                ["2", "p",
                    null, "vous",
                    ["mangez"]
                ]
            ]
        },
        "indicatif":
        {
            "futur-antérieur": [
                ["1", "s",
                    null, "je",
                    ["j'aurai mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu auras mangé"]
                ],
                ["3", "s", "m", "il",
                    ["il aura mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["elle aura mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["on aura mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous aurons mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous aurez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["ils auront mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["elles auront mangé"]
                ]
            ],
            "futur-simple": [
                ["1", "s",
                    null, "je",
                    ["je mangerai"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu mangeras"]
                ],
                ["3", "s", "m", "il",
                    ["il mangera"]
                ],
                ["3", "s", "f", "elle",
                    ["elle mangera"]
                ],
                ["3", "s",
                    null, "on",
                    ["on mangera"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous mangerons"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous mangerez"]
                ],
                ["3", "p", "m", "ils",
                    ["ils mangeront"]
                ],
                ["3", "p", "f", "elles",
                    ["elles mangeront"]
                ]
            ],
            "imparfait": [
                ["1", "s",
                    null, "je",
                    ["je mangeais"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu mangeais"]
                ],
                ["3", "s", "m", "il",
                    ["il mangeait"]
                ],
                ["3", "s", "f", "elle",
                    ["elle mangeait"]
                ],
                ["3", "s",
                    null, "on",
                    ["on mangeait"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous mangions"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous mangiez"]
                ],
                ["3", "p", "m", "ils",
                    ["ils mangeaient"]
                ],
                ["3", "p", "f", "elles",
                    ["elles mangeaient"]
                ]
            ],
            "passé-antérieur": [
                ["1", "s",
                    null, "je",
                    ["j'eus mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu eus mangé"]
                ],
                ["3", "s", "m", "il",
                    ["il eut mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["elle eut mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["on eut mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous eûmes mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous eûtes mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["ils eurent mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["elles eurent mangé"]
                ]
            ],
            "passé-composé": [
                ["1", "s",
                    null, "je",
                    ["j'ai mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu as mangé"]
                ],
                ["3", "s", "m", "il",
                    ["il a mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["elle a mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["on a mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous avons mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous avez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["ils ont mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["elles ont mangé"]
                ]
            ],
            "passé-simple": [
                ["1", "s",
                    null, "je",
                    ["je mangeai"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu mangeas"]
                ],
                ["3", "s", "m", "il",
                    ["il mangea"]
                ],
                ["3", "s", "f", "elle",
                    ["elle mangea"]
                ],
                ["3", "s",
                    null, "on",
                    ["on mangea"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous mangeâmes"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous mangeâtes"]
                ],
                ["3", "p", "m", "ils",
                    ["ils mangèrent"]
                ],
                ["3", "p", "f", "elles",
                    ["elles mangèrent"]
                ]
            ],
            "plus-que-parfait": [
                ["1", "s",
                    null, "je",
                    ["j'avais mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu avais mangé"]
                ],
                ["3", "s", "m", "il",
                    ["il avait mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["elle avait mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["on avait mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous avions mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous aviez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["ils avaient mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["elles avaient mangé"]
                ]
            ],
            "présent": [
                ["1", "s",
                    null, "je",
                    ["je mange"]
                ],
                ["2", "s",
                    null, "tu",
                    ["tu manges"]
                ],
                ["3", "s", "m", "il",
                    ["il mange"]
                ],
                ["3", "s", "f", "elle",
                    ["elle mange"]
                ],
                ["3", "s",
                    null, "on",
                    ["on mange"]
                ],
                ["1", "p",
                    null, "nous",
                    ["nous mangeons"]
                ],
                ["2", "p",
                    null, "vous",
                    ["vous mangez"]
                ],
                ["3", "p", "m", "ils",
                    ["ils mangent"]
                ],
                ["3", "p", "f", "elles",
                    ["elles mangent"]
                ]
            ]
        },
        "infinitif":
        {
            "infinitif-présent": [
                [
                    null,
                    null,
                    null,
                    null,
                    ["manger"]
                ]
            ]
        },
        "participe":
        {
            "participe-passé": [
                [
                    null, "s", "m",
                    null,
                    ["mangé"]
                ],
                [
                    null, "p", "m",
                    null,
                    ["mangés"]
                ],
                [
                    null, "s", "f",
                    null,
                    ["mangée"]
                ],
                [
                    null, "p", "f",
                    null,
                    ["mangées"]
                ]
            ],
            "participe-présent": [
                [
                    null,
                    null,
                    null,
                    null,
                    ["mangeant"]
                ]
            ]
        },
        "subjonctif":
        {
            "imparfait": [
                ["1", "s",
                    null, "je",
                    ["que je mangeasse"]
                ],
                ["2", "s",
                    null, "tu",
                    ["que tu mangeasses"]
                ],
                ["3", "s", "m", "il",
                    ["qu'il mangeât"]
                ],
                ["3", "s", "f", "elle",
                    ["qu'elle mangeât"]
                ],
                ["3", "s",
                    null, "on",
                    ["qu'on mangeât"]
                ],
                ["1", "p",
                    null, "nous",
                    ["que nous mangeassions"]
                ],
                ["2", "p",
                    null, "vous",
                    ["que vous mangeassiez"]
                ],
                ["3", "p", "m", "ils",
                    ["qu'ils mangeassent"]
                ],
                ["3", "p", "f", "elles",
                    ["qu'elles mangeassent"]
                ]
            ],
            "passé": [
                ["1", "s",
                    null, "je",
                    ["que j'aie mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["que tu aies mangé"]
                ],
                ["3", "s", "m", "il",
                    ["qu'il ait mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["qu'elle ait mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["qu'on ait mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["que nous ayons mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["que vous ayez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["qu'ils aient mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["qu'elles aient mangé"]
                ]
            ],
            "plus-que-parfait": [
                ["1", "s",
                    null, "je",
                    ["que j'eusse mangé"]
                ],
                ["2", "s",
                    null, "tu",
                    ["que tu eusses mangé"]
                ],
                ["3", "s", "m", "il",
                    ["qu'il eût mangé"]
                ],
                ["3", "s", "f", "elle",
                    ["qu'elle eût mangé"]
                ],
                ["3", "s",
                    null, "on",
                    ["qu'on eût mangé"]
                ],
                ["1", "p",
                    null, "nous",
                    ["que nous eussions mangé"]
                ],
                ["2", "p",
                    null, "vous",
                    ["que vous eussiez mangé"]
                ],
                ["3", "p", "m", "ils",
                    ["qu'ils eussent mangé"]
                ],
                ["3", "p", "f", "elles",
                    ["qu'elles eussent mangé"]
                ]
            ],
            "présent": [
                ["1", "s",
                    null, "je",
                    ["que je mange"]
                ],
                ["2", "s",
                    null, "tu",
                    ["que tu manges"]
                ],
                ["3", "s", "m", "il",
                    ["qu'il mange"]
                ],
                ["3", "s", "f", "elle",
                    ["qu'elle mange"]
                ],
                ["3", "s",
                    null, "on",
                    ["qu'on mange"]
                ],
                ["1", "p",
                    null, "nous",
                    ["que nous mangions"]
                ],
                ["2", "p",
                    null, "vous",
                    ["que vous mangiez"]
                ],
                ["3", "p", "m", "ils",
                    ["qu'ils mangent"]
                ],
                ["3", "p", "f", "elles",
                    ["qu'elles mangent"]
                ]
            ]
        }
    },
    "verb":
    {
        "infinitive": "manger",
        "lang": "fr",
        "pred_score": 1.0,
        "predicted": false,
        "stem": "man",
        "template": "man:ger",
        "translation_en": "eat"
    }
}

>>> cc[Moods.fr.Indicatif][Tenses.fr.Présent]
[
    ["1", "s",
        null, "je",
        ["je mange"]
    ],
    ["2", "s",
        null, "tu",
        ["tu manges"]
    ],
    ["3", "s", "m", "il",
        ["il mange"]
    ],
    ["3", "s", "f", "elle",
        ["elle mange"]
    ],
    ["3", "s",
        null, "on",
        ["on mange"]
    ],
    ["1", "p",
        null, "nous",
        ["nous mangeons"]
    ],
    ["2", "p",
        null, "vous",
        ["vous mangez"]
    ],
    ["3", "p", "m", "ils",
        ["ils mangent"]
    ],
    ["3", "p", "f", "elles",
        ["elles mangent"]
    ]
]

>>> cc.get_moods().get_data().keys()
dict_keys([<MoodFr.Infinitif: 'infinitif'>, <MoodFr.Indicatif: 'indicatif'>, <MoodFr.Conditionnel: 'conditionnel'>, <MoodFr.Subjonctif: 'subjonctif'>, <MoodFr.Imperatif: 'imperatif'>, <MoodFr.Participe: 'participe'>])
>>> cc[Moods.fr.Indicatif].get_data().keys()
dict_keys([<TenseFr.Présent: 'présent'>, <TenseFr.Imparfait: 'imparfait'>, <TenseFr.FuturSimple: 'futur-simple'>, <TenseFr.PasséSimple: 'passé-simple'>, <TenseFr.PasséComposé: 'passé-composé'>, <TenseFr.PlusQueParfait: 'plus-que-parfait'>, <TenseFr.FuturAntérieur: 'futur-antérieur'>, <TenseFr.PasséAntérieur: 'passé-antérieur'>])
>>> cc[Moods.fr.Subjonctif].get_data().keys()
dict_keys([<TenseFr.Présent: 'présent'>, <TenseFr.Imparfait: 'imparfait'>, <TenseFr.Passé: 'passé'>, <TenseFr.PlusQueParfait: 'plus-que-parfait'>])
```

### French `être` (to be)
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.fr)
# Observe that it finds and conjugates `être` even though we input `etre`
>>> print(cg.conjugate('etre'))
{
    "verb": {
        "infinitive": "être",
        "predicted": false,
        "pred_score": 1.0,
        "template": ":être",
        "translation_en": "be",
        "stem": ""
    },
    "moods": {
        "infinitif": {
            "infinitif-présent": [
                "être"
            ]
        },
        "indicatif": {
            "présent": [
                "je suis",
                "tu es",
                "il est",
                "nous sommes",
                "vous êtes",
                "ils sont"
            ],
            "imparfait": [
                "j'étais",
                "tu étais",
                "il était",
                "nous étions",
                "vous étiez",
                "ils étaient"
            ],
            "futur-simple": [
                "je serai",
                "tu seras",
                "il sera",
                "nous serons",
                "vous serez",
                "ils seront"
            ],
            "passé-simple": [
                "je fus",
                "tu fus",
                "il fut",
                "nous fûmes",
                "vous fûtes",
                "ils furent"
            ],
            "passé-composé": [
                "j'ai été",
                "tu as été",
                "il a été",
                "nous avons été",
                "vous avez été",
                "ils ont été"
            ],
            "plus-que-parfait": [
                "j'avais été",
                "tu avais été",
                "il avait été",
                "nous avions été",
                "vous aviez été",
                "ils avaient été"
            ],
            "futur-antérieur": [
                "j'aurai été",
                "tu auras été",
                "il aura été",
                "nous aurons été",
                "vous aurez été",
                "ils auront été"
            ],
            "passé-antérieur": [
                "j'eus été",
                "tu eus été",
                "il eut été",
                "nous eûmes été",
                "vous eûtes été",
                "ils eurent été"
            ]
        },
        "conditionnel": {
            "présent": [
                "je serais",
                "tu serais",
                "il serait",
                "nous serions",
                "vous seriez",
                "ils seraient"
            ],
            "passé": [
                "j'aurais été",
                "tu aurais été",
                "il aurait été",
                "nous aurions été",
                "vous auriez été",
                "ils auraient été"
            ]
        },
        "subjonctif": {
            "présent": [
                "que je sois",
                "que tu sois",
                "qu'il soit",
                "que nous soyons",
                "que vous soyez",
                "qu'ils soient"
            ],
            "imparfait": [
                "que je fusse",
                "que tu fusses",
                "qu'il fût",
                "que nous fussions",
                "que vous fussiez",
                "qu'ils fussent"
            ],
            "passé": [
                "que j'aie été",
                "que tu aies été",
                "qu'il ait été",
                "que nous ayons été",
                "que vous ayez été",
                "qu'ils aient été"
            ],
            "plus-que-parfait": [
                "que j'eusse été",
                "que tu eusses été",
                "qu'il eût été",
                "que nous eussions été",
                "que vous eussiez été",
                "qu'ils eussent été"
            ]
        },
        "imperatif": {
            "imperatif-présent": [
                "sois",
                "soyons",
                "soyez"
            ],
            "imperatif-passé": [
                "aie été",
                "ayons été",
                "ayez été"
            ]
        },
        "participe": {
            "participe-présent": [
                "étant"
            ],
            "participe-passé": [
                "été"
            ]
        }
    }
}
```
