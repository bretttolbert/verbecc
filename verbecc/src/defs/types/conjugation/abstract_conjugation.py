from dataclasses import fields
from typing import cast, Optional
from abc import ABC, abstractmethod
import json
import yaml

from verbecc.src.utils.dict_utils import DictUtils
from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig
from verbecc.src.defs.types.config.json_opts import JSONOpts
from verbecc.src.utils.config.verbecc_config_util import VerbeccConfigUtil
from verbecc.src.utils.jsbeautifier_utils import JSBeautifier
from verbecc.src.utils.json_utils import JSONUtils
from verbecc.src.utils.yaml_utils import YAMLUtils
from verbecc.src.defs.types.conjugation.conjugation_data import ConjugationKeyPerson

config = VerbeccConfigUtil().load_config()


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

    def to_json(
        self,
        indent: Optional[int] = config.JSON_OPTS.indent,
        beautify: bool = config.JSBEAUTIFIER_ENABLE,
    ) -> str:
        """The data of this object as a JSON string,
        optionally pretty-formatted.
        :param indent: Passed json.dumps(). None=no whitespace. Overrides config.JSON_OPS.indent.
        :param beautify: Whether to pretty-format the JSON output using jsbeautifier. Overrides config.JSBEAUTIFIER_ENABLE.
        :return: JSON string
        """
        data = self.get_data()
        return JSONUtils.to_json(data, indent=indent, beautify=beautify)

    def __str__(self) -> str:
        return self.to_json()

    def to_yaml(self) -> str:
        """
        The data of this object as a YAML string.
        """
        # convert it to JSON and back to convert Python types (Gender, etc.) to strings.
        # TODO: Figure out how to do this with custom yaml.Dumper
        data = json.loads(self.to_json())

        # Cast Person from string to int, for cleaner representation in yaml
        # (keeping it as a string in JSON, since it looks more consistent since JSON has quotes
        # around all the string values, unlike YAML)
        # TODO: Figure out how to do this with custom yaml.Dumper

        data = DictUtils.cast_values_recursive(data, ConjugationKeyPerson, int)

        # TODO: If possiuble, figure out how to prevent YAML from putting quotes around the
        # French pronoun "on" ("on" is considered an "ambiguous value" in YAML, by default)
        #
        # > ambiguous values: Adhere to the YAML 1.2 specification by avoiding unquoted values
        #   that can be interpreted as other types (like certain boolean forms,
        #   e.g., yes, no, on, off from older YAML 1.1 specs).
        #   Sticking to lowercase true and false for booleans can also help.

        return YAMLUtils.to_yaml(data)

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
