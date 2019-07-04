from verbecc.mood import (
    is_valid_mood,
    is_valid_mood_tense
)


def test_is_valid_mood():
    assert is_valid_mood("indicative")
    assert not is_valid_mood("vindicative")


def test_is_valid_mood_tense():
    assert is_valid_mood_tense("indicative", "present")
    assert not is_valid_mood_tense("vindicative", "past")
    assert is_valid_mood_tense("participle", "present-participle")
    assert not is_valid_mood_tense("participle", "future-participle")
