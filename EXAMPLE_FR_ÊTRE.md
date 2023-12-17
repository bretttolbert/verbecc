### Conjugation Example: French `être` (to be)
```python
>>> cg = Conjugator(lang='fr')
# Observe that it finds and conjugates `être` even though we input `etre`
>>> printjson(cg.conjugate('etre'))
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