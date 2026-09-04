# Python library for verb conjugation in French, Spanish, Catalan, Italian, Portuguese, and Romanian, enhanced by machine learning

- `verbecc` python library
[![Python Package Index Status](https://img.shields.io/pypi/v/verbecc.svg)](https://pypi.python.org/pypi/verbecc) 
[![PyPi Downloads Per Month](https://img.shields.io/pypi/dm/verbecc)](https://pypistats.org/packages/verbecc)
[![GitHub Actions CI status](https://github.com/bretttolbert/verbecc/actions/workflows/python-package.yml/badge.svg)](https://github.com/bretttolbert/verbecc/actions/workflows/python-package.yml?query=branch%3Amain)

##### [EN] Verbs completely conjugated: verb conjugations for French, Spanish, Portuguese, Italian, Romanian and Catalan, enhanced by machine learning
##### [CA] Verbs completament conjugats: conjugacions verbals per a francès, espanyol, portuguès, italià, romanès i català, millorades per l'aprenentatge automàtic
##### [ES] Verbos completamente conjugados: conjugaciones de verbos en francés, español, portugués, italiano, rumano y catalán, mejoradas por aprendizaje automático
##### [FR] Verbes complètement conjugués: conjugaisons des verbes français, espagnol, portugais, italien, roumain et catalan, à l'aide de l'apprentissage automatique
##### [IT] Verbi completamente coniugati: coniugazioni di verbi per francese, spagnolo, portoghese, italiano, rumeno e catalano, migliorate dall'apprendimento automatico
##### [PT] Verbos completamente conjugados: conjugações verbais para francês, espanhol, português, italiano, romeno e catalão, aprimoradas pelo aprendizado de máquina
##### [RO] Verbe complet conjugate: conjugări de verbe pentru franceză, spaniolă, portugheză, italiană, română și catalană, îmbunătățite de învățarea automată

## Contents

- [Quick Start](#quick-start)
- [Live Demo](#live-demo)
- [Example Output](#example-output)
- [What's new in Verbecc 2.0](#whats-new-in-verbecc-20)
- [Academic publications referencing Verbecc](#academic-publications-referencing-verbecc)
- [Typing - Parameter and Data Type Annotations](#typing---parameter-and-data-type-annotations)
- [Multi-Language Conjugation](#multi-language-conjugation)
- [Multi-Language Conjugation using English mood and tense names via `localization` module](#multi-language-conjugation-using-english-mood-and-tense-names-via-localization-module)
- [Credits / Collaborators](#credits--collaborators)

## Live Demo
- [Web GUI](https://verbe.cc)
- [HTTP API : /verbecc/conjugate/fr/manger](https://verbe.cc/verbecc/conjugate/fr/manger)

### Example Output

| Français / French | Català / Catalan | Español / Castellano / Spanish | Português / Portuguese | Italiano / Italian | Română / Romanian |
| ------ | ------ | ------- | -------- | --------- | ------ |
| [Français / French](./doc/example_output/fr.md) | [Català / Catalan](./doc/example_output/ca.md) | [Español / Castellano /Spanish](./doc/example_output/es.md) | [Português / Portuguese](./doc/example_output/pt.md) | [Italiano / Italian](./doc/example_output/it.md) | [Română / Romanian](./doc/example_output/ro.md) |
| [French `être` (to be)](./doc/example_output/fr.md#french-être-to-be) | [Catalan `ser` (to be)](./doc/example_output/ca.md#example-catalan-ser-to-be) | [Spanish `ser` (to be)](./doc/example_output/es.md#example-spanish-ser-to-be) | [Portuguese `ser` (to be)](./doc/example_output/pt.md#example-portuguese--ser-to-be) | [Italian `essere` (to be)](./doc/example_output/it.md#italian-essere-to-be) | [Romanian `fi` (to be)](./doc/example_output/ro.md#romanian-fi-to-be) |
| [French `se lever` (to lift oneself)](./doc/example_output/fr.md#french-se-lever-to-lift-oneself) |  |  |  |  |  |
| [French `ubériser` (to "uberize") (unknown verb conjugated with ML template prediction))](./doc/example_output/fr.md#ml-prediction-french-uberiser-to-uberize) |  |  |  |  |  |

## Features
* **Multilingual**
    * Conjugate verbs in six romance languages: French, Spanish, Portuguese, Italian, Romanian, Catalan
    * Includes Spanish voseo conjugation, with regional options in development.
    * Predict conjugation of unknown verbs with 99% accuracy using machine learning techniques
    * Conjugate thousands of known verbs without machine learning, using simple string transformations based on XML conjugation templates
* **Complete**
    * Includes both simple and compound conjugations (i.e. with helping/auxiliary verbs)
    * Includes alternate conjugations (for regional variations, e.g. Catalan vs. Valencian)
    * Includes inflections for all genders where applicable
    * Includes inlections for misc. pronouns such as the Spanish pronouns `usted` and `ustedes` and the French pronoun `on`.
* **Quality**
    * Fully type-annotated python library
        * Unit-tests require type-annotations on everything
    * Typed return data
    * Meticulously organized source tree
    * Has a plethora of unit-tests to ensure correctness of verb conjugations
    * Continuous Integration with GitHub Actions CI/CD pipeline
        * CI tests python 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14.
    * Dependencies: `scikit-learn`, `scipy`, `numpy`, `lxml`, `pyaml`, `jsbeautifier`, `importlib_resources`
* **Trusted**
    * Cited in [academic publications](#academic-publications-referencing-verbecc)


## Quick Start
```bash
git clone https://github.com/bretttolbert/verbecc.git
cd verbecc
pip install .
```

### Academic publications referencing verbecc

- [Segura Lores, Alba. (2025) Estudio de la variación del sujeto pronominal en la ciudad de Málaga: sociolingüística cognitiva de su producción y percepción. Universität Heidelberg. pp. 69. [DOI:10.11588/heidok.00037508]](https://nbn-resolving.org/urn:nbn:de:bsz:16-heidok-375088)


### What's new in Verbecc 2.0

| verbecc 1.x | verbecc 2.x |
| --- | --- |
| `lang='fr'` | `lang=Lang.fr` / `from verbecc import LangCodeISO639_1 as Lang` |
| `mood="indicatif"` | `mood=Moods.fr.Indicatif` / `from verbecc import Moods` |
| `tense="présent"` | `tense=Tenses.fr.Présent` / `from verbecc import Tenses` |
| `gender='f'` | `gender=Gender.f` / `from verbecc import Gender` |
| `person="1s"` | `person=Person.First, number=Number.Singular` / `from verbecc import Person, Number` | 
| Conjugations include masculine pronouns (default) or feminine but not both | All pronouns, including both masculine and feminine third-person pronouns are included | 
| `lang_specific_options` is a parameter of the `conjugate` method | `lang_specific_options` is a parameter of the `CompleteConjugator` class constructor |
| `gender` is a parameter of the `conjugate` method | there is no `gender` parameter, instead all possible gender inflections are returned |
| `alternate_options` is a parameter of the `conjugate` method | there is no `alternate_options` parameter, instead all possible conjugations, including alternates, are returned (use `c[0]` to get default conjugation, `c[1]` to get first alternate, etc.) |
| Spanish Conjugations include `tú` (default) or `vos` but not both | All pronouns, including both `tú` and `vos` are included | 
| Pronouns such as French `on` and Spanish `usted/ustedes` not included | French `on` and Spanish `usted/ustedes` pronouns are included |
| Array index is used to determine `Person`, i.e. `1s, 2s, 3s, 1p, 2p, 3p` | Each `Conjugation` object in the `TenseConjugation` has `Person`, `Number` and `Gender` values (any of which may be `None` if not-applicable) |
| Returned objects are primitive (`Dict`) data types | Returned wrapper objects are subclasses of `AbstractConjugation` (e.g. `CompleteConjugation`) with `get_data()` and `to_json()` methods |
| `Conjugator` returns `CompleteConjugationData` | `CompleteConjugator` returns wrapper type `CompleteConjugation`, `CompleteConjugation.get_data()` returns `CompleteConjugationData` |
| (no wrapper types) | Wrapper types hierarchy: `CompleteConjugation` > `MoodsConjugation` > `MoodConjugation` > `TenseConjugation` > `Conjugation` -> `conjugations: list[str]` |
| Primitive data types hierarchy: `Conjugation` > `MoodsConjugation` > `MoodConjugation` > `TenseConjugation` > `PersonConjugation` | Primitive data types hierarchy: `CompleteConjugationData` > `MoodsConjugationData` > `MoodConjugationData` > `TenseConjugationData` > `ConjugationData` -> `conjugations: list[str]` |
| `pred_score` was always included in the output | `pred_score` is only included in output if `predicted` is `true` |
| Only returned primitive Python data | `Conjugation` objects have both `.to_json()` and `.to_yaml()` methods | | 

### Typing - Parameter and Data Type Annotations

Originally `verbecc` used strings for most parameters. `verbecc` is now fully type-annotated but strings are still supported for backwards-compatibility and ease of use. This is accomplished using `StrEnum` for parameters and by defining a hierarchy of `typing` type definitions for the returned data objects (See [conjugation.py](./verbecc/src/defs/types/conjugation/conjugation.py)).

E.g.:

```python
>>> from verbecc import grammar_defines, localization, Moods, Tenses, Person, Number, Gender, LangCodeISO639_1 as Lang
>>> xmood = localization.xmood
>>> xtense = localization.xtense
>>> grammar_defines.SUPPORTED_LANGUAGES[Lang.fr]
'français'
>>> xtense(Lang.fr, Tenses.en.Present)
<TenseFr.Présent: 'présent'>
>>> xmood(Lang.fr, Moods.en.Subjunctive)
<MoodFr.Subjonctif: 'subjonctif'>
>>> Gender.f
<Gender.f: 'f'>
>>> Number.Singular
<Number.Singular: 's'>
>>> Person.First
<Person.First: '1'>
```

### Multi-Language Conjugation

```python
>>> from functools import partial
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang, grammar_defines, Moods, Tenses
>>> ccgs = {lang : CompleteConjugator(lang) for lang in grammar_defines.SUPPORTED_LANGUAGES}

>>> print([c[0] for c in ccgs[Lang.fr].conjugate('être')[Moods.fr.Indicatif][Tenses.fr.Présent]])
['je suis', 'tu es', 'il est', 'elle est', 'on est', 'nous sommes', 'vous êtes', 'ils sont', 'elles sont']
>>> print([c[0] for c in ccgs[Lang.es].conjugate('ser')[Moods.es.Indicativo][Tenses.es.Presente]])
['yo soy', 'tú eres', 'vos sos', 'él es', 'ella es', 'usted es', 'nosotros somos', 'vosotros sois', 'ellos son', 'ellas son', 'ustedes son']
>>> print([c[0] for c in ccgs[Lang.ca].conjugate('ser')[Moods.ca.Indicatiu][Tenses.ca.Present]])
['jo sóc', 'tu ets', 'ell és', 'ella és', 'nosaltres som', 'vosaltres sou', 'ells són', 'elles són']
>>> print([c[0] for c in ccgs[Lang.pt].conjugate('ser')[Moods.pt.Indicativo][Tenses.pt.Presente]])
['eu sou', 'tu és', 'ele é', 'ela é', 'nós somos', 'vós sois', 'eles são', 'elas são']
>>> print([c[0] for c in ccgs[Lang.it].conjugate('essere')[Moods.it.Indicativo][Tenses.it.Presente]])
['io sono', 'tu sei', 'lui è', 'lei è', 'noi siamo', 'voi siete', 'loro sono']
>>> print([c[0] for c in ccgs[Lang.it].conjugate('essere')[Moods.it.Indicativo][Tenses.it.Presente]])
['io sono', 'tu sei', 'lui è', 'lei è', 'noi siamo', 'voi siete', 'loro sono']
>>> print([c[0] for c in ccgs[Lang.ro].conjugate('fi')[Moods.ro.Indicativ][Tenses.ro.Prezent]])
['eu sunt', 'tu ești', 'el e', 'ea e', 'noi suntem', 'voi sunteţi', 'ei sunt', 'ele sunt']
```

### Multi-Language Conjugation using English mood and tense names via localization module

Observe below that strings may be still used for mood and tense, rather than the `Mood` and `Tense` (`StrEnum`) types. E.g. `indicative` is interchangeable with `Moods.en.Indicative` and `present` is interchangeable with `Tenses.en.Present`.

```python
>>> from verbecc import CompleteConjugator, localization
>>> def xconj(lang, infinitive, mood, tense):
    m = localization.xmood(lang, mood)
    t = localization.xtense(lang, tense)
    cc = CompleteConjugator(lang).conjugate(infinitive)
    return [c[0] for c in cc[m][t]]

>>> xconj('fr', 'etre', 'indicative', 'present')
['je suis', 'tu es', 'il est', 'elle est', 'on est', 'nous sommes', 'vous êtes', 'ils sont', 'elles sont']
>>> xconj('es', 'ser', 'indicative', 'present')
['yo soy', 'tú eres', 'vos sos', 'él es', 'ella es', 'usted es', 'nosotros somos', 'vosotros sois', 'ellos son', 'ellas son', 'ustedes son']
>>> xconj('pt', 'ser', 'indicative', 'present')
['eu sou', 'tu és', 'ele é', 'ela é', 'nós somos', 'vós sois', 'eles são', 'elas são']
>>> xconj('ca', 'ser', 'indicative', 'present')
['jo sóc', 'tu ets', 'ell és', 'ella és', 'nosaltres som', 'vosaltres sou', 'ells són', 'elles són']
>>> xconj('it', 'essere', 'indicative', 'present')
['io sono', 'tu sei', 'lui è', 'lei è', 'noi siamo', 'voi siete', 'loro sono']
>>> xconj('ro', 'fi', 'indicative', 'present')
['eu sunt', 'tu ești', 'el e', 'ea e', 'noi suntem', 'voi sunteţi', 'ei sunt', 'ele sunt']
```

### Credits / Collaborators
- Romanian bug fixes by [Peter Abolins](https://github.com/peterabolins), developer of [lexicro](https://lexicro.com/)
- Created with the help of [scikit-learn](https://scikit-learn.org), [lxml](https://github.com/lxml/lxml), [pytest](https://docs.pytest.org) and [python](https://www.python.org/)
- French verb conjugation template XML files derived from Pierre Sarrazin's C++ program [Verbiste](https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html). 
- Conjugation XML files (Verbiste format) for Spanish, Portuguese, Italian and Romanian and machine-learning conjugation template prediction for unknown verbs dervied from Sekou Diao's older project [mlconjug](https://github.com/SekouD/mlconjug) however they have a newer version out now: [mlconjug3](https://github.com/SekouDiaoNlp/mlconjug3/)
- Catalan verbs list imported from [catverbs](https://github.com/bpeel/catverbs)
