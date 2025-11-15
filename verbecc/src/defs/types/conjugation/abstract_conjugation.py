from abc import ABC, abstractmethod
import json
from jsbeautifier import beautify

from verbecc.src.defs.constants import config
from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts


class AbstractConjugation:

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
