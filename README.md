# Python library for verb conjugation in French, Spanish, Italian, Portuguese, Romanian and Catalan, enhanced by machine learning

- `verbecc` python library
[![Python Package Index Status](https://img.shields.io/pypi/v/verbecc.svg)](https://pypi.python.org/pypi/verbecc) 
[![PyPi Downloads Per Month](https://img.shields.io/pypi/dm/verbecc)](https://pypistats.org/packages/verbecc)
[![GitLab CI pipeline status](https://gitlab.com/bretttolbert/verbecc/badges/master/pipeline.svg)](https://gitlab.com/bretttolbert/verbecc/-/pipelines)
[![Code Coverage](https://codecov.io/gl/bretttolbert/verbecc/branch/master/graph/badge.svg)](https://codecov.io/gl/bretttolbert/verbecc)

##### [EN] Verbs completely conjugated: verb conjugations for French, Spanish, Portuguese, Italian, Romanian and Catalan, enhanced by machine learning
##### [CA] Verbs completament conjugats: conjugacions verbals per a francès, espanyol, portuguès, italià, romanès i català, millorades per l'aprenentatge automàtic
##### [ES] Verbos completamente conjugados: conjugaciones de verbos en francés, español, portugués, italiano, rumano y catalán, mejoradas por aprendizaje automático
##### [FR] Verbes complètement conjugués: conjugaisons des verbes français, espagnol, portugais, italien, roumain et catalan, à l'aide de l'apprentissage automatique
##### [IT] Verbi completamente coniugati: coniugazioni di verbi per francese, spagnolo, portoghese, italiano, rumeno e catalano, migliorate dall'apprendimento automatico
##### [PT] Verbos completamente conjugados: conjugações verbais para francês, espanhol, português, italiano, romeno e catalão, aprimoradas pelo aprendizado de máquina
##### [RO] Verbe complet conjugate: conjugări de verbe pentru franceză, spaniolă, portugheză, italiană, română și catalană, îmbunătățite de învățarea automată

### Live Demo
- [Web GUI](http://verbe.cc)
- [HTTP API : /verbecc/conjugate/fr/manger](http://verbe.cc/verbecc/conjugate/fr/manger)

### Features
* Conjugate verbs in six romance languages: French, Spanish, Portuguese, Italian, Romanian, Catalan
* Uses machine learning techniques to predict conjugation of unknown verbs with 99% accurracy
* Includes both simple and compound conjugations
* Unit-tested
* Continuous integration with GitLab CI/CD pipeline
* Dependencies: `scikit-learn`, `lxml`

### Quick Start
```bash
git clone https://github.com/bretttolbert/verbecc.git
cd verbecc
pip install .
```

### Examples

In the following examples, the following function will be used to make the output more readable:

```python
import json
def printjson(c):
    print(json.dumps(c, indent=4, ensure_ascii=False))
```

### Conjugation Example: French `manger` (to eat)
```python
>>> from verbecc import Conjugator
>>> cg = Conjugator(lang='fr') # If this is the first run, it will take a minute for the model to train, 
                               # but it should save the model .zip file and run fast subsequently
>>> cg.conjugate('manger')
{'verb': {'infinitive': 'manger', 'predicted': False, 'pred_score': 1.0, 'template': 'man:ger', 'translation_en': 'eat', 'stem': 'man'}, 'moods': {'infinitif': {'infinitif-présent': ['manger']}, 'indicatif': {'présent': ['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent'], 'imparfait': ['je mangeais', 'tu mangeais', 'il mangeait', 'nous mangions', 'vous mangiez', 'ils mangeaient'], 'futur-simple': ['je mangerai', 'tu mangeras', 'il mangera', 'nous mangerons', 'vous mangerez', 'ils mangeront'], 'passé-simple': ['je mangeai', 'tu mangeas', 'il mangea', 'nous mangeâmes', 'vous mangeâtes', 'ils mangèrent'], 'passé-composé': ["j'ai mangé", 'tu as mangé', 'il a mangé', 'nous avons mangé', 'vous avez mangé', 'ils ont mangé'], 'plus-que-parfait': ["j'avais mangé", 'tu avais mangé', 'il avait mangé', 'nous avions mangé', 'vous aviez mangé', 'ils avaient mangé'], 'futur-antérieur': ["j'aurai mangé", 'tu auras mangé', 'il aura mangé', 'nous aurons mangé', 'vous aurez mangé', 'ils auront mangé'], 'passé-antérieur': ["j'eus mangé", 'tu eus mangé', 'il eut mangé', 'nous eûmes mangé', 'vous eûtes mangé', 'ils eurent mangé']}, 'conditionnel': {'présent': ['je mangerais', 'tu mangerais', 'il mangerait', 'nous mangerions', 'vous mangeriez', 'ils mangeraient'], 'passé': ["j'aurais mangé", 'tu aurais mangé', 'il aurait mangé', 'nous aurions mangé', 'vous auriez mangé', 'ils auraient mangé']}, 'subjonctif': {'présent': ['que je mange', 'que tu manges', "qu'il mange", 'que nous mangions', 'que vous mangiez', "qu'ils mangent"], 'imparfait': ['que je mangeasse', 'que tu mangeasses', "qu'il mangeât", 'que nous mangeassions', 'que vous mangeassiez', "qu'ils mangeassent"], 'passé': ["que j'aie mangé", 'que tu aies mangé', "qu'il ait mangé", 'que nous ayons mangé', 'que vous ayez mangé', "qu'ils aient mangé"], 'plus-que-parfait': ["que j'eusse mangé", 'que tu eusses mangé', "qu'il eût mangé", 'que nous eussions mangé', 'que vous eussiez mangé', "qu'ils eussent mangé"]}, 'imperatif': {'imperatif-présent': ['mange', 'mangeons', 'mangez'], 'imperatif-passé': ['aie mangé', 'ayons mangé', 'ayez mangé']}, 'participe': {'participe-présent': ['mangeant'], 'participe-passé': ['mangé', 'mangés', 'mangée', 'mangées']}}}
>>> # ok now let's make it more readable
>>> printjson(cg.conjugate('manger'))
{
    "verb": {
        "infinitive": "manger",
        "predicted": false,
        "pred_score": 1.0,
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
        "indicatif": {
            "présent": [
                "je mange",
                "tu manges",
                "il mange",
                "nous mangeons",
                "vous mangez",
                "ils mangent"
            ],
            "imparfait": [
                "je mangeais",
                "tu mangeais",
                "il mangeait",
                "nous mangions",
                "vous mangiez",
                "ils mangeaient"
            ],
            "futur-simple": [
                "je mangerai",
                "tu mangeras",
                "il mangera",
                "nous mangerons",
                "vous mangerez",
                "ils mangeront"
            ],
            "passé-simple": [
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
            "plus-que-parfait": [
                "j'avais mangé",
                "tu avais mangé",
                "il avait mangé",
                "nous avions mangé",
                "vous aviez mangé",
                "ils avaient mangé"
            ],
            "futur-antérieur": [
                "j'aurai mangé",
                "tu auras mangé",
                "il aura mangé",
                "nous aurons mangé",
                "vous aurez mangé",
                "ils auront mangé"
            ],
            "passé-antérieur": [
                "j'eus mangé",
                "tu eus mangé",
                "il eut mangé",
                "nous eûmes mangé",
                "vous eûtes mangé",
                "ils eurent mangé"
            ]
        },
        "conditionnel": {
            "présent": [
                "je mangerais",
                "tu mangerais",
                "il mangerait",
                "nous mangerions",
                "vous mangeriez",
                "ils mangeraient"
            ],
            "passé": [
                "j'aurais mangé",
                "tu aurais mangé",
                "il aurait mangé",
                "nous aurions mangé",
                "vous auriez mangé",
                "ils auraient mangé"
            ]
        },
        "subjonctif": {
            "présent": [
                "que je mange",
                "que tu manges",
                "qu'il mange",
                "que nous mangions",
                "que vous mangiez",
                "qu'ils mangent"
            ],
            "imparfait": [
                "que je mangeasse",
                "que tu mangeasses",
                "qu'il mangeât",
                "que nous mangeassions",
                "que vous mangeassiez",
                "qu'ils mangeassent"
            ],
            "passé": [
                "que j'aie mangé",
                "que tu aies mangé",
                "qu'il ait mangé",
                "que nous ayons mangé",
                "que vous ayez mangé",
                "qu'ils aient mangé"
            ],
            "plus-que-parfait": [
                "que j'eusse mangé",
                "que tu eusses mangé",
                "qu'il eût mangé",
                "que nous eussions mangé",
                "que vous eussiez mangé",
                "qu'ils eussent mangé"
            ]
        },
        "imperatif": {
            "imperatif-présent": [
                "mange",
                "mangeons",
                "mangez"
            ],
            "imperatif-passé": [
                "aie mangé",
                "ayons mangé",
                "ayez mangé"
            ]
        },
        "participe": {
            "participe-présent": [
                "mangeant"
            ],
            "participe-passé": [
                "mangé",
                "mangés",
                "mangée",
                "mangées"
            ]
        }
    }
}
>>> c['moods']['indicatif']['présent']
['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent']
>>> c['moods'].keys()
dict_keys(['infinitif', 'indicatif', 'conditionnel', 'subjonctif', 'imperatif', 'participe'])
>>> c['moods']['indicatif'].keys()
dict_keys(['présent', 'imparfait', 'futur-simple', 'passé-simple', 'passé-composé', 'plus-que-parfait', 'futur-antérieur', 'passé-antérieur'])
>>> c['moods']['subjonctif'].keys()
dict_keys(['présent', 'imparfait', 'passé', 'plus-que-parfait'])
```

### ML Prediction Conjugation Example: French `uberiser` (to _Uberize_)

In this example, we will conjugate a verb that `verbecc` doesn't explicitly know. The conjugation will be predicted using a machine-learning model trained on `verbecc`'s French verb conjugation data XML models.

```python
>>> printjson(cg.conjugate('ubériser'))
{
    "verb": {
        "infinitive": "ubériser",
        "predicted": true,
        "pred_score": 0.9997949959188503,
        "template": "aim:er",
        "translation_en": "",
        "stem": "ubéris"
    },
    "moods": {
        "infinitif": {
            "infinitif-présent": [
                "ubériser"
            ]
        },
        "indicatif": {
            "présent": [
                "j'ubérise",
                "tu ubérises",
                "il ubérise",
                "nous ubérisons",
                "vous ubérisez",
                "ils ubérisent"
            ],
            "imparfait": [
                "j'ubérisais",
                "tu ubérisais",
                "il ubérisait",
                "nous ubérisions",
                "vous ubérisiez",
                "ils ubérisaient"
            ],
            "futur-simple": [
                "j'ubériserai",
                "tu ubériseras",
                "il ubérisera",
                "nous ubériserons",
                "vous ubériserez",
                "ils ubériseront"
            ],
            "passé-simple": [
                "j'ubérisai",
                "tu ubérisas",
                "il ubérisa",
                "nous ubérisâmes",
                "vous ubérisâtes",
                "ils ubérisèrent"
            ],
            "passé-composé": [
                "j'ai ubérisé",
                "tu as ubérisé",
                "il a ubérisé",
                "nous avons ubérisé",
                "vous avez ubérisé",
                "ils ont ubérisé"
            ],
            "plus-que-parfait": [
                "j'avais ubérisé",
                "tu avais ubérisé",
                "il avait ubérisé",
                "nous avions ubérisé",
                "vous aviez ubérisé",
                "ils avaient ubérisé"
            ],
            "futur-antérieur": [
                "j'aurai ubérisé",
                "tu auras ubérisé",
                "il aura ubérisé",
                "nous aurons ubérisé",
                "vous aurez ubérisé",
                "ils auront ubérisé"
            ],
            "passé-antérieur": [
                "j'eus ubérisé",
                "tu eus ubérisé",
                "il eut ubérisé",
                "nous eûmes ubérisé",
                "vous eûtes ubérisé",
                "ils eurent ubérisé"
            ]
        },
        "conditionnel": {
            "présent": [
                "j'ubériserais",
                "tu ubériserais",
                "il ubériserait",
                "nous ubériserions",
                "vous ubériseriez",
                "ils ubériseraient"
            ],
            "passé": [
                "j'aurais ubérisé",
                "tu aurais ubérisé",
                "il aurait ubérisé",
                "nous aurions ubérisé",
                "vous auriez ubérisé",
                "ils auraient ubérisé"
            ]
        },
        "subjonctif": {
            "présent": [
                "que j'ubérise",
                "que tu ubérises",
                "qu'il ubérise",
                "que nous ubérisions",
                "que vous ubérisiez",
                "qu'ils ubérisent"
            ],
            "imparfait": [
                "que j'ubérisasse",
                "que tu ubérisasses",
                "qu'il ubérisât",
                "que nous ubérisassions",
                "que vous ubérisassiez",
                "qu'ils ubérisassent"
            ],
            "passé": [
                "que j'aie ubérisé",
                "que tu aies ubérisé",
                "qu'il ait ubérisé",
                "que nous ayons ubérisé",
                "que vous ayez ubérisé",
                "qu'ils aient ubérisé"
            ],
            "plus-que-parfait": [
                "que j'eusse ubérisé",
                "que tu eusses ubérisé",
                "qu'il eût ubérisé",
                "que nous eussions ubérisé",
                "que vous eussiez ubérisé",
                "qu'ils eussent ubérisé"
            ]
        },
        "imperatif": {
            "imperatif-présent": [
                "ubérise",
                "ubérisons",
                "ubérisez"
            ],
            "imperatif-passé": [
                "aie ubérisé",
                "ayons ubérisé",
                "ayez ubérisé"
            ]
        },
        "participe": {
            "participe-présent": [
                "ubérisant"
            ],
            "participe-passé": [
                "ubérisé",
                "ubérisés",
                "ubérisée",
                "ubérisées"
            ]
        }
    }
}
```

### Example: Multi-Language Conjugation

```python
>>> from verbecc import Conjugator
>>> Conjugator('fr').conjugate('etre')['moods']['indicatif']['présent']
['je suis', 'tu es', 'il est', 'nous sommes', 'vous êtes', 'ils sont']
>>> Conjugator('es').conjugate('ser')['moods']['indicativo']['presente']
['yo soy', 'tú eres', 'él es', 'nosotros somos', 'vosotros sois', 'ellos son']
>>> Conjugator('pt').conjugate('ser')['moods']['indicativo']['presente']
['eu sou', 'tu és', 'ele é', 'nós somos', 'vós sois', 'eles são']
>>> Conjugator('ca').conjugate('ser')['moods']['indicatiu']['present']
['jo sóc', 'tu ets', 'ell és', 'nosaltres som', 'vosaltres sou', 'ells són']
>>> Conjugator('it').conjugate('essere')['moods']['indicativo']['presente']
['io sono', 'tu sei', 'lui è', 'noi siamo', 'voi siete', 'loro sono']
>>> Conjugator('ro').conjugate('fi')['moods']['indicativ']['prezent']
['eu sunt', 'tu ești', 'el e', 'noi suntem', 'voi sunteţi', 'ei sunt']
```

### Example: Multi-Language Conjugation using English mood and tense names via `localization` module

```python
>>> from verbecc import Conjugator
>>> from verbecc.localization import xmood, xtense
>>> def xconj(lang, infinitive, mood, tense):
...     return Conjugator(lang).conjugate(infinitive)['moods'][xmood(lang, mood)][xtense(lang, tense)]
... 
>>> xconj('fr', 'etre', 'indicative', 'present')
['je suis', 'tu es', 'il est', 'nous sommes', 'vous êtes', 'ils sont']
>>> xconj('es', 'ser', 'indicative', 'present')
['yo soy', 'tú eres', 'él es', 'nosotros somos', 'vosotros sois', 'ellos son']
>>> xconj('pt', 'ser', 'indicative', 'present')
['eu sou', 'tu és', 'ele é', 'nós somos', 'vós sois', 'eles são']
>>> xconj('ca', 'ser', 'indicative', 'present')
['jo sóc', 'tu ets', 'ell és', 'nosaltres som', 'vosaltres sou', 'ells són']
>>> xconj('it', 'essere', 'indicative', 'present')
['io sono', 'tu sei', 'lui è', 'noi siamo', 'voi siete', 'loro sono']
>>> xconj('ro', 'fi', 'indicative', 'present')
['eu sunt', 'tu ești', 'el e', 'noi suntem', 'voi sunteţi', 'ei sunt']
```


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

### Conjugation Example: Italian `essere` (to be)
```python
>>> cg = Conjugator(lang='it')
>>> printjson(cg.conjugate('essere'))
>>> printjson(cg.conjugate('essere'))
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
                "io ho ente/essente",
                "tu hai ente/essente",
                "lui ha ente/essente",
                "noi abbiamo ente/essente",
                "voi avete ente/essente",
                "loro hanno ente/essente"
            ],
            "trapassato-prossimo": [
                "io avevo ente/essente",
                "tu avevi ente/essente",
                "lui aveva ente/essente",
                "noi avevamo ente/essente",
                "voi avevate ente/essente",
                "loro avevano ente/essente"
            ],
            "trapassato-remoto": [
                "io ebbi ente/essente",
                "tu avesti ente/essente",
                "lui ebbe ente/essente",
                "noi avemmo ente/essente",
                "voi aveste ente/essente",
                "loro ebbero ente/essente"
            ],
            "futuro-anteriore": [
                "io avrò ente/essente",
                "tu avrai ente/essente",
                "lui avrà ente/essente",
                "noi avremo ente/essente",
                "voi avrete ente/essente",
                "loro avranno ente/essente"
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
                "che io abbia ente/essente",
                "che tu abbia ente/essente",
                "che lui abbia ente/essente",
                "che noi abbiamo ente/essente",
                "che voi abbiate ente/essente",
                "che loro abbiano ente/essente"
            ],
            "trapassato": [
                "che io avessi ente/essente",
                "che tu avessi ente/essente",
                "che lui avesse ente/essente",
                "che noi avessimo ente/essente",
                "che voi aveste ente/essente",
                "che loro avessero ente/essente"
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
                "io avrei ente/essente",
                "tu avresti ente/essente",
                "lui avrebbe ente/essente",
                "noi avremmo ente/essente",
                "voi avreste ente/essente",
                "loro avrebbero ente/essente"
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
            "participio": [
                "ente/essente",
                "stato",
                "stata",
                "stati",
                "state"
            ]
        }
    }
}
```

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

### Conjugation Example: Romanian `fi` (to be)
```python
>>> cg = Conjugator(lang='ro')
>>> printjson(cg.conjugate('fi'))
{
    "verb": {
        "infinitive": "fi",
        "predicted": false,
        "pred_score": 1.0,
        "template": ":fi",
        "translation_en": "",
        "stem": ""
    },
    "moods": {
        "indicativ": {
            "prezent": [
                "eu sunt",
                "tu ești",
                "el e",
                "noi suntem",
                "voi sunteţi",
                "ei sunt"
            ],
            "imperfect": [
                "eu eram",
                "tu erai",
                "el era",
                "noi eram",
                "voi eraţi",
                "ei erau"
            ],
            "perfect-simplu": [
                "eu fui",
                "tu fuși",
                "el fu",
                "noi furăm",
                "voi furăţi",
                "ei fură"
            ],
            "mai-mult-ca-perfect": [
                "eu fusesem",
                "tu fuseseși",
                "el fusese",
                "noi fuseserăm",
                "voi fuseserăţi",
                "ei fuseseră"
            ],
            "perfect-compus": [
                "eu am fost",
                "tu ai fost",
                "el a fost",
                "noi am fost",
                "voi aţi fost",
                "ei au fost"
            ],
            "viitor-1": [
                "eu voi fi",
                "tu vei fi",
                "el va fi",
                "noi vom fi",
                "voi veţi fi",
                "ei vor fi"
            ],
            "viitor-2": [
                "eu voi fi fost",
                "tu vei fi fost",
                "el va fi fost",
                "noi vom fi fost",
                "voi veţi fi fost",
                "ei vor fi fost"
            ],
            "viitor-1-popular": [
                "eu o să fiu",
                "tu o să fii",
                "el o să fie",
                "noi o să fim",
                "voi o să fiţi",
                "ei o să fie"
            ],
            "viitor-2-popular": [
                "eu am să fi fost",
                "tu ai să fi fost",
                "el are să fi fost",
                "noi avem să fi fost",
                "voi aveţi să fi fost",
                "ei au să fi fost"
            ]
        },
        "conjunctiv": {
            "prezent": [
                "eu să fiu",
                "tu să fii",
                "el să fie",
                "noi să fim",
                "voi să fiţi",
                "ei să fie"
            ],
            "perfect": [
                "eu să fi fost",
                "tu să fi fost",
                "el să fi fost",
                "noi să fi fost",
                "voi să fi fost",
                "ei să fi fost"
            ]
        },
        "infinitiv": {
            "afirmativ": [
                "fi"
            ]
        },
        "imperativ": {
            "imperativ": [
                "fii",
                "fiţi"
            ],
            "negativ": [
                "nu fi",
                "nu fiţi"
            ]
        },
        "gerunziu": {
            "gerunziu": [
                "fiind"
            ]
        },
        "participiu": {
            "participiu": [
                "fost"
            ]
        }
    }
}
```

### Credits
- Created with the help of [scikit-learn](https://scikit-learn.org), [lxml](https://github.com/lxml/lxml), [pytest](https://docs.pytest.org) and [python](https://www.python.org/)
- French verb conjugation template XML files derived from Pierre Sarrazin's C++ program [Verbiste](https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html). 
- Conjugation XML files (Verbiste format) for Spanish, Portuguese, Italian and Romanian and machine-learning conjugation template prediction for unknown verbs dervied from Sekou Diao's older project [mlconjug](https://github.com/SekouD/mlconjug) however they have a newer version out now: [mlconjug3](https://github.com/SekouDiaoNlp/mlconjug3/)
- Catalan verbs list imported from [catverbs](https://github.com/bpeel/catverbs)
