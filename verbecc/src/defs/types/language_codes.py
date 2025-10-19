import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class LangISOCode639_1(StrEnum):
    """
    Enum of supported languages as two-letter ISO 639-1 codes
    """

    Català = "ca"
    Français = "fr"
    Español = "es"
    English = "en"
    Italiano = "it"
    Português = "pt"
    Română = "ro"
