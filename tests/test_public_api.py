from verbecc import CompleteConjugator
from verbecc.core import CompleteConjugator as CoreCompleteConjugator
from verbecc.core.conjugator import CompleteConjugator as PackageCompleteConjugator
from verbecc.core.conjugator.complete_conjugator import CompleteConjugator as ImplementationCompleteConjugator
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang


def test_complete_conjugator_re_exports() -> None:
    assert CompleteConjugator is CoreCompleteConjugator
    assert CompleteConjugator is PackageCompleteConjugator
    assert CompleteConjugator is ImplementationCompleteConjugator


def test_public_complete_conjugator_conjugates() -> None:
    conjugator = CompleteConjugator(lang=Lang.fr)
    assert conjugator.conjugate("parler")
