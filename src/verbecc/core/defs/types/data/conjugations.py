from bisect import bisect_left
from typing import Iterator

from verbecc.core.defs.types.data.element import Element
from verbecc.core.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.core.defs.types.exceptions import TemplateNotFoundError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1


class Conjugations(Element):
    def __init__(
        self, lang: LangCodeISO639_1, templates: list[ConjugationTemplate]
    ) -> None:
        self.lang = lang
        self._templates: list[ConjugationTemplate] = templates
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
        raise TemplateNotFoundError()
