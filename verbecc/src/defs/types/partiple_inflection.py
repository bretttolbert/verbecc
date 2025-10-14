import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class ParticipleInflection(StrEnum):
    MasculineSingular = "ms"
    MasculinePlural = "mp"
    FeminineSingular = "fs"
    FemininePlural = "fp"
