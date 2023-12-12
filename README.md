# Python library for verb conjugation in French, Spanish, Italian, Portuguese, Romanian and Catalan, enhanced by machine learning

- `verbecc` python library
[![Python Package Index Status](https://img.shields.io/pypi/v/verbecc.svg)](https://pypi.python.org/pypi/verbecc) 
[![PyPi Downloads Per Month](https://img.shields.io/pypi/dm/verbecc)](https://pypistats.org/packages/verbecc)
[![GitLab CI pipeline status](https://gitlab.com/bretttolbert/verbecc/badges/master/pipeline.svg)](https://gitlab.com/bretttolbert/verbecc/-/pipelines)
[![Code Coverage](https://codecov.io/gl/bretttolbert/verbecc/branch/master/graph/badge.svg)](https://codecov.io/gl/bretttolbert/verbecc)

###### Verbs completely conjugated: verb conjugations for French, Spanish, Portuguese, Italian, Romanian and Catalan, enhanced by machine learning
###### Verbes complètement conjugués: conjugaisons des verbes français, espagnol, portugais, italien, roumain et catalan, à l'aide de l'apprentissage automatique
###### Verbi completamente coniugati: coniugazioni di verbi per francese, spagnolo, portoghese, italiano, rumeno e catalano, migliorate dall'apprendimento automatico
###### Verbos completamente conjugados: conjugaciones de verbos en francés, español, portugués, italiano, rumano y catalán, mejoradas por aprendizaje automático
###### Verbs completament conjugats: conjugacions verbals per a francès, espanyol, portuguès, italià, romanès i català, millorades per l'aprenentatge automàtic
###### Verbos completamente conjugados: conjugações verbais para francês, espanhol, português, italiano, romeno e catalão, aprimoradas pelo aprendizado de máquina
###### Verbe complet conjugate: conjugări de verbe franceză, spaniolă, portugheză, italiană, română și catalană, utilizând învățarea prin mașină

https://github.com/bretttolbert/verbecc

#### Features
* Conjugate verbs in six romance languages: French, Spanish, Portuguese, Italian, Romanian, Catalan (limited-support)
* Uses machine learning techniques to predict conjugation of unknown verbs with 99% accurracy
* Includes both simple and compound conjugations
* Unit-tested
* Continuous integration with GitLab CI/CD pipeline
* Dependencies: `scikit-learn`, `lxml`

# verbecc

#### Quick Start
```bash
git clone https://github.com/bretttolbert/verbecc.git
cd verbecc
pip install .
```

## Usage
```python
>>> from verbecc import Conjugator
>>> cg = Conjugator(lang='fr')
>>> conjugation = cg.conjugate('manger')
>>> conjugation
{'verb': {'infinitive': 'manger', 'predicted': False, 'pred_score': 1.0, 'template': 'man:ger', 'translation_en': 'eat', 'stem': 'man'}, 'moods': {'infinitif': {'infinitif-présent': ['manger']}, 'indicatif': {'présent': ['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent'], 'imparfait': ['je mangeais', 'tu mangeais', 'il mangeait', 'nous mangions', 'vous mangiez', 'ils mangeaient'], 'futur-simple': ['je mangerai', 'tu mangeras', 'il mangera', 'nous mangerons', 'vous mangerez', 'ils mangeront'], 'passé-simple': ['je mangeai', 'tu mangeas', 'il mangea', 'nous mangeâmes', 'vous mangeâtes', 'ils mangèrent'], 'passé-composé': ["j'ai mangé", 'tu as mangé', 'il a mangé', 'nous avons mangé', 'vous avez mangé', 'ils ont mangé'], 'plus-que-parfait': ["j'avais mangé", 'tu avais mangé', 'il avait mangé', 'nous avions mangé', 'vous aviez mangé', 'ils avaient mangé'], 'futur-antérieur': ["j'aurai mangé", 'tu auras mangé', 'il aura mangé', 'nous aurons mangé', 'vous aurez mangé', 'ils auront mangé'], 'passé-antérieur': ["j'eus mangé", 'tu eus mangé', 'il eut mangé', 'nous eûmes mangé', 'vous eûtes mangé', 'ils eurent mangé']}, 'conditionnel': {'présent': ['je mangerais', 'tu mangerais', 'il mangerait', 'nous mangerions', 'vous mangeriez', 'ils mangeraient'], 'passé': ["j'aurais mangé", 'tu aurais mangé', 'il aurait mangé', 'nous aurions mangé', 'vous auriez mangé', 'ils auraient mangé']}, 'subjonctif': {'présent': ['que je mange', 'que tu manges', "qu'il mange", 'que nous mangions', 'que vous mangiez', "qu'ils mangent"], 'imparfait': ['que je mangeasse', 'que tu mangeasses', "qu'il mangeât", 'que nous mangeassions', 'que vous mangeassiez', "qu'ils mangeassent"], 'passé': ["que j'aie mangé", 'que tu aies mangé', "qu'il ait mangé", 'que nous ayons mangé', 'que vous ayez mangé', "qu'ils aient mangé"], 'plus-que-parfait': ["que j'eusse mangé", 'que tu eusses mangé', "qu'il eût mangé", 'que nous eussions mangé', 'que vous eussiez mangé', "qu'ils eussent mangé"]}, 'imperatif': {'imperatif-présent': ['mange', 'mangeons', 'mangez'], 'imperatif-passé': ['aie mangé', 'ayons mangé', 'ayez mangé']}, 'participe': {'participe-présent': ['mangeant'], 'participe-passé': ['mangé', 'mangés', 'mangée', 'mangées']}}}
>>> conjugation['moods']['indicatif']['présent']
['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent']
>>> conjugation['moods'].keys()
dict_keys(['infinitif', 'indicatif', 'conditionnel', 'subjonctif', 'imperatif', 'participe'])
>>> conjugation['moods']['indicatif'].keys()
dict_keys(['présent', 'imparfait', 'futur-simple', 'passé-simple', 'passé-composé', 'plus-que-parfait', 'futur-antérieur', 'passé-antérieur'])
>>> conjugation['moods']['subjonctif'].keys()
dict_keys(['présent', 'imparfait', 'passé', 'plus-que-parfait'])
>>> # Now let's conjugate a verb that verbecc doesn't explicitly know. 
>>> # In this case, the conjugation will be predicted using a machine-learning model.
>>> cg.conjugate('ubériser')
{'verb': {'infinitive': 'ubériser', 'predicted': True, 'pred_score': 0.9998728791090999, 'template': 'aim:er', 'translation_en': '', 'stem': 'ubéris'}, 'moods': {'infinitif': {'infinitif-présent': ['ubériser']}, 'indicatif': {'présent': ["j'ubérise", 'tu ubérises', 'il ubérise', 'nous ubérisons', 'vous ubérisez', 'ils ubérisent'], 'imparfait': ["j'ubérisais", 'tu ubérisais', 'il ubérisait', 'nous ubérisions', 'vous ubérisiez', 'ils ubérisaient'], 'futur-simple': ["j'ubériserai", 'tu ubériseras', 'il ubérisera', 'nous ubériserons', 'vous ubériserez', 'ils ubériseront'], 'passé-simple': ["j'ubérisai", 'tu ubérisas', 'il ubérisa', 'nous ubérisâmes', 'vous ubérisâtes', 'ils ubérisèrent'], 'passé-composé': ["j'ai ubérisé", 'tu as ubérisé', 'il a ubérisé', 'nous avons ubérisé', 'vous avez ubérisé', 'ils ont ubérisé'], 'plus-que-parfait': ["j'avais ubérisé", 'tu avais ubérisé', 'il avait ubérisé', 'nous avions ubérisé', 'vous aviez ubérisé', 'ils avaient ubérisé'], 'futur-antérieur': ["j'aurai ubérisé", 'tu auras ubérisé', 'il aura ubérisé', 'nous aurons ubérisé', 'vous aurez ubérisé', 'ils auront ubérisé'], 'passé-antérieur': ["j'eus ubérisé", 'tu eus ubérisé', 'il eut ubérisé', 'nous eûmes ubérisé', 'vous eûtes ubérisé', 'ils eurent ubérisé']}, 'conditionnel': {'présent': ["j'ubériserais", 'tu ubériserais', 'il ubériserait', 'nous ubériserions', 'vous ubériseriez', 'ils ubériseraient'], 'passé': ["j'aurais ubérisé", 'tu aurais ubérisé', 'il aurait ubérisé', 'nous aurions ubérisé', 'vous auriez ubérisé', 'ils auraient ubérisé']}, 'subjonctif': {'présent': ["que j'ubérise", 'que tu ubérises', "qu'il ubérise", 'que nous ubérisions', 'que vous ubérisiez', "qu'ils ubérisent"], 'imparfait': ["que j'ubérisasse", 'que tu ubérisasses', "qu'il ubérisât", 'que nous ubérisassions', 'que vous ubérisassiez', "qu'ils ubérisassent"], 'passé': ["que j'aie ubérisé", 'que tu aies ubérisé', "qu'il ait ubérisé", 'que nous ayons ubérisé', 'que vous ayez ubérisé', "qu'ils aient ubérisé"], 'plus-que-parfait': ["que j'eusse ubérisé", 'que tu eusses ubérisé', "qu'il eût ubérisé", 'que nous eussions ubérisé', 'que vous eussiez ubérisé', "qu'ils eussent ubérisé"]}, 'imperatif': {'imperatif-présent': ['ubérise', 'ubérisons', 'ubérisez'], 'imperatif-passé': ['aie ubérisé', 'ayons ubérisé', 'ayez ubérisé']}, 'participe': {'participe-présent': ['ubérisant'], 'participe-passé': ['ubérisé', 'ubérisés', 'ubérisée', 'ubérisées']}}}
```

#### Credits
- Created with the help of [scikit-learn](https://scikit-learn.org), [lxml](https://github.com/lxml/lxml), [pytest](https://docs.pytest.org) and [python](https://www.python.org/)
- French verb conjugation template XML files derived from [Verbiste](https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html). 
- Conjugation XML files for Spanish, Portuguese, Italian and Romanian and machine-learning conjugation template prediction for unknown verbs dervied from Sekou Diao's older project [mlconjug](https://github.com/SekouD/mlconjug) however they have a newer version out now: [mlconjug3](https://github.com/SekouDiaoNlp/mlconjug3/)
