### Example: Catalan `ser` (to be)
```python
>>> from verbecc import Conjugator
>>> cg = Conjugator(lang='ca') # If this is the first run, it will take a minute for the model to train, 
                               # but it should save the model .zip file and run fast subsequently
>>> cg.conjugate('ser')
>>> printjson(cg.conjugate('ser'))
{
    "verb": {
        "infinitive": "ser",
        "predicted": false,
        "pred_score": 1.0,
        "template": ":ser",
        "translation_en": "",
        "stem": ""
    },
    "moods": {
        "indicatiu": {
            "present": [
                "jo sóc",
                "tu ets",
                "ell és",
                "nosaltres som",
                "vosaltres sou",
                "ells són"
            ],
            "imperfet": [
                "jo era",
                "tu eres",
                "ell era",
                "nosaltres érem",
                "vosaltres éreu",
                "ells eren"
            ],
            "passat-simple": [
                "jo fui",
                "tu fores",
                "ell fou",
                "nosaltres fórem",
                "vosaltres fóreu",
                "ells foren"
            ],
            "futur": [
                "jo seré",
                "tu seràs",
                "ell serà",
                "nosaltres serem",
                "vosaltres sereu",
                "ells seran"
            ]
        },
        "subjuntiu": {
            "present": [
                "jo sigui",
                "tu siguis",
                "ell sigui",
                "nosaltres siguem",
                "vosaltres sigueu",
                "ells siguin"
            ],
            "imperfet": [
                "jo fos",
                "tu fossis",
                "ell fos",
                "nosaltres fóssim",
                "vosaltres fóssiu",
                "ells fossin"
            ]
        },
        "imperatiu": {
            "imperatiu-present": [
                "sigues",
                "sigui",
                "siguem",
                "sigueu",
                "siguin"
            ]
        },
        "condicional": {
            "present": [
                "jo seria",
                "tu series",
                "ell seria",
                "nosaltres seríem",
                "vosaltres seríeu",
                "ells serien"
            ]
        },
        "infinitiu": {
            "infinitiu-present": [
                "ser",
                "ésser"
            ]
        },
        "gerundi": {
            "gerundi": [
                "sent",
                "essent"
            ]
        },
        "particip": {
            "particip": [
                "estat",
                "estada",
                "estats",
                "estades"
            ]
        }
    }
}
```