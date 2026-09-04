import pytest

from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang
from verbecc.core.mlconjug.data_set import DataSet
from verbecc.core.mlconjug.predictor import TemplatePredictor
from verbecc.core.mlconjug.feature_extract import extract_verb_features
from verbecc.core.inflectors.lang.inflector_fr import InflectorFr
from verbecc.core.utils.config.verbecc_config_util import VerbeccConfigUtil

config = VerbeccConfigUtil().load_config()


@pytest.fixture(scope="module")
def verb_template_pairs():
    inf = InflectorFr()
    yield [(v.infinitive, v.template) for v in inf._verbs]


def test_extract_verb_features():
    if config.ENABLE_ML_PREDICTION:
        assert extract_verb_features("parler", Lang.fr, (2, 7)) == [
            "END=er",
            "END=ler",
            "END=rler",
            "END=arler",
            "END=parler",
            "START=pa",
            "START=par",
            "START=parl",
            "START=parle",
            "START=parler",
            "LEN=6",
            "VOW_NUM=2",
            "CONS_NUM=4",
            "V/C=0.5",
        ]


def test_DataSet_construct_dict_conjug(verb_template_pairs):
    if config.ENABLE_ML_PREDICTION:
        dict_conjug = DataSet(verb_template_pairs).dict_conjug
        assert "abaisser" in dict_conjug["aim:er"]


def test_DataSet_split_test_train(verb_template_pairs):
    if config.ENABLE_ML_PREDICTION:
        ds = DataSet(verb_template_pairs)
        assert ds.min_threshold == 8
        assert ds.split_proportion == 0.5
        assert len(ds.train_input) == len(ds.train_labels)
        assert len(ds.test_input) == len(ds.test_labels)
        for verb in ds.test_input:
            assert verb not in ds.train_input
        test_verb = ds.test_input[0]
        train_verb = ds.train_input[0]
        test_template = next(p[1] for p in verb_template_pairs if p[0] == test_verb)
        train_template = next(p[1] for p in verb_template_pairs if p[0] == train_verb)
        assert (
            ds.templates[ds.test_labels[ds.test_input.index(test_verb)]]
            == test_template
        )
        assert (
            ds.templates[ds.train_labels[ds.train_input.index(train_verb)]]
            == train_template
        )


def test_mlconjug_template_predictor(verb_template_pairs):
    if config.ENABLE_ML_PREDICTION:
        predictor = TemplatePredictor(verb_template_pairs, lang=Lang.fr)
        template, prediction_score = predictor.predict("parler")
        assert template == "aim:er"
        assert prediction_score > 0.97
