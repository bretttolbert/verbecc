from typing import Dict

from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.conjugation.tense_conjugation_data import (
    TenseConjugationData,
)

MoodConjugationData = Dict[Tense, TenseConjugationData]
