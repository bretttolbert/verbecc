from verbecc.core.conjugator.complete_conjugator import CompleteConjugator
from verbecc.core.defs.constants.grammar_defines import SUPPORTED_LANGUAGES


def train_models() -> None:
    print("Begin model training")
    for i, lang in enumerate(SUPPORTED_LANGUAGES.keys()):
        print(f"Training model {i+1} of {len(SUPPORTED_LANGUAGES.keys())} lang={lang}")
        print("Please be patient, this could take a while...")
        ccg = CompleteConjugator(lang=lang)
        if lang == "fr":
            cc = ccg.conjugate("etre")
        elif lang == "it":
            cc = ccg.conjugate("essere")
        elif lang == "ro":
            cc = ccg.conjugate("fi")
        else:
            cc = ccg.conjugate("ser")
        print(f"lang={lang} cc={cc}")
        print(f"Finished training model lang={lang}")
    print("Model training complete")
