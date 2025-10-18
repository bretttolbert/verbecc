import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class Language(StrEnum):
    """
    Enum of supported languages as ISO 639-1 codes
    """

    Català = "ca"
    Français = "fr"
    Español = "es"
    Italiano = "it"
    Português = "pt"
    Română = "ro"
