from typing import cast, Optional
from abc import ABC, abstractmethod
import json
from jsbeautifier import beautify

from verbecc.src.defs.constants import config
from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts


class AbstractConjugation(ABC):

    def __init__(self):
        self._parent: Optional[AbstractConjugation] = None

    def get_parent(self) -> Optional[object]:
        return self._parent

    def set_parent(self, value: object):
        if isinstance(value, AbstractConjugation):
            self._parent = cast(AbstractConjugation, value)
        else:
            raise TypeError

    @abstractmethod
    def get_data(self) -> object:
        """The data of this object as primitive types (JSON-serializable)"""
        pass

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """The data of this object as a pretty-formatted JSON string"""
        pretty_json = json.dumps(
            self.get_data(),
            allow_nan=False,
            sort_keys=True,
            indent=4,
            ensure_ascii=config.JSON_OPT_ENSURE_ASCII,
        )
        if config.JSBEAUTIFIER_ENABLE:
            pretty_json = beautify(pretty_json, JSBeautifierOpts.get_opts())
        return pretty_json

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
