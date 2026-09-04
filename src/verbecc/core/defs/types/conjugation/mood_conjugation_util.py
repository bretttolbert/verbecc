from verbecc.core.defs.types.conjugation.mood_conjugation import MoodConjugation


class MoodConjugationUtil:

    @classmethod
    def combine(cls, a: MoodConjugation, b: MoodConjugation) -> MoodConjugation:
        """
        I would have liked to have made this a method of class MoodConjugation,
        but that is problematic due to the way Python's type annotations work
        (MoodConjugation isn't defined until MoodConjugation is initialized).
        Putting it in a separate file seems preferable to casting.
        """
        if a._mood != b._mood:
            raise TypeError("Cannot combine MoodsConjugations with different moods")
        combined = {}
        for mc in (a, b):
            combined.update(mc._data)
        return MoodConjugation(a._mood, combined)
