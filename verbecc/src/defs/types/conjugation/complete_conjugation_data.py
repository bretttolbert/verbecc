from typing import Dict, Union

from verbecc.src.defs.types.conjugation.verb_info_data import VerbInfoData
from verbecc.src.defs.types.conjugation.moods_conjugation_data import (
    MoodsConjugationData,
)

CompleteConjugationData = Dict[str, Union[VerbInfoData, MoodsConjugationData]]
