# -*- coding: utf-8 -*-

import pytest
from verbecc import mlconjug
from verbecc import inflector_fr
from verbecc import config

inf = inflector_fr.InflectorFr()
verb_template_pairs = [(v.infinitive,v.template) for v in inf._verb_parser.verbs]

def test_extract_verb_features():
    if config.ml:
        assert mlconjug.extract_verb_features('parler', 'fr', (2, 7)) == [
            'END=er', 'END=ler', 'END=rler', 'END=arler', 'END=parler', 
            'START=pa', 'START=par', 'START=parl', 'START=parle', 'START=parler', 
            'LEN=6', 'VOW_NUM=2', 'CONS_NUM=4', 'V/C=0.5']

def test_data_set_construct_dict_conjug():
    if config.ml:
        dict_conjug = mlconjug.DataSet(verb_template_pairs).dict_conjug
        assert 'abaisser' in dict_conjug['aim:er']

def test_data_set_split_test_train():
    if config.ml:
        data_set = mlconjug.DataSet(verb_template_pairs)
        assert data_set.min_threshold == 8
        assert data_set.split_proportion == 0.5
        assert len(data_set.train_input) == len(data_set.train_labels)
        assert len(data_set.test_input) == len(data_set.test_labels)
        for verb in data_set.test_input:
            assert verb not in data_set.train_input
        test_verb = data_set.test_input[0]
        train_verb = data_set.train_input[0]
        test_template = next(p[1] for p in verb_template_pairs if p[0] == test_verb)
        train_template = next(p[1] for p in verb_template_pairs if p[0] == train_verb)
        assert data_set.templates[data_set.test_labels[data_set.test_input.index(test_verb)]] == test_template
        assert data_set.templates[data_set.train_labels[data_set.train_input.index(train_verb)]] == train_template

def test_mlconjug_template_predictor():
    if config.ml:
        predictor = mlconjug.TemplatePredictor(verb_template_pairs, lang='fr')
        template, prediction_score = predictor.predict('parler')
        assert template == 'aim:er'
        assert prediction_score > 0.99
