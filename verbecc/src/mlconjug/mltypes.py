from typing import Tuple, Union, Any

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

VerbTemplatePair = Tuple[str, str]  # (verb, template)
Vectorizor = Union[CountVectorizer, Any]
FeatureSelector = Union[SelectFromModel, Any]
Classifier = Union[SGDClassifier, Any]
