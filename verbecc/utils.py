from verbecc import Conjugator, SUPPORTED_LANGUAGES


def train_models():
    print("Begin model training")
    for i, l in enumerate(SUPPORTED_LANGUAGES.keys()):
        print(f"Training model {i+1} of {len(SUPPORTED_LANGUAGES.keys())} lang={l}")
        print("Please be patient, this could take a while...")
        cg = Conjugator(lang=l)
        print(f"Finished training model lang={l}")
    print("Model training complete")
