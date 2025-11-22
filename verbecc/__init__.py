from verbecc.src.conjugator.complete_conjugator import CompleteConjugator
from verbecc.src.conjugator.mood_conjugator import MoodConjugator
from verbecc.src.conjugator.tense_conjugator import TenseConjugator
from verbecc.src.defs.constants import grammar_defines
from verbecc.src.defs.constants.grammar_defines import SUPPORTED_LANGUAGES
from verbecc.src.defs.constants import localization
from verbecc.src.defs.types.config.verbecc_config import VerbeccConfig
from verbecc.src.defs.types.config.jsbeautifier_opts import JSBeautifierOpts
from verbecc.src.utils.config.verbecc_config_util import VerbeccConfigUtil
from verbecc.src.utils.logging_utils import LoggingUtils
from verbecc.src.defs.types.conjugation import CompleteConjugation
from verbecc.src.defs.types.conjugation.complete_conjugation import (
    CompleteConjugationData,
)
from verbecc.src.defs.types.conjugation.conjugation import Conjugation
from verbecc.src.defs.types.conjugation.conjugation_data import ConjugationData
from verbecc.src.defs.types.exceptions.conjugations_parser_error import (
    ConjugationsParserError,
)
from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.exceptions.conjugation_template_error import (
    ConjugationTemplateError,
)
from verbecc.src.defs.types.exceptions.conjugator_error import ConjugatorError
from verbecc.src.defs.types.data.element import Element
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.exceptions.invalid_lang_error import InvalidLangError
from verbecc.src.defs.types.exceptions.invalid_mood_error import InvalidMoodError
from verbecc.src.defs.types.exceptions.invalid_tense_error import InvalidTenseError
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang_specific_options.lang.es.lang_specific_options_es import (
    LangSpecificOptionsEs,
)
from verbecc.src.defs.types.mood.mood import Mood
from verbecc.src.defs.types.mood.lang.mood_ca import MoodCa
from verbecc.src.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.src.defs.types.conjugation.mood_conjugation_data import MoodConjugationData
from verbecc.src.defs.types.mood.lang.mood_es import MoodEs
from verbecc.src.defs.types.mood.lang.mood_fr import MoodFr
from verbecc.src.defs.types.mood.lang.mood_it import MoodIt
from verbecc.src.defs.types.mood.lang.mood_pt import MoodPt
from verbecc.src.defs.types.mood.lang.mood_ro import MoodRo
from verbecc.src.defs.types.mood.moods import Moods
from verbecc.src.defs.types.mood.mood_factory import MoodFactory
from verbecc.src.defs.types.conjugation.moods_conjugation import MoodsConjugation
from verbecc.src.defs.types.conjugation.moods_conjugation_data import (
    MoodsConjugationData,
)
from verbecc.src.defs.types.data.mood_template import MoodTemplate
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.exceptions.template_not_found_error import (
    TemplateNotFoundError,
)
from verbecc.src.defs.types.tense.tense import Tense
from verbecc.src.defs.types.tense.lang.tense_ca import TenseCa
from verbecc.src.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.src.defs.types.conjugation.tense_conjugation_data import (
    TenseConjugationData,
)
from verbecc.src.defs.types.tense.lang.tense_es import TenseEs
from verbecc.src.defs.types.tense.lang.tense_fr import TenseFr
from verbecc.src.defs.types.tense.lang.tense_it import TenseIt
from verbecc.src.defs.types.tense.lang.tense_pt import TensePt
from verbecc.src.defs.types.tense.lang.tense_ro import TenseRo
from verbecc.src.defs.types.tense.tenses import Tenses
from verbecc.src.defs.types.tense.tense_factory import TenseFactory
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.data.verb import Verb
from verbecc.src.defs.types.conjugation.verb_info import VerbInfo
from verbecc.src.defs.types.conjugation.verb_info_data import VerbInfoData
from verbecc.src.defs.types.exceptions.verb_not_found_error import VerbNotFoundError
from verbecc.src.defs.types.data.verbs import Verbs
from verbecc.src.defs.types.lang_specific_options.lang.es.voseo_options import (
    VoseoOptions,
)
from verbecc.src.defs.types.pronoun.pronoun import Pronoun
from verbecc.src.defs.types.pronoun.pronouns import Pronouns
from verbecc.src.defs.types.pronoun.pronoun_factory import PronounFactory
from verbecc.src.defs.types.pronoun.lang.pronoun_ca import PronounCa
from verbecc.src.defs.types.pronoun.lang.pronoun_en import PronounEn
from verbecc.src.defs.types.pronoun.lang.pronoun_es import PronounEs
from verbecc.src.defs.types.pronoun.lang.pronoun_fr import PronounFr
from verbecc.src.defs.types.pronoun.lang.pronoun_it import PronounIt
from verbecc.src.defs.types.pronoun.lang.pronoun_pt import PronounPt
from verbecc.src.defs.types.pronoun.lang.pronoun_ro import PronounRo
