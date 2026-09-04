from bisect import bisect_left
from typing import Iterator, List

from verbecc.core.utils.logging_utils import LoggingUtils
from verbecc.core.defs.types.data.verb import Verb
from verbecc.core.defs.types.exceptions import VerbNotFoundError
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.mlconjug.predictor import TemplatePredictor
from verbecc.core.utils import string_utils
from verbecc.core.utils.config.verbecc_config_util import VerbeccConfigUtil

config = VerbeccConfigUtil().load_config()


class Verbs:
    def __init__(self, lang: LangCodeISO639_1, verbs: list[Verb]) -> None:
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)
        self.lang = lang
        self._verbs = verbs
        self._verbs_no_accents = sorted(
            self._verbs, key=lambda v: v.infinitive_no_accents
        )
        self.infinitives = [v.infinitive for v in verbs]

        self.infinitives_no_accents = [
            v.infinitive_no_accents for v in self._verbs_no_accents
        ]
        self.template_predictor = None
        self._logger.info("loaded verbecc config: %s", config)
        if config.ENABLE_ML_PREDICTION:
            self.template_predictor = TemplatePredictor(
                [(v.infinitive, v.template) for v in verbs], self.lang
            )

    def __len__(self) -> int:
        """
        Returns the number of verbs in the collection.
        """
        return len(self._verbs)

    def __iter__(self) -> Iterator[Verb]:
        return iter(self._verbs)

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        """First try to find with accents, e.g. if infinitive is 'Abañar',
        search for 'abañar' and not 'abanar'.
        If not found then try searching with accents stripped.
        If all else fails, use machine-learning magic to predict
        which conjugation template should be used.
        """
        query = infinitive.lower()
        i = bisect_left(self.infinitives, query)
        if i != len(self.infinitives) and self.infinitives[i] == query:
            return self._verbs[i]
        query = string_utils.strip_accents(infinitive.lower())

        i = bisect_left(self.infinitives_no_accents, query)
        if (
            i != len(self.infinitives_no_accents)
            and self.infinitives_no_accents[i] == query
        ):
            return self._verbs_no_accents[i]
        if config.ENABLE_ML_PREDICTION and self.template_predictor is not None:
            template, pred_score = self.template_predictor.predict(query)
            ret = Verb(infinitive.lower(), template, translation_en="")
            ret.predicted = True
            ret.pred_score = pred_score
            return ret
        else:
            raise VerbNotFoundError()

    def get_verbs_that_start_with(self, pre: str, max_results: int = 10) -> list[str]:
        ret: list[str] = []
        pre_no_accents = string_utils.strip_accents(pre.lower())
        for verb in self._verbs:
            if verb.infinitive_no_accents.startswith(pre_no_accents):
                ret.append(verb.infinitive)
                if len(ret) >= max_results:
                    break
        return ret
