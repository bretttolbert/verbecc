# -*- coding: utf-8 -*-

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

verbecc predates mlconjug and verbecc's verb conjugation implementation
was developed independently of mlconjug, but credit to Sekou Diao for the ML
template prediction code in this module and for and the XML conjugation templates
for languages other than French. Credit to Pierre Sarrazin (Verbiste) for the 
developing the original French XML conjugation template format on which both 
verbecc and mlconjug are based.

I found mlconjug and was impressed by the machine learning feature and I 
so I borrowed this feature and retrofit it onto verbecc. 
I chose not to add the entire mlconjug python package as a dependency because 
it duplicates much of the functionality of verbecc and would be redundant. 
So this one source file of verbecc is based mlconjug's mlconjug.py but 
mlconjug and verbecc are independent projects and this file has diverged.

verbecc is Open Source Software (GNU GPL license)
mlconjug is also Open Source Software (MIT license)
Verbiste is Open Source Software (GNU GPL license)

Copyright (c) 2023, Brett Tolbert <http://bretttolbert.com/>
Copyright (c) 2017, SekouD <https://github.com/SekouDiaoNlp/>
Copyright (c) 2003-2016, Pierre Sarrazin <http://sarrazip.com/>
"""

__author__ = ["Sekou Diao"]
__credits__ = ["Sekou Diao", "Pierre Sarrazin"]


import re
import os
import random
from collections import defaultdict
from functools import partial
import pickle
import pkg_resources
from zipfile import ZipFile
from typing import Dict, List, Tuple

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from verbecc.grammar_defines import ALPHABET


class TemplatePredictor:
    def __init__(self, verb_template_pairs: List[Tuple[str,str]], lang: str):
        self.data_set = DataSet(verb_template_pairs)
        model = load_model(lang)
        if not model:
            model = Model(lang=lang)
            model.train(self.data_set.train_input, self.data_set.train_labels)
            save_model(model)
        self.model = model

    def predict(self, verb):
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
    def __init__(self, vectorizer=None, feature_selector=None, classifier=None, lang='fr'):
        if not vectorizer:
            vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, 
                                                          lang=lang, 
                                                          ngram_range=(2, 7)), 
                                        binary=True)
        if not feature_selector:
            feature_selector = SelectFromModel(LinearSVC(penalty='l1', 
                                                         max_iter=12000, 
                                                         dual=False, 
                                                         verbose=0))
        if not classifier:
            classifier = SGDClassifier(loss='log_loss', 
                                       penalty='elasticnet', 
                                       l1_ratio=0.15,
                                       max_iter=40000, 
                                       alpha=1e-5, 
                                       verbose=0)
                                       
        self.pipeline = Pipeline([('vectorizer', vectorizer),
                                  ('feature_selector', feature_selector),
                                  ('classifier', classifier)])
        self.lang = lang
        return

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, *sorted(self.pipeline.named_steps))

    def train(self, samples, labels):
        """
        Trains the pipeline on the supplied samples and labels.

        :param samples: list.
            List of verbs.
        :param labels: list.
            List of verb templates.

        """
        self.pipeline = self.pipeline.fit(samples, labels)
        return

    def predict(self, verbs):
        """
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list.
            List of verbs.
        :return: list.
            List of predicted conjugation groups.

        """
        prediction = self.pipeline.predict(verbs)
        return prediction



class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper methodss for managing Machine Learning tasks like constructing a training and testing set.
    """

    def __init__(self, verb_template_pairs: List[Tuple[str,str]]):
        self.verbs = [pair[0] for pair in verb_template_pairs]
        self.templates = sorted(set([pair[1] for pair in verb_template_pairs]))
        self.dict_conjug = self._construct_dict_conjug(verb_template_pairs)
        self._split_test_train()

    def _construct_dict_conjug(self, verb_template_pairs: List[Tuple[str,str]]) -> Dict[str, List[str]]:
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

    def _split_test_train(self, threshold: int=8, proportion: float=0.5):
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
            raise ValueError(f'The split proportion ({proportion}) must be between 0 and 1.')
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set = []
        test_set = []
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
        self.train_input = [elmt[0] for elmt in train_set]
        self.train_labels = [self.templates.index(elmt[1]) for elmt in train_set]
        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [self.templates.index(elmt[1]) for elmt in test_set]
        return


def extract_verb_features(verb, lang: str, ngram_range: Tuple[int, int]):
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
    :param lang: string.
        Language to analyze.
    :param ngram_range: tuple.
        The range of the ngram sliding window.
    :return: list.
        List of the most salient features of the verb for the task of finding it's conjugation's class.

    """
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb)
    verb = verb.lower()
    verb_len = len(verb)
    length_feature = 'LEN={0}'.format(str(verb_len))
    min_n, max_n = ngram_range
    final_ngrams = ['END={0}'.format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    initial_ngrams = ['START={0}'.format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    if lang not in ALPHABET:
        lang = 'en'  # We chose 'en' as the default alphabet because english is more standard, without accents or diactrics.
    vowels = sum(verb.count(c) for c in ALPHABET[lang]['vowels'])
    vowels_number = 'VOW_NUM={0}'.format(vowels)
    consonants = sum(verb.count(c) for c in ALPHABET[lang]['consonants'])
    consonants_number = 'CONS_NUM={0}'.format(consonants)
    if consonants == 0:
        vow_cons_ratio = 'V/C=N/A'
    else:
        vow_cons_ratio = 'V/C={0}'.format(round(vowels / consonants, 2))
    final_ngrams.extend(initial_ngrams)
    final_ngrams.extend((length_feature, vowels_number, consonants_number, vow_cons_ratio))
    return final_ngrams

def get_model_zip_filename(lang: str) -> str:
    return 'data/models/trained_model-{}.zip'.format(lang)
    
def get_model_pickle_filename(lang: str) -> str:
    return 'trained_model-{0}.pickle'.format(lang)

def save_model(model: Model):
    pickle_filename = get_model_pickle_filename(model.lang)
    with open(pickle_filename, 'wb') as f:
        pickle.dump(model, f)
    zip_filename = get_model_zip_filename(model.lang)
    with ZipFile(pkg_resources.resource_filename(
            "verbecc", zip_filename), mode='w') as zf:
        zf.write(pickle_filename)
    os.remove(pickle_filename)

def load_model(lang):
    model = None
    zip_filename = get_model_zip_filename(lang)
    try:
        with ZipFile(pkg_resources.resource_stream(
                __name__, zip_filename)) as zf:
            with zf.open(get_model_pickle_filename(lang), 'r') as model_pickle:
                model = pickle.loads(model_pickle.read())
    except:
        pass
    return model
