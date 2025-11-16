from verbecc.src.conjugator.conjugator import Conjugator
from verbecc.src.defs.constants.grammar_defines import SUPPORTED_LANGUAGES


def train_models() -> None:
    print("Begin model training")
    for i, lang in enumerate(SUPPORTED_LANGUAGES.keys()):
        print(f"Training model {i+1} of {len(SUPPORTED_LANGUAGES.keys())} lang={lang}")
        print("Please be patient, this could take a while...")
        cg = Conjugator(lang=lang)
        if lang == "fr":
            cc = cg.conjugate("etre")
        elif lang == "it":
            cc = cg.conjugate("essere")
        elif lang == "ro":
            cc = cg.conjugate("fi")
        else:
            cc = cg.conjugate("ser")
        print(f"lang={lang} cc={cc}")
        print(f"Finished training model lang={lang}")
    print("Model training complete")
