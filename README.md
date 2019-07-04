# verbecc

### Verbes, complètement conjugués - conjugueur français

### Verbs, completely conjugated - French conjugator

https://github.com/bretttolbert/verbecc

[![pipeline status](https://gitlab.com/bretttolbert/verbecc/badges/master/pipeline.svg)](https://gitlab.com/bretttolbert/verbecc/pipelines)

# verbecc-svc

### verbecc-svc Microservice Python avec un API REST pour la conjugaison des verbes français

### verbecc-svc Python microservice with REST API for conjugation of French verbs

https://github.com/bretttolbert/verbecc-svc

[![pipeline status](https://gitlab.com/bretttolbert/verb-conjugate-fr/badges/master/pipeline.svg)](https://gitlab.com/bretttolbert/verb-conjugate-fr/pipelines)

# verbecc-web

### Une interface web pour verbecc-svc

### Web front-end for verbecc-svc

https://github.com/bretttolbert/verbecc-web

http://verbe.cc

Features
* Over 7,000 verbs supported
* Unit tested
* Continuous Integration and Deployment with GitLab CI/CD

## Installation

```
pip install verbecc
```

## Usage
```
>>> from verbecc import conjugator
>>> cg = conjugator.Conjugator()
>>> conjugation = cg.conjugate('manger')
>>> conjugation
{'verb': {'infinitive': 'manger', 'template': 'man:ger', 'translation_en': 'eat', 'stem': 'man'}, 'moods': {'infinitive': {'infinitive-present': ['manger']}, 'indicative': {'present': ['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent'], 'imperfect': ['je mangeais', 'tu mangeais', 'il mangeait', 'nous mangions', 'vous mangiez', 'ils mangeaient'], 'future': ['je mangerai', 'tu mangeras', 'il mangera', 'nous mangerons', 'vous mangerez', 'ils mangeront'], 'simple-past': ['je mangeai', 'tu mangeas', 'il mangea', 'nous mangeâmes', 'vous mangeâtes', 'ils mangèrent'], 'passé-composé': ["j'ai mangé", 'tu as mangé', 'il a mangé', 'nous avons mangé', 'vous avez mangé', 'ils ont mangé'], 'pluperfect': ["j'avais mangé", 'tu avais mangé', 'il avait mangé', 'nous avions mangé', 'vous aviez mangé', 'ils avaient mangé'], 'future-perfect': ["j'aurai mangé", 'tu auras mangé', 'il aura mangé', 'nous aurons mangé', 'vous aurez mangé', 'ils auront mangé'], 'anterior-past': ["j'eus mangé", 'tu eus mangé', 'il eut mangé', 'nous eûmes mangé', 'vous eûtes mangé', 'ils eurent mangé']}, 'conditional': {'present': ['je mangerais', 'tu mangerais', 'il mangerait', 'nous mangerions', 'vous mangeriez', 'ils mangeraient'], 'past': ["j'aurais mangé", 'tu aurais mangé', 'il aurait mangé', 'nous aurions mangé', 'vous auriez mangé', 'ils auraient mangé']}, 'subjunctive': {'present': ['que je mange', 'que tu manges', "qu'il mange", 'que nous mangions', 'que vous mangiez', "qu'ils mangent"], 'imperfect': ['que je mangeasse', 'que tu mangeasses', "qu'il mangeât", 'que nous mangeassions', 'que vous mangeassiez', "qu'ils mangeassent"], 'past': ["que j'aie mangé", 'que tu aies mangé', "qu'il ait mangé", 'que nous ayons mangé', 'que vous ayez mangé', "qu'ils aient mangé"], 'pluperfect': ["que j'eusse mangé", 'que tu eusses mangé', "qu'il eût mangé", 'que nous eussions mangé', 'que vous eussiez mangé', "qu'ils eussent mangé"]}, 'imperative': {'imperative-present': ['mange', 'mangeons', 'mangez'], 'imperative-past': ['aie mangé', 'ayons mangé', 'ayez mangé']}, 'participle': {'present-participle': ['mangeant'], 'past-participle': ['mangé', 'mangés', 'mangée', 'mangées']}}}
>>> conjugation['moods']['indicative']['present']
['je mange', 'tu manges', 'il mange', 'nous mangeons', 'vous mangez', 'ils mangent']
>>> conjugation['moods'].keys()
dict_keys(['infinitive', 'indicative', 'conditional', 'subjunctive', 'imperative', 'participle'])
```