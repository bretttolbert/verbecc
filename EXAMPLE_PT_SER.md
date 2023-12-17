### Example: Portuguese  `ser` (to be)
```python
>>> from verbecc import Conjugator
>>> cg = Conjugator(lang='pt') # If this is the first run, it will take a minute for the model to train, 
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
                "eu sou",
                "tu és",
                "ele é",
                "nós somos",
                "vós sois",
                "eles são"
            ],
            "pretérito-imperfeito": [
                "eu era",
                "tu eras",
                "ele era",
                "nós éramos",
                "vós éreis",
                "eles eram"
            ],
            "pretérito-mais-que-perfeito": [
                "eu fora",
                "tu foras",
                "ele fora",
                "nós fôramos",
                "vós fôreis",
                "eles foram"
            ],
            "pretérito-perfeito": [
                "eu fui",
                "tu foste",
                "ele foi",
                "nós fomos",
                "vós fostes",
                "eles foram"
            ],
            "futuro-do-presente": [
                "eu serei",
                "tu serás",
                "ele será",
                "nós seremos",
                "vós sereis",
                "eles serão"
            ],
            "pretérito-perfeito-composto": [
                "eu tenho sido",
                "tu tens sido",
                "ele tem sido",
                "nós temos sido",
                "vós tendes sido",
                "eles têm sido"
            ],
            "pretérito-mais-que-perfeito-composto": [
                "eu tinha sido",
                "tu tinhas sido",
                "ele tinha sido",
                "nós tínhamos sido",
                "vós tínheis sido",
                "eles tinham sido"
            ],
            "pretérito-mais-que-perfeito-anterior": [
                "eu tivera sido",
                "tu tiveras sido",
                "ele tivera sido",
                "nós tivéramos sido",
                "vós tivéreis sido",
                "eles tiveram sido"
            ],
            "futuro-do-presente-composto": [
                "eu terei sido",
                "tu terás sido",
                "ele terá sido",
                "nós teremos sido",
                "vós tereis sido",
                "eles terão sido"
            ]
        },
        "condicional": {
            "futuro-do-pretérito": [
                "eu seria",
                "tu serias",
                "ele seria",
                "nós seríamos",
                "vós seríeis",
                "eles seriam"
            ],
            "futuro-do-pretérito-composto": [
                "eu teria sido",
                "tu terias sido",
                "ele teria sido",
                "nós teríamos sido",
                "vós teríeis sido",
                "eles teriam sido"
            ]
        },
        "subjuntivo": {
            "presente": [
                "que eu seja",
                "que tu sejas",
                "que ele seja",
                "que nós sejamos",
                "que vós sejais",
                "que eles sejam"
            ],
            "pretérito-imperfeito": [
                "se eu fosse",
                "se tu fosses",
                "se ele fosse",
                "se nós fôssemos",
                "se vós fôsseis",
                "se eles fossem"
            ],
            "futuro": [
                "quando eu for",
                "quando tu fores",
                "quando ele for",
                "quando nós formos",
                "quando vós fordes",
                "quando eles forem"
            ],
            "pretérito-perfeito": [
                "eu tenha sido",
                "tu tenhas sido",
                "ele tenha sido",
                "nós tenhamos sido",
                "vós tenhais sido",
                "eles tenham sido"
            ],
            "pretérito-mais-que-perfeito": [
                "eu tivesse sido",
                "tu tivesses sido",
                "ele tivesse sido",
                "nós tivéssemos sido",
                "vós tivésseis sido",
                "eles tivessem sido"
            ],
            "futuro-composto": [
                "eu tiver sido",
                "tu tiveres sido",
                "ele tiver sido",
                "nós tivermos sido",
                "vós tiverdes sido",
                "eles tiverem sido"
            ]
        },
        "infinitivo": {
            "infinitivo-pessoal-presente": [
                "por ser eu",
                "por seres tu",
                "por ser ele",
                "por sermos nós",
                "por serdes vós",
                "por serem eles"
            ],
            "infinitivo": [
                "ser",
                "sido"
            ],
            "infinitivo-pessoal-composto": [
                "ter sido",
                "teres sido",
                "ter sido",
                "termos sido",
                "terdes sido",
                "terem sido"
            ]
        },
        "imperativo": {
            "afirmativo": [
                "-",
                "sê tu",
                "seja você",
                "sejamos nós",
                "sede vós",
                "sejam vocês"
            ],
            "negativo": [
                "-",
                "não sejas tu",
                "não seja você",
                "não sejamos nós",
                "não sejais vós",
                "não sejam vocês"
            ]
        },
        "gerúndio": {
            "gerúndio": [
                "sendo",
                "sido"
            ]
        },
        "particípio": {
            "particípio": [
                "sido"
            ]
        }
    }
}
```