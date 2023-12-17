### Example: Spanish `ser` (to be)
```python
>>> from verbecc import Conjugator
>>> cg = Conjugator(lang='es') # If this is the first run, it will take a minute for the model to train, 
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
        "indicativo": {
            "presente": [
                "yo soy",
                "tú eres",
                "él es",
                "nosotros somos",
                "vosotros sois",
                "ellos son"
            ],
            "pretérito-imperfecto": [
                "yo era",
                "tú eras",
                "él era",
                "nosotros éramos",
                "vosotros erais",
                "ellos eran"
            ],
            "pretérito-perfecto-simple": [
                "yo fui",
                "tú fuiste",
                "él fue",
                "nosotros fuimos",
                "vosotros fuisteis",
                "ellos fueron"
            ],
            "futuro": [
                "yo seré",
                "tú serás",
                "él será",
                "nosotros seremos",
                "vosotros seréis",
                "ellos serán"
            ],
            "pretérito-perfecto-compuesto": [
                "yo he sido",
                "tú has sido",
                "él ha sido",
                "nosotros hemos sido",
                "vosotros habéis sido",
                "ellos han sido"
            ],
            "pretérito-pluscuamperfecto": [
                "yo había sido",
                "tú habías sido",
                "él había sido",
                "nosotros habíamos sido",
                "vosotros habíais sido",
                "ellos habían sido"
            ],
            "pretérito-anterior": [
                "yo hube sido",
                "tú hubiste sido",
                "él hubo sido",
                "nosotros hubimos sido",
                "vosotros hubisteis sido",
                "ellos hubieron sido"
            ],
            "futuro-perfecto": [
                "yo habré sido",
                "tú habrás sido",
                "él habrá sido",
                "nosotros habremos sido",
                "vosotros habréis sido",
                "ellos habrán sido"
            ]
        },
        "subjuntivo": {
            "presente": [
                "yo sea",
                "tú seas",
                "él sea",
                "nosotros seamos",
                "vosotros seáis",
                "ellos sean"
            ],
            "pretérito-imperfecto-1": [
                "yo fuera",
                "tú fueras",
                "él fuera",
                "nosotros fuéramos",
                "vosotros fuerais",
                "ellos fueran"
            ],
            "pretérito-imperfecto-2": [
                "yo fuese",
                "tú fueses",
                "él fuese",
                "nosotros fuésemos",
                "vosotros fueseis",
                "ellos fuesen"
            ],
            "futuro": [
                "yo fuere",
                "tú fueres",
                "él fuere",
                "nosotros fuéremos",
                "vosotros fuereis",
                "ellos fueren"
            ],
            "pretérito-perfecto": [
                "yo haya sido",
                "tú hayas sido",
                "él haya sido",
                "nosotros hayamos sido",
                "vosotros hayáis sido",
                "ellos hayan sido"
            ],
            "pretérito-pluscuamperfecto-1": [
                "yo hubiera sido",
                "tú hubieras sido",
                "él hubiera sido",
                "nosotros hubiéramos sido",
                "vosotros hubierais sido",
                "ellos hubieran sido"
            ],
            "pretérito-pluscuamperfecto-2": [
                "yo hubiese sido",
                "tú hubieses sido",
                "él hubiese sido",
                "nosotros hubiésemos sido",
                "vosotros hubieseis sido",
                "ellos hubiesen sido"
            ],
            "futuro-perfecto": [
                "yo hubiere sido",
                "tú hubieres sido",
                "él hubiere sido",
                "nosotros hubiéremos sido",
                "vosotros hubiereis sido",
                "ellos hubieren sido"
            ]
        },
        "imperativo": {
            "afirmativo": [
                "sé",
                "sea",
                "seamos",
                "sed",
                "sean"
            ],
            "negativo": [
                "no seas",
                "no sea",
                "no seamos",
                "no seáis",
                "no sean"
            ]
        },
        "condicional": {
            "presente": [
                "yo sería",
                "tú serías",
                "él sería",
                "nosotros seríamos",
                "vosotros seríais",
                "ellos serían"
            ],
            "perfecto": [
                "yo habría sido",
                "tú habrías sido",
                "él habría sido",
                "nosotros habríamos sido",
                "vosotros habríais sido",
                "ellos habrían sido"
            ]
        },
        "infinitivo": {
            "infinitivo": [
                "ser",
                "sido"
            ]
        },
        "gerundio": {
            "gerundio": [
                "siendo",
                "sido"
            ]
        },
        "participo": {
            "participo": [
                "sido"
            ]
        }
    }
}
```