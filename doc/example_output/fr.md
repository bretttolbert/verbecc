# Français

### French `être` (to be)
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.fr) 
# If this is the first run, it will take a minute for the model to train, 
# but it should save the model .zip file and run fast subsequently
>>> cc = ccg.conjugate("être")
>>> print(cc.to_json())
```
[(View Output JSON)](./example_json/fr-être.json)
```python
>>> print(cc.to_yaml())
```
[(View Output YAML)](./example_yaml/fr-être.yaml)


### French `se lever` (to lift oneself)
This verb is conjugated with the auxiliary verb `ềtre` so it must be inflected for gender and number.
That's why the output is nearly 1200 lines of JSON whereas `être` is just over 900 lines.
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.fr) 
# If this is the first run, it will take a minute for the model to train, 
# but it should save the model .zip file and run fast subsequently
>>> cc = ccg.conjugate("se lever")
>>> print(cc.to_json())
```
[(View Output JSON)](./example_json/fr-se-lever.json)
```python
>>> print(cc.to_yaml())
```
[(View Output YAML)](./example_yaml/fr-se-lever.yaml)

### ML Prediction French `uberiser` (to _Uberize_)

In this example, we will conjugate a verb that `verbecc` doesn't explicitly know. The conjugation will be predicted using a machine-learning model trained on `verbecc`'s French verb conjugation data XML models.

```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.fr)
>>> cc = ccg.conjugate('ubériser')
>>> print(cc.to_json())
```
[(View Output JSON)](./example_json/fr-ubériser.json)
```python
>>> print(cc.to_yaml())
```
[(View Output YAML)](./example_yaml/fr-ubériser.yaml)
