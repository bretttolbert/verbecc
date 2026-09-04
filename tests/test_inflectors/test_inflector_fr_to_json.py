import pytest
import json
import sys
from pathlib import Path
from typing import Any

try:
    from tests.common import assert_json_str_equal
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from common import assert_json_str_equal

from verbecc.core.conjugator.complete_conjugator import CompleteConjugator
from verbecc.core.conjugator.mood_conjugator import MoodConjugator
from verbecc.core.conjugator.tense_conjugator import TenseConjugator
from verbecc.core.defs.types.lang_code import LangCodeISO639_1 as Lang


@pytest.fixture(scope="module")
def ccg():
    ccg = CompleteConjugator(lang=Lang.fr)
    yield ccg


@pytest.fixture(scope="module")
def mcg():
    mcg = MoodConjugator(lang=Lang.fr)
    yield mcg


@pytest.fixture(scope="module")
def tcg():
    tcg = TenseConjugator(lang=Lang.fr)
    yield tcg


expected_value_conj_manger: dict[str, dict[str, Any]] = {
    "moods": {
        "conditionnel": {
            "passé": [
                {"c": ["j'aurais mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu aurais mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il aurait mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["elle aurait mangé"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["on aurait mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous aurions mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous auriez mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["ils auraient mangé"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["elles auraient mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["je mangerais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu mangerais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il mangerait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle mangerait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on mangerait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous mangerions"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous mangeriez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils mangeraient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles mangeraient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
        "imperatif": {
            "imperatif-passé": [
                {"c": ["aie mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["ayons mangé"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["ayez mangé"], "n": "p", "p": "2", "pr": "vous"},
            ],
            "imperatif-présent": [
                {"c": ["mange"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["mangeons"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["mangez"], "n": "p", "p": "2", "pr": "vous"},
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                {"c": ["j'aurai mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu auras mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il aura mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle aura mangé"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on aura mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous aurons mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous aurez mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils auront mangé"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles auront mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "futur-simple": [
                {"c": ["je mangerai"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu mangeras"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il mangera"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle mangera"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on mangera"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous mangerons"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous mangerez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils mangeront"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles mangeront"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imparfait": [
                {"c": ["je mangeais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu mangeais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il mangeait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle mangeait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on mangeait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous mangions"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous mangiez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils mangeaient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles mangeaient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-antérieur": [
                {"c": ["j'eus mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu eus mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il eut mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle eut mangé"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on eut mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous eûmes mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous eûtes mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils eurent mangé"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles eurent mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-composé": [
                {"c": ["j'ai mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu as mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il a mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle a mangé"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on a mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous avons mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {"c": ["vous avez mangé"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils ont mangé"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles ont mangé"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passé-simple": [
                {"c": ["je mangeai"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu mangeas"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il mangea"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle mangea"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on mangea"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous mangeâmes"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous mangeâtes"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils mangèrent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles mangèrent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "plus-que-parfait": [
                {"c": ["j'avais mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu avais mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il avait mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle avait mangé"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on avait mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous avions mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous aviez mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils avaient mangé"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles avaient mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["je mange"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu manges"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il mange"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle mange"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on mange"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous mangeons"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous mangez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils mangent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles mangent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitif": {"infinitif-présent": [{"c": ["manger"]}]},
        "participe": {
            "participe-passé": [
                {"c": ["mangé"], "g": "m", "n": "s"},
                {"c": ["mangés"], "g": "m", "n": "p"},
                {"c": ["mangée"], "g": "f", "n": "s"},
                {"c": ["mangées"], "g": "f", "n": "p"},
            ],
            "participe-présent": [{"c": ["mangeant"]}],
        },
        "subjonctif": {
            "imparfait": [
                {"c": ["que je mangeasse"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu mangeasses"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il mangeât"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle mangeât"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on mangeât"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous mangeassions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous mangeassiez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils mangeassent"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles mangeassent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé": [
                {"c": ["que j'aie mangé"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu aies mangé"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il ait mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["qu'elle ait mangé"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["qu'on ait mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous ayons mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous ayez mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils aient mangé"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles aient mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "plus-que-parfait": [
                {"c": ["que j'eusse mangé"], "n": "s", "p": "1", "pr": "je"},
                {
                    "c": ["que tu eusses mangé"],
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {"c": ["qu'il eût mangé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["qu'elle eût mangé"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["qu'on eût mangé"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous eussions mangé"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous eussiez mangé"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils eussent mangé"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles eussent mangé"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["que je mange"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu manges"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il mange"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle mange"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on mange"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous mangions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous mangiez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils mangent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles mangent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
    },
    "verb": {
        "infinitive": "manger",
        "lang": "fr",
        "predicted": False,
        "stem": "man",
        "template": "man:ger",
        "translation_en": "eat",
    },
}

expected_value_conj_pouvoir: dict[str, dict[str, Any]] = {
    "moods": {
        "conditionnel": {
            "passé": [
                {"c": ["j'aurais pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu aurais pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il aurait pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle aurait pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on aurait pu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous aurions pu"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous auriez pu"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils auraient pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles auraient pu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["je pourrais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu pourrais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il pourrait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pourrait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pourrait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous pourrions"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous pourriez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils pourraient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles pourraient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                {"c": ["j'aurai pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu auras pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il aura pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle aura pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on aura pu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous aurons pu"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous aurez pu"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils auront pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles auront pu"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "futur-simple": [
                {"c": ["je pourrai"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu pourras"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il pourra"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pourra"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pourra"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous pourrons"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous pourrez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils pourront"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles pourront"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imparfait": [
                {"c": ["je pouvais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu pouvais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il pouvait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pouvait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pouvait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous pouvions"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous pouviez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils pouvaient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles pouvaient"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passé-antérieur": [
                {"c": ["j'eus pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu eus pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il eut pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle eut pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on eut pu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous eûmes pu"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous eûtes pu"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils eurent pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles eurent pu"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passé-composé": [
                {"c": ["j'ai pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu as pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il a pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle a pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on a pu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous avons pu"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous avez pu"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils ont pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles ont pu"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passé-simple": [
                {"c": ["je pus"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu pus"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il put"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle put"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on put"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous pûmes"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous pûtes"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils purent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles purent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "plus-que-parfait": [
                {"c": ["j'avais pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu avais pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il avait pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle avait pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on avait pu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous avions pu"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous aviez pu"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils avaient pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles avaient pu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {
                    "c": ["je peux", "je puis"],
                    "n": "s",
                    "p": "1",
                    "pr": "je",
                },
                {"c": ["tu peux"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il peut"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle peut"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on peut"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["nous pouvons"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["vous pouvez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils peuvent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles peuvent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitif": {"infinitif-présent": [{"c": ["pouvoir"]}]},
        "participe": {
            "participe-passé": [
                {"c": ["pu"], "g": "m", "n": "s"},
                {"c": ["pus"], "g": "m", "n": "p"},
                {"c": ["pue"], "g": "f", "n": "s"},
                {"c": ["pues"], "g": "f", "n": "p"},
            ],
            "participe-présent": [{"c": ["pouvant"]}],
        },
        "subjonctif": {
            "imparfait": [
                {"c": ["que je pusse"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu pusses"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il pût"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle pût"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on pût"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous pussions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous pussiez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils pussent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles pussent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé": [
                {"c": ["que j'aie pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu aies pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il ait pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle ait pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on ait pu"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous ayons pu"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous ayez pu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils aient pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles aient pu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "plus-que-parfait": [
                {"c": ["que j'eusse pu"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu eusses pu"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il eût pu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle eût pu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on eût pu"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous eussions pu"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous eussiez pu"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils eussent pu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles eussent pu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["que je puisse"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu puisses"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il puisse"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle puisse"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on puisse"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous puissions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous puissiez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils puissent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles puissent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
    },
    "verb": {
        "infinitive": "pouvoir",
        "lang": "fr",
        "predicted": False,
        "stem": "p",
        "template": "p:ouvoir",
        "translation_en": "power",
    },
}


expected_value_conj_pleuvoir: dict[str, dict[str, Any]] = {
    "moods": {
        "conditionnel": {
            "passé": [
                {"c": ["il aurait plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle aurait plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on aurait plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils auraient plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles auraient plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["il pleuvrait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pleuvrait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pleuvrait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils pleuvraient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles pleuvraient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
        "imperatif": {"imperatif-passé": [], "imperatif-présent": []},
        "indicatif": {
            "futur-antérieur": [
                {"c": ["il aura plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle aura plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on aura plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils auront plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles auront plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "futur-simple": [
                {"c": ["il pleuvra"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pleuvra"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pleuvra"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils pleuvront"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles pleuvront"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "imparfait": [
                {"c": ["il pleuvait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pleuvait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pleuvait"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils pleuvaient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles pleuvaient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-antérieur": [
                {"c": ["il eut plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle eut plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on eut plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils eurent plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles eurent plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-composé": [
                {"c": ["il a plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle a plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on a plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils ont plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles ont plu"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "passé-simple": [
                {"c": ["il plut"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle plut"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on plut"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils plurent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles plurent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
            "plus-que-parfait": [
                {"c": ["il avait plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle avait plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on avait plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils avaient plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles avaient plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["il pleut"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle pleut"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on pleut"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["ils pleuvent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles pleuvent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitif": {"infinitif-présent": [{"c": ["pleuvoir"]}]},
        "participe": {
            "participe-passé": [
                {"c": ["plu"], "g": "m", "n": "s"},
                {"c": ["plus"], "g": "m", "n": "p"},
                {"c": ["plue"], "g": "f", "n": "s"},
                {"c": ["plues"], "g": "f", "n": "p"},
            ],
            "participe-présent": [{"c": ["pleuvant"]}],
        },
        "subjonctif": {
            "imparfait": [
                {"c": ["qu'il plût"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle plût"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on plût"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["qu'ils plussent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles plussent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé": [
                {"c": ["qu'il ait plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle ait plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on ait plu"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["qu'ils aient plu"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles aient plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "plus-que-parfait": [
                {"c": ["qu'il eût plu"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle eût plu"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on eût plu"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["qu'ils eussent plu"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles eussent plu"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["qu'il pleuve"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle pleuve"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on pleuve"], "n": "s", "p": "3", "pr": "on"},
                {"c": ["qu'ils pleuvent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles pleuvent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
    },
    "verb": {
        "infinitive": "pleuvoir",
        "lang": "fr",
        "predicted": False,
        "stem": "pl",
        "template": "pl:euvoir",
        "translation_en": "rain",
    },
}


expected_value_conj_se_lever: dict[str, dict[str, Any]] = {
    "moods": {
        "conditionnel": {
            "passé": [
                {"c": ["je me serais levée"], "g": "f", "n": "s", "p": "1", "pr": "je"},
                {"c": ["je me serais levé"], "g": "m", "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te serais levée"], "g": "f", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["tu te serais levé"], "g": "m", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se serait levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["elle se serait levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["on se serait levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["on se serait levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous serions levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["nous nous serions levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous seriez levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["vous vous seriez levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["ils se seraient levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["elles se seraient levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["je me lèverais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te lèverais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se lèverait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle se lèverait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on se lèverait"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous lèverions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous lèveriez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils se lèveraient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles se lèveraient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
        "imperatif": {
            "imperatif-passé": [],
            "imperatif-présent": [
                {"c": ["lève-toi"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["levons-nous"], "n": "p", "p": "1", "pr": "nous"},
                {"c": ["levez-vous"], "n": "p", "p": "2", "pr": "vous"},
            ],
        },
        "indicatif": {
            "futur-antérieur": [
                {"c": ["je me serai levée"], "g": "f", "n": "s", "p": "1", "pr": "je"},
                {"c": ["je me serai levé"], "g": "m", "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te seras levée"], "g": "f", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["tu te seras levé"], "g": "m", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se sera levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["elle se sera levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["on se sera levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["on se sera levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous serons levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["nous nous serons levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous serez levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["vous vous serez levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["ils se seront levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["elles se seront levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "futur-simple": [
                {"c": ["je me lèverai"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te lèveras"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se lèvera"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle se lèvera"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on se lèvera"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous lèverons"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous lèverez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils se lèveront"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles se lèveront"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "imparfait": [
                {"c": ["je me levais"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te levais"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se levait"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle se levait"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on se levait"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous levions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous leviez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils se levaient"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles se levaient"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-antérieur": [
                {"c": ["je me fus levée"], "g": "f", "n": "s", "p": "1", "pr": "je"},
                {"c": ["je me fus levé"], "g": "m", "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te fus levée"], "g": "f", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["tu te fus levé"], "g": "m", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se fut levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["elle se fut levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["on se fut levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["on se fut levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous fûmes levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["nous nous fûmes levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous fûtes levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["vous vous fûtes levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["ils se furent levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["elles se furent levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-composé": [
                {"c": ["je me suis levée"], "g": "f", "n": "s", "p": "1", "pr": "je"},
                {"c": ["je me suis levé"], "g": "m", "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu t'es levée"], "g": "f", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["tu t'es levé"], "g": "m", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il s'est levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle s'est levée"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on s'est levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["on s'est levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous sommes levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["nous nous sommes levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous êtes levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["vous vous êtes levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils se sont levés"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles se sont levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé-simple": [
                {"c": ["je me levai"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te levas"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se leva"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle se leva"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on se leva"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous levâmes"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous levâtes"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["ils se levèrent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["elles se levèrent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "plus-que-parfait": [
                {"c": ["je m'étais levée"], "g": "f", "n": "s", "p": "1", "pr": "je"},
                {"c": ["je m'étais levé"], "g": "m", "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu t'étais levée"], "g": "f", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["tu t'étais levé"], "g": "m", "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il s'était levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["elle s'était levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["on s'était levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["on s'était levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous étions levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["nous nous étions levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["vous vous étiez levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["vous vous étiez levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["ils s'étaient levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["elles s'étaient levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["je me lève"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["tu te lèves"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["il se lève"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["elle se lève"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["on se lève"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["nous nous levons"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {"c": ["vous vous levez"], "n": "p", "p": "2", "pr": "vous"},
                {"c": ["ils se lèvent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {"c": ["elles se lèvent"], "g": "f", "n": "p", "p": "3", "pr": "elles"},
            ],
        },
        "infinitif": {"infinitif-présent": [{"c": ["lever"]}]},
        "participe": {
            "participe-passé": [
                {"c": ["étant levé"], "g": "m", "n": "s"},
                {"c": ["étant levés"], "g": "m", "n": "p"},
                {"c": ["étant levée"], "g": "f", "n": "s"},
                {"c": ["étant levées"], "g": "f", "n": "p"},
            ],
            "participe-présent": [{"c": ["levant"]}],
        },
        "subjonctif": {
            "imparfait": [
                {"c": ["que je me levasse"], "n": "s", "p": "1", "pr": "je"},
                {
                    "c": ["que tu te levasses"],
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {"c": ["qu'il se levât"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle se levât"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on se levât"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous nous levassions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous vous levassiez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils se levassent"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles se levassent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "passé": [
                {
                    "c": ["que je me sois levée"],
                    "g": "f",
                    "n": "s",
                    "p": "1",
                    "pr": "je",
                },
                {
                    "c": ["que je me sois levé"],
                    "g": "m",
                    "n": "s",
                    "p": "1",
                    "pr": "je",
                },
                {
                    "c": ["que tu te sois levée"],
                    "g": "f",
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {
                    "c": ["que tu te sois levé"],
                    "g": "m",
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {"c": ["qu'il se soit levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["qu'elle se soit levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {
                    "c": ["qu'on se soit levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "on",
                },
                {"c": ["qu'on se soit levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous nous soyons levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que nous nous soyons levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous vous soyez levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["que vous vous soyez levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils se soient levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles se soient levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "plus-que-parfait": [
                {
                    "c": ["que je me fusse levée"],
                    "g": "f",
                    "n": "s",
                    "p": "1",
                    "pr": "je",
                },
                {
                    "c": ["que je me fusse levé"],
                    "g": "m",
                    "n": "s",
                    "p": "1",
                    "pr": "je",
                },
                {
                    "c": ["que tu te fusses levée"],
                    "g": "f",
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {
                    "c": ["que tu te fusses levé"],
                    "g": "m",
                    "n": "s",
                    "p": "2",
                    "pr": "tu",
                },
                {"c": ["qu'il se fût levé"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {
                    "c": ["qu'elle se fût levée"],
                    "g": "f",
                    "n": "s",
                    "p": "3",
                    "pr": "elle",
                },
                {"c": ["qu'on se fût levée"], "g": "f", "n": "s", "p": "3", "pr": "on"},
                {"c": ["qu'on se fût levé"], "g": "m", "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous nous fussions levées"],
                    "g": "f",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que nous nous fussions levés"],
                    "g": "m",
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous vous fussiez levées"],
                    "g": "f",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["que vous vous fussiez levés"],
                    "g": "m",
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {
                    "c": ["qu'ils se fussent levés"],
                    "g": "m",
                    "n": "p",
                    "p": "3",
                    "pr": "ils",
                },
                {
                    "c": ["qu'elles se fussent levées"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
            "présent": [
                {"c": ["que je me lève"], "n": "s", "p": "1", "pr": "je"},
                {"c": ["que tu te lèves"], "n": "s", "p": "2", "pr": "tu"},
                {"c": ["qu'il se lève"], "g": "m", "n": "s", "p": "3", "pr": "il"},
                {"c": ["qu'elle se lève"], "g": "f", "n": "s", "p": "3", "pr": "elle"},
                {"c": ["qu'on se lève"], "n": "s", "p": "3", "pr": "on"},
                {
                    "c": ["que nous nous levions"],
                    "n": "p",
                    "p": "1",
                    "pr": "nous",
                },
                {
                    "c": ["que vous vous leviez"],
                    "n": "p",
                    "p": "2",
                    "pr": "vous",
                },
                {"c": ["qu'ils se lèvent"], "g": "m", "n": "p", "p": "3", "pr": "ils"},
                {
                    "c": ["qu'elles se lèvent"],
                    "g": "f",
                    "n": "p",
                    "p": "3",
                    "pr": "elles",
                },
            ],
        },
    },
    "verb": {
        "infinitive": "lever",
        "lang": "fr",
        "predicted": False,
        "stem": "l",
        "template": "l:ever",
        "translation_en": "lift",
    },
}

"""
asserts that conjugator.cojugate returns the expected_value
Why not use @pytest.mark.parametrize?
Because it sucks.
Seriously I was using it but it makes the tests more difficult to debug and
makes it impossible to call certain tests with a -k expression e.g.

python -m pytest . -vv -k test_conjugate[Se lever-expected_value4]

I think this pattern of
many "def test_<SUT>_<value>(fixtures)" to one "def run_test_<SUT>(value)" 
as exhibited bleow is better than @pytest.mark.parametrize in many cases. 

Another benefit is being able to jump directly to the specific test
by clicking on it in VSCode. You can't do that with parametrize.

"""


def run_test_conjugate_to_json_(
    ccg: CompleteConjugator,
    infinitive: str,
    expected_value: dict[str, dict[str, Any]],
):
    cc = ccg.conjugate(infinitive)
    conj_json = cc.to_json(beautify=False)
    assert_json_str_equal(conj_json, json.dumps(expected_value))


def test_conjugate_to_json_manger(ccg: CompleteConjugator):
    run_test_conjugate_to_json_(ccg, "manger", expected_value_conj_manger)


def test_conjugate_to_json_pouvoir(ccg: CompleteConjugator):
    run_test_conjugate_to_json_(ccg, "pouvoir", expected_value_conj_pouvoir)


def test_conjugate_to_json_Pouvoir(ccg: CompleteConjugator):
    run_test_conjugate_to_json_(ccg, "Pouvoir", expected_value_conj_pouvoir)


def test_conjugate_to_json_pleuvoir(ccg: CompleteConjugator):
    run_test_conjugate_to_json_(ccg, "pleuvoir", expected_value_conj_pleuvoir)


def test_conjugate_to_json_Se_lever(ccg: CompleteConjugator):
    run_test_conjugate_to_json_(ccg, "Se lever", expected_value_conj_se_lever)
