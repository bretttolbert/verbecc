# Italiano

### Italian `essere` (to be)
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.it)
>>> print(cg.conjugate('essere'))
{
    "verb": {
        "infinitive": "essere",
        "predicted": false,
        "pred_score": 1.0,
        "template": ":essere",
        "translation_en": "",
        "stem": ""
    },
    "moods": {
        "indicativo": {
            "presente": [
                "io sono",
                "tu sei",
                "lui è",
                "noi siamo",
                "voi siete",
                "loro sono"
            ],
            "imperfetto": [
                "io ero",
                "tu eri",
                "lui era",
                "noi eravamo",
                "voi eravate",
                "loro erano"
            ],
            "passato-remoto": [
                "io fui",
                "tu fosti",
                "lui fu",
                "noi fummo",
                "voi foste",
                "loro furono"
            ],
            "futuro": [
                "io sarò",
                "tu sarai",
                "lui sarà",
                "noi saremo",
                "voi sarete",
                "loro saranno"
            ],
            "passato-prossimo": [
                "io sono stato",
                "tu sei stato",
                "lui è stato",
                "noi siamo stati",
                "voi siete stati",
                "loro sono stati"
            ],
            "trapassato-prossimo": [
                "io ero stato",
                "tu eri stato",
                "lui era stato",
                "noi eravamo stati",
                "voi eravate stati",
                "loro erano stati"
            ],
            "trapassato-remoto": [
                "io fui stato",
                "tu fosti stato",
                "lui fu stato",
                "noi fummo stati",
                "voi foste stati",
                "loro furono stati"
            ],
            "futuro-anteriore": [
                "io sarò stato",
                "tu sarai stato",
                "lui sarà stato",
                "noi saremo stati",
                "voi sarete stati",
                "loro saranno stati"
            ]
        },
        "congiuntivo": {
            "presente": [
                "che io sia",
                "che tu sia",
                "che lui sia",
                "che noi siamo",
                "che voi siate",
                "che loro siano"
            ],
            "imperfetto": [
                "che io fossi",
                "che tu fossi",
                "che lui fosse",
                "che noi fossimo",
                "che voi foste",
                "che loro fossero"
            ],
            "passato": [
                "che io sia stato",
                "che tu sia stato",
                "che lui sia stato",
                "che noi siamo stati",
                "che voi siate stati",
                "che loro siano stati"
            ],
            "trapassato": [
                "che io fossi stato",
                "che tu fossi stato",
                "che lui fosse stato",
                "che noi fossimo stati",
                "che voi foste stati",
                "che loro fossero stati"
            ]
        },
        "condizionale": {
            "presente": [
                "io sarei",
                "tu saresti",
                "lui sarebbe",
                "noi saremmo",
                "voi sareste",
                "loro sarebbero"
            ],
            "passato": [
                "io sarei stato",
                "tu saresti stato",
                "lui sarebbe stato",
                "noi saremmo stati",
                "voi sareste stati",
                "loro sarebbero stati"
            ]
        },
        "imperativo": {
            "affermativo": [
                "-",
                "sii",
                "sia",
                "siamo",
                "siate",
                "siano"
            ],
            "negativo": [
                "-",
                "ellere",
                "ella",
                "elliamo",
                "ellete",
                "ellano"
            ],
            "Negativo": [
                "-",
                "essere",
                "sia",
                "siamo",
                "siate",
                "siano"
            ]
        },
        "infinito": {
            "gerundio": [
                "essere",
                "stato",
                "essendo",
                "stato"
            ]
        },
        "participio": {
            "participio-presente": [
                "ente"
            ],
            "participio-passato": [
                "stato",
                "stata",
                "stati",
                "state"
            ]
        }
    }
}
```