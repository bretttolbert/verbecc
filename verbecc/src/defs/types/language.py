import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class Lanugage(StrEnum):
    Catalan = "ca"
    French = "fr"
    Spanish = "es"
    Italian = "it"
    Portuguese = "pt"
    Romanian = "ro"
