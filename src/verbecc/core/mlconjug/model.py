from typing import List
from functools import partial
import numpy as np

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

from verbecc.core.defs.types.lang_code import LangCodeISO639_1

from verbecc.core.mlconjug.mltypes import (
    Classifier,
    Vectorizor,
    FeatureSelector,
    CountVectorizer,
)
from verbecc.core.mlconjug.feature_extract import extract_verb_features


class Model:
    """
    | This class manages the scikit-learn pipeline.
    | The Pipeline includes a feature vectorizer, a feature selector and a classifier.
    | If any of the vectorizer, feature selector or classifier is not supplied at instance declaration,
     the __init__ method will provide good default values that get more than 92% prediction accuracy.

    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method
    :param language: language of the corpus of verbs to be analyzed.
    """

    def __init__(
        self,
        vectorizer: Vectorizor = None,
        feature_selector: FeatureSelector = None,
        classifier: Classifier = None,
        lang: LangCodeISO639_1 = LangCodeISO639_1.fr,
    ) -> None:
        if not vectorizer:
            vectorizer = CountVectorizer(
                analyzer=partial(extract_verb_features, lang=lang, ngram_range=(2, 7)),
                binary=True,
            )
        if not feature_selector:
            feature_selector = SelectFromModel(LinearSVC(penalty="l1", max_iter=20000, dual=False, verbose=0))
        if not classifier:
            classifier = SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                l1_ratio=0.15,
                max_iter=100000,
                alpha=1e-5,
                verbose=0,
            )

        self.pipeline = Pipeline(
            [
                ("vectorizer", vectorizer),
                ("feature_selector", feature_selector),
                ("classifier", classifier),
            ]
        )
        self.lang = lang
        return

    def __repr__(self) -> str:
        return "{0}.{1}({2}, {3}, {4})".format(__name__, self.__class__.__name__, *sorted(self.pipeline.named_steps))

    def train(self, samples: list[str], labels: list[int]) -> None:
        """
        Trains the pipeline on the supplied samples and labels.

        :param samples: list[str].
            List of verbs.
        :param labels: list[int].
            List of verb template indices.

        """
        self.pipeline = self.pipeline.fit(samples, labels)
        return

    def predict(self, verbs: list[str]) -> list[np.int64]:
        """
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list[str].
            List of verbs.
        :return: list[np.int64].
            List of incices of predicted conjugation templates

        """
        prediction = self.pipeline.predict(verbs)
        return list(prediction)
