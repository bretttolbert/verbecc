from verbecc.src.utils.string_utils import (
    get_common_letters,
    get_common_letter_count,
    starts_with_vowel,
    strip_accents,
    unicodefix,
)


def test_starts_with_vowel():
    assert starts_with_vowel("aller")
    assert not starts_with_vowel("banane")
    assert starts_with_vowel("éparpiller")
    assert not starts_with_vowel("yodler")
    assert not starts_with_vowel("")


def test_strip_accents():
    assert (
        strip_accents("français, être, égalité, très")
        == "francais, etre, egalite, tres"
    )


def test_get_common_letters():
    assert get_common_letters("brett", "tolbert") == {"b": 1, "e": 1, "r": 1, "t": 2}


def test_get_common_letters_count():
    assert get_common_letter_count("brett", "tolbert") == 5
    assert get_common_letter_count("çar", "cer") == 1
    assert get_common_letter_count(strip_accents("çar"), "cer") == 2


def test_unicodefix():
    assert unicodefix("éparpiller") == "éparpiller"
