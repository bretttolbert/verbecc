from verbecc.src.conjugator.conjugator import Conjugator, SUPPORTED_LANGUAGES


def train_models():
    print("Begin model training")
    for i, l in enumerate(SUPPORTED_LANGUAGES.keys()):
        print(f"Training model {i+1} of {len(SUPPORTED_LANGUAGES.keys())} lang={l}")
        print("Please be patient, this could take a while...")
        cg = Conjugator(lang=l)
        if l == "fr":
            c = cg.conjugate("etre")
        elif l == "it":
            c = cg.conjugate("essere")
        elif l == "ro":
            c = cg.conjugate("fi")
        else:
            c = cg.conjugate("ser")
        print(f"lang={l} {c}")
        print(f"Finished training model lang={l}")
    print("Model training complete")
