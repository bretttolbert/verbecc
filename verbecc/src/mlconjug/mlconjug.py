"""
Brett Tolbert note:

This module adds an ML-based conjugation template prediction
feature. E.g. given the infinitive form of a verb, it can accurately
predict which conjugation template the verb should be conjugated
with.

The code in this module is based on an early version of mlconjug by Sekou Diao:
https://github.com/SekouD/mlconjug
Sekou Diao notes that a newer version of mjconjug is now available (mlconjug3):
https://github.com/SekouDiaoNlp/mlconjug3

However I have updated this version to use importlib_resources instead of
the deprecated pkg_resources API (as of today, mlconjug3 is still using
pkg_resources)

History:
verbecc predates mlconjug and verbecc's verb conjugation implementation
was developed independently of mlconjug, but credit to Sekou Diao for the ML
template prediction code in this module and for and the XML conjugation templates
for languages other than French and Catalan.

Credit to Pierre Sarrazin (Verbiste) for the developing the original French
XML conjugation template format on which both verbecc and mlconjug are based.

I found mlconjug and was impressed by the machine learning feature and I
so I borrowed this feature and retrofit it onto verbecc.
I chose not to add the entire mlconjug python package as a dependency because
it duplicates much of the functionality of verbecc and would be redundant.
mlconjug and verbecc are independent projects and this file, based on the
origin mlconjug module, has diverged.

verbecc is Open Source Software (GNU LGPL license)
mlconjug is also Open Source Software (MIT license)
Verbiste is Open Source Software (GNU GPL license)

Copyright (c) 2025, Brett Tolbert <http://bretttolbert.com/>
Copyright (c) 2017, SekouD <https://github.com/SekouDiaoNlp/>
Copyright (c) 2003-2016, Pierre Sarrazin <http://sarrazip.com/>
"""

__author__ = ["Sekou Diao"]
__credits__ = ["Sekou Diao", "Pierre Sarrazin", "Brett Tolbert"]


import re
from collections import defaultdict
from functools import partial
from importlib_resources import as_file, files
import os
import pickle
import random
from typing import Any, Dict, List, Tuple, Union
from zipfile import ZipFile

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from verbecc.src.defs.constants.grammar_defines import ALPHABET
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
import logging

from verbecc.src.defs.constants.config import DEVEL_MODE

logging_level = logging.CRITICAL + 1  # effectively disables logging
if DEVEL_MODE:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("verbecc-mlconjug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

VerbTemplatePair = Tuple[str, str]  # (verb, template)
Vectorizor = Union[CountVectorizer, Any]
FeatureSelector = Union[SelectFromModel, Any]
Classifier = Union[SGDClassifier, Any]


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
        prediction = self.model.predict([verb])[0]
        prediction_score = self.model.pipeline.predict_proba([verb])[0][prediction]
        template = self.data_set.templates[prediction]
        return (template, prediction_score)


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
            feature_selector = SelectFromModel(
                LinearSVC(penalty="l1", max_iter=12000, dual=False, verbose=0)
            )
        if not classifier:
            classifier = SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                l1_ratio=0.15,
                max_iter=40000,
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
        return "{0}.{1}({2}, {3}, {4})".format(
            __name__, self.__class__.__name__, *sorted(self.pipeline.named_steps)
        )

    def train(self, samples: List[str], labels: List[int]) -> None:
        """
        Trains the pipeline on the supplied samples and labels.

        :param samples: list[str].
            List of verbs.
        :param labels: list[int].
            List of verb template indices.

        """
        self.pipeline = self.pipeline.fit(samples, labels)
        return

    def predict(self, verbs: List[str]) -> List[str]:
        """
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list[str].
            List of verbs.
        :return: list[str].
            List of predicted conjugation groups.

        """
        prediction = self.pipeline.predict(verbs)
        return prediction


class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper methodss for managing Machine Learning tasks like constructing a training and testing set.
    """

    def __init__(self, verb_template_pairs: List[VerbTemplatePair]) -> None:
        self.verbs = [pair[0] for pair in verb_template_pairs]
        self.templates = sorted(set([pair[1] for pair in verb_template_pairs]))
        self.dict_conjug = self._construct_dict_conjug(verb_template_pairs)
        self._split_test_train()
        return

    def _construct_dict_conjug(
        self, verb_template_pairs: List[VerbTemplatePair]
    ) -> Dict[str, List[str]]:
        """
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.

        :param verb_template_pairs: list.
            List of tuples of (verb,template) e.g. ('abaisser','aim:er')
        :return: defaultdict.
            defaultdict mapping each template to one or more verbs e.g. {'aim:er': ['abaisser', ...]}
        """
        ret = defaultdict(list)
        random.shuffle(verb_template_pairs)
        for verb, template in verb_template_pairs:
            ret[template].append(verb)
        return ret

    def _split_test_train(self, threshold: int = 8, proportion: float = 0.5) -> None:
        """
        Splits the template:verbs dict into a training and a testing set.

        :param verb_template_pairs: list.
            List of tuples of (verb,template) e.g. ('abaisser','aim:er')
        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set.
            Must be between 0 and 1.

        """
        if proportion <= 0 or proportion > 1:
            raise ValueError(
                f"The split proportion ({proportion}) must be between 0 and 1."
            )
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set: List[VerbTemplatePair] = []
        test_set: List[VerbTemplatePair] = []
        for template, lverbs in self.dict_conjug.items():
            if len(lverbs) <= threshold:
                for verb in lverbs:
                    train_set.append((verb, template))
            else:
                index = round(len(lverbs) * proportion)
                for verb in lverbs[:index]:
                    train_set.append((verb, template))
                for verb in lverbs[index:]:
                    test_set.append((verb, template))
        random.shuffle(train_set)
        random.shuffle(test_set)
        self.train_input: List[str] = [elmt[0] for elmt in train_set]
        self.train_labels: List[int] = [
            self.templates.index(elmt[1]) for elmt in train_set
        ]
        self.test_input: List[str] = [elmt[0] for elmt in test_set]
        self.test_labels: List[int] = [
            self.templates.index(elmt[1]) for elmt in test_set
        ]


def extract_verb_features(
    verb: str, lang: LangCodeISO639_1, ngram_range: Tuple[int, int]
) -> List[str]:
    """
    | Custom Vectorizer optimized for extracting verbs features.
    | The Vectorizer subclasses sklearn.feature_extraction.text.CountVectorizer .
    | As in Indo-European languages verbs are inflected by adding a morphological suffix,
     the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.

    | To enhance the results of the feature extration, several other features have been included:

    | The features are the verb's ending n-grams, starting n-grams, length of the verb, number of vowels,
     number of consonants and the ratio of vowels over consonants.

    :param verb: string.
        Verb to vectorize.
    :param lang: LangCodeISO639_1.
        Language to analyze.
    :param ngram_range: tuple.
        The range of the ngram sliding window.
    :return: list[str].
        List of the most salient features of the verb for the task of finding it's conjugation's class.

    """
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb)
    verb = verb.lower()
    verb_len = len(verb)
    length_feature = "LEN={0}".format(str(verb_len))
    min_n, max_n = ngram_range
    final_ngrams = [
        "END={0}".format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))
    ]
    initial_ngrams = [
        "START={0}".format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))
    ]
    if lang not in ALPHABET:
        lang = "en"  # We chose 'en' as the default alphabet because EN is more standard, without accents or diactrics.
    vowels = sum(verb.count(c) for c in ALPHABET[lang]["vowels"])
    vowels_number = "VOW_NUM={0}".format(vowels)
    consonants = sum(verb.count(c) for c in ALPHABET[lang]["consonants"])
    consonants_number = "CONS_NUM={0}".format(consonants)
    if consonants == 0:
        vow_cons_ratio = "V/C=N/A"
    else:
        vow_cons_ratio = "V/C={0}".format(round(vowels / consonants, 2))
    final_ngrams.extend(initial_ngrams)
    final_ngrams.extend(
        (length_feature, vowels_number, consonants_number, vow_cons_ratio)
    )
    return final_ngrams


def get_model_zip_filename(lang: LangCodeISO639_1) -> str:
    return "data/models/trained_model-{}.zip".format(lang)


def get_model_pickle_filename(lang: LangCodeISO639_1) -> str:
    return "trained_model-{0}.pickle".format(lang)


def save_model(model: Model) -> None:
    pickle_filename = get_model_pickle_filename(model.lang)
    with open(pickle_filename, "wb") as f:
        pickle.dump(model, f)
    zip_filename = get_model_zip_filename(model.lang)
    zip_path = files("verbecc") / zip_filename
    with as_file(zip_path) as f:
        with ZipFile(f, mode="w") as zf:
            zf.write(pickle_filename)
            logger.info(
                "Saved model pickle filename %s to zip filename %s.",
                pickle_filename,
                zip_filename,
            )
    os.remove(pickle_filename)


def load_model(lang: LangCodeISO639_1) -> Model:
    model = None
    zip_filename = get_model_zip_filename(lang)
    try:
        zip_path = files("verbecc") / zip_filename
        with as_file(zip_path) as f:
            with ZipFile(f) as zf:
                pickle_filename = get_model_pickle_filename(lang)
                with zf.open(pickle_filename, "r") as model_pickle:
                    model = pickle.loads(model_pickle.read())
                    logger.info(
                        "Loaded model pickle filename %s from zip filename %s",
                        pickle_filename,
                        zip_filename,
                    )
    except Exception as ex:
        logger.warning(
            "Exception loading model %s: %s", zip_filename, ex, exc_info=True
        )
    return model
