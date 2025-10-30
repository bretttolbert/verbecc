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
from verbecc.src.defs.types.participle_inflection import ParticipleInflection
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
from verbecc.src.defs.types.data.verb import Verb
from verbecc.src.defs.types.data.verbs import Verbs
from verbecc.src.defs.types.data.mood_template import MoodTemplate
from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.data.conjugations import Conjugations
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
