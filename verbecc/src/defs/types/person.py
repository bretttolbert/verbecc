import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


# Refers to grammatical person (i.e. 'usted' is third-person singular,
#   despite being semantically second-person plural)
class Person(StrEnum):
    First = "1"
    Second = "2"
    Third = "3"
