import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class LangCodeISO639_1(StrEnum):
    """
    Enum of supported languages as two-letter ISO 639-1 codes
    """

    ca = "ca"
    fr = "fr"
    es = "es"
    en = "en"
    it = "it"
    pt = "pt"
    ro = "ro"
