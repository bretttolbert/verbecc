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
