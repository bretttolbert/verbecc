import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


# This refers to grammatical person ('usted' is 3s despite being semantically 2p)
class Person(StrEnum):
    FirstPersonSingular = "1s"
    SecondPersonSingular = "2s"
    ThirdPersonSingular = "3s"
    FirstPersonPlural = "1p"
    SecondPersonPlural = "2p"
    ThirdPersonPlural = "3p"


def is_plural(p: Person) -> bool:
    return p in (
        Person.FirstPersonPlural,
        Person.SecondPersonPlural,
        Person.ThirdPersonPlural,
    )


def is_singular(p: Person) -> bool:
    return not is_plural(p)
