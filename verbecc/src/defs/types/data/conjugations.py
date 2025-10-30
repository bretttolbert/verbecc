from bisect import bisect_left
from typing import List, Iterator

from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.exceptions import TemplateNotFoundError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1


class Conjugations:
    def __init__(
        self, lang: LangCodeISO639_1, templates: List[ConjugationTemplate]
    ) -> None:
        self.lang = lang
        self._templates: List[ConjugationTemplate] = templates
        self._keys = [template.name for template in self._templates]

    def __len__(self) -> int:
        """
        Returns the number of verbs in the collection.
        """
        return len(self._templates)

    def __iter__(self) -> Iterator[ConjugationTemplate]:
        return iter(self._templates)

    def find_template(self, name: str) -> ConjugationTemplate:
        """Assumes templates are already sorted by name"""
        i = bisect_left(self._keys, name)
        if i != len(self._keys) and self._keys[i] == name:
            return self._templates[i]
        raise TemplateNotFoundError
