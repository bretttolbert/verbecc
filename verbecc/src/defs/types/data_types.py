from typing import Union, Dict, List

# PersonConjugation format depends on AlternatesBehavior
# With AlternatesBehavior.All, its a List[str]
# With AlternatesBehvioar.FirstOnly or SecondOnly, it's a str
PersonConjugation = Union[List[str], str]
TenseConjugation = List[PersonConjugation]
MoodConjugation = Dict[str, TenseConjugation]
MoodsConjugation = Dict[str, MoodConjugation]  # the "moods" section
VerbInfo = Dict[str, Union[str, bool, float]]  # the "verb" section
Conjugation = Dict[str, Union[VerbInfo, MoodsConjugation]]
