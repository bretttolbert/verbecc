from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.alternates_behavior import AlternatesBehavior
from verbecc.src.defs.types.data_types import (
    MoodsConjugation,
    MoodConjugation,
    TenseConjugation,
    PersonConjugation,
    VerbInfo,
    Conjugation,
)
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person, is_plural, is_singular
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.language import Lanugage
import verbecc.src.defs.constants.localization as localization
import verbecc.src.defs.constants.grammar_defines as grammar_defines
from verbecc.src.parsers.mood import Mood
from verbecc.src.parsers.verb import Verb
from verbecc.src.defs.types.exceptions import (
    ConjugatorError,
    ConjugationTemplateError,
    ConjugationsParserError,
    VerbNotFoundError,
    TemplateNotFoundError,
    InvalidLangError,
    InvalidMoodError,
    InvalidTenseError,
)
