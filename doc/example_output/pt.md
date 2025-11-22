# Português

### Example: Portuguese  `ser` (to be)
```python
>>> from verbecc import CompleteConjugator, LangCodeISO639_1 as Lang
>>> ccg = CompleteConjugator(Lang.pt) 
# If this is the first run, it will take a minute for the model to train, 
# but it should save the model .zip file and run fast subsequently
>>> cc = ccg.conjugate('ser')
>>> print(cc.to_json())
```
[(View Output JSON)](./example_json/pt-ser.json)
```python
>>> print(cc.to_yaml())
```
[(View Output YAML)](./example_yaml/pt-ser.yaml)
