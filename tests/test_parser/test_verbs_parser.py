from verbecc.src.parsers.verbs_parser import VerbsParser
from verbecc.src.defs.types.lang_code import LangCodeISO639_1 as Lang


def test_verbs_parser():
    vp = VerbsParser(Lang.fr)
    verbs = vp.parse()
    assert len(verbs) >= 7000
