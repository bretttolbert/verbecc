from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.types.alternates_behavior import AlternatesBehavior
from verbecc.src.defs.types.conjugation import (
    MoodsConjugation,
    MoodConjugation,
    TenseConjugation,
    PersonConjugation,
    ConjugationInfo,
    Conjugation,
)
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.person import Person, is_plural, is_singular
from verbecc.src.defs.types.partiple_inflection import ParticipleInflection
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.mood import (
    Mood,
    MoodCa,
    MoodEs,
    MoodFr,
    MoodIt,
    MoodPt,
    MoodRo,
)
from verbecc.src.defs.types.tense import (
    Tense,
    TenseCa,
    TenseEs,
    TenseFr,
    TenseIt,
    TensePt,
    TenseRo,
)
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)
from verbecc.src.defs.types.lang.es.voseo_options import VoseoOptions
import verbecc.src.defs.constants.localization as localization
import verbecc.src.defs.constants.grammar_defines as grammar_defines
from verbecc.src.parsers.mood_template import MoodTemplate
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
