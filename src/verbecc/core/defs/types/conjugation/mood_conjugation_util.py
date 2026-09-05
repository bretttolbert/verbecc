from verbecc.core.defs.types.conjugation.mood_conjugation import MoodConjugation
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.tense import Tense


class MoodConjugationUtil:

    @classmethod
    def combine(cls, a: MoodConjugation, b: MoodConjugation) -> MoodConjugation:
        """
        I would have liked to have made this a method of class MoodConjugation,
        but that is problematic due to the way Python's type annotations work
        (MoodConjugation isn't defined until MoodConjugation is initialized).
        Putting it in a separate file seems preferable to casting.
        """
        if a.get_mood() != b.get_mood():
            raise TypeError("Cannot combine MoodsConjugations with different moods")
        combined: dict[Tense, TenseConjugation] = {
            tense: a[tense] for tense in a.get_data()
        }
        combined.update({tense: b[tense] for tense in b.get_data()})
        return MoodConjugation(a.get_mood(), combined)
