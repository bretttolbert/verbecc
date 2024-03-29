from typing import Dict, List

from verbecc import verb
from verbecc.exceptions import InvalidLangError
from verbecc import conjugation_template

from verbecc import (
    inflector_ca,
    inflector_es,
    inflector_fr,
    inflector_it,
    inflector_pt,
    inflector_ro,
)


SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ca": "català",
    "es": "español",
    "fr": "français",
    "it": "italiano",
    "pt": "português",
    "ro": "română",
}


class Conjugator:
    def __init__(self, lang: str):
        """
        :param lang: two-letter language code
        :type lang: str
        """
        if lang == "ca":
            self._inflector = inflector_ca.InflectorCa()
        elif lang == "es":
            self._inflector = inflector_es.InflectorEs()
        elif lang == "fr":
            self._inflector = inflector_fr.InflectorFr()
        elif lang == "it":
            self._inflector = inflector_it.InflectorIt()
        elif lang == "pt":
            self._inflector = inflector_pt.InflectorPt()
        elif lang == "ro":
            self._inflector = inflector_ro.InflectorRo()
        else:
            raise InvalidLangError

    def conjugate(
        self, infinitive: str, include_alternates: bool = False, conjugate_pronouns=True
    ):
        """
        :param include_alterates: if True, a list of one or more possible conjugations is returned
            if False, the default conjugation is returned as a scalar string
        :param conjugate_prouns: if True, verbecc will conjugate the pronoun together with
            its inflected form, e.g. for the French verb apprendre, for the first-person singular
            present tense you'd get "j'apprends" if True or "apprends" if False.

        E.g. for the Catalan verb "ser"
        include_alternates=False, conjugate_pronouns=True -> "jo seria"
        include_alternates=True, conjugate_pronouns=False -> ["seria", "fora"]
        """
        return self._inflector.conjugate(
            infinitive, include_alternates, conjugate_pronouns
        )

    def conjugate_mood(self, infinitive: str, mood_name: str) -> Dict[str, List[str]]:
        return self._inflector.conjugate_mood(infinitive, mood_name)

    def conjugate_mood_include_alternates(
        self, infinitive: str, mood_name: str
    ) -> Dict[str, List[List[str]]]:
        return self._inflector.conjugate_mood_include_alternates(
            infinitive, mood_name, conjugate_pronouns=True
        )

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood_name: str,
        tense_name: str,
        alternate: bool = False,
        gender: str = "m",
    ):
        return self._inflector.conjugate_mood_tense(
            infinitive, mood_name, tense_name, alternate, gender
        )

    def get_verbs(self) -> List[verb.Verb]:
        return self._inflector.get_verbs()

    def get_infinitives(self) -> List[str]:
        return self._inflector.get_infinitives()

    def get_templates(self) -> List[conjugation_template.ConjugationTemplate]:
        return self._inflector.get_templates()

    def get_template_names(self) -> List[str]:
        return self._inflector.get_template_names()

    def find_verb_by_infinitive(self, infinitive: str) -> verb.Verb:
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> conjugation_template.ConjugationTemplate:
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        return self._inflector.get_verbs_that_start_with(query, max_results)
