from typing import Union

from verbecc.core.defs.types.conjugation.verb_info_data import VerbInfoData
from verbecc.core.defs.types.conjugation.moods_conjugation_data import (
    MoodsConjugationData,
)

CompleteConjugationData = dict[str, Union[VerbInfoData, MoodsConjugationData]]
