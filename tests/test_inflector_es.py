# -*- coding: utf-8 -*-

import pytest

from verbecc import inflector_es

inf = inflector_es.InflectorEs()

def test_inflector_es_conjugate():
    assert inf.conjugate('comer') is not None
