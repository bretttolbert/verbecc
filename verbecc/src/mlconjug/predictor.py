from typing import List, Tuple
import numpy as np

from verbecc.src.defs.types.lang_code import LangCodeISO639_1

from verbecc.src.mlconjug.model import Model
from verbecc.src.mlconjug.model_utils import load_model, save_model
from verbecc.src.mlconjug.data_set import DataSet
from verbecc.src.mlconjug.mltypes import VerbTemplatePair


class TemplatePredictor:
    def __init__(
        self, verb_template_pairs: List[VerbTemplatePair], lang: LangCodeISO639_1
    ) -> None:
        self.data_set = DataSet(verb_template_pairs)
        model = load_model(lang)
        if not model:
            model = Model(lang=lang)
            model.train(self.data_set.train_input, self.data_set.train_labels)
            save_model(model)
        self.model = model
        return

    def predict(self, verb: str) -> Tuple[str, float]:
        predict_results: List[np.int64] = self.model.predict([verb])
        if len(predict_results) == 0:
            raise Exception("Template prediction failed")
        prediction = predict_results[0]
        predict_proba = self.model.pipeline.predict_proba([verb])
        prediction_score = predict_proba[0][prediction]
        template = self.data_set.templates[prediction]
        return (template, prediction_score)
