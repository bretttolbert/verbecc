from dataclasses import fields
from typing import cast, Optional
from abc import ABC, abstractmethod
import json

from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig
from verbecc.src.defs.types.config.json_opts import JSONOpts
from verbecc.src.utils.config_utils import ConfigUtils
from verbecc.src.utils.jsbeautifier_utils import JSBeautifier
from verbecc.src.utils.json_utils import JSONUtils

config = ConfigUtils.load_verbecc_config()


class AbstractConjugation(ABC):

    def __init__(self) -> None:
        self._parent: Optional[AbstractConjugation] = None

    def get_parent(self) -> Optional[object]:
        return self._parent

    def set_parent(self, value: object) -> None:
        if isinstance(value, AbstractConjugation):
            self._parent = cast(AbstractConjugation, value)
        else:
            raise TypeError()

    @abstractmethod
    def get_data(self) -> object:
        """The data of this object as primitive types (JSON-serializable)"""
        pass

    def __repr__(self) -> str:
        return str(self)

    def to_json(self, beautify: bool = config.JSBEAUTIFIER_ENABLE) -> str:
        """The data of this object as a JSON string,
        optionally pretty-formatted.
        :param beautify: Whether to pretty-format the JSON output
        :return: JSON string
        """
        return JSONUtils.to_json(self.get_data(), beautify=beautify)

    def __str__(self) -> str:
        return self.to_json()

    @abstractmethod
    def get_str_id(self) -> str:
        """
        Returns unique string identifier for this conjugation object

        For Conjugation, the most specific conjugation object, the format is:

        lang:verb:mood:tense:person:number:gender:pronoun

        E.g. "fr:parler:participe:participe-passé::s:f:"
        E.g. "fr:parler:participe:participe-passé::p:m:"
        E.g. "fr:parler:indicatif:présent:1:s::je"
        E.g. "fr:parler:indicatif:présent:3:s:f:elle"

        For TenseConjugation objects, on the other hand, the format is:
        E.g. "fr:parler:participe:participe-passé"
        E.g. "fr:parler:indicatif:présent"

        And so on...
        """
        pass
