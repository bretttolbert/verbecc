import sys
from enum import Enum

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.number import Number


class ParticipleInflection(Enum):
    MasculineSingular = (Gender.m, Number.Singular)
    MasculinePlural = (Gender.m, Number.Plural)
    FeminineSingular = (Gender.f, Number.Singular)
    FemininePlural = (Gender.f, Number.Plural)
