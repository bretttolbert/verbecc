from enum import Enum


class AlternatesBehavior(Enum):
    FirstOnly = (
        1  # PersonConjugation is a scalar (str), using the first (default) conjugation
    )
    SecondOnly = 2  # PersonConjugation is a scalar (str), using the alternate conjugation (if available)
    All = 3  # PersonConjugation is a list (str) of all possible conjugations, default first
