from typing import Callable, Tuple, cast
import numpy as np

from verbecc.core.defs.types.lang_code import LangCodeISO639_1

from verbecc.core.mlconjug.model import Model
from verbecc.core.mlconjug.model_utils import load_model, save_model
from verbecc.core.mlconjug.data_set import DataSet
from verbecc.core.mlconjug.mltypes import VerbTemplatePair
from verbecc.core.utils.logging_utils import LoggingUtils


class TemplatePredictor:
    def __init__(
        self, verb_template_pairs: list[VerbTemplatePair], lang: LangCodeISO639_1
    ) -> None:
        self._logger = LoggingUtils.get_logger(self.__class__.__name__)
        self.data_set = DataSet(verb_template_pairs)
        model = load_model(lang)
        if model:
            self._logger.info("Loaded existing model from zip file.")
        else:
            self._logger.info("Could not load existing model, training new model...")
            model = Model(lang=lang)
            model.train(self.data_set.train_input, self.data_set.train_labels)
            zip_filename = save_model(model)
            self._logger.info(
                "Model training complete. Model saved to %s.", zip_filename
            )
        self.model = model
        return

    def predict(self, verb: str) -> Tuple[str, float]:
        predict_results: list[np.int64] = self.model.predict([verb])
        if len(predict_results) == 0:
            raise Exception("Template prediction failed")
        prediction = predict_results[0]
        predict_proba_fn = cast(
            Callable[[list[str]], np.ndarray],
            getattr(self.model.pipeline, "predict_proba"),
        )
        predict_proba = predict_proba_fn([verb])
        prediction_score = predict_proba[0][prediction]
        template = self.data_set.templates[prediction]
        return (template, prediction_score)
