# verbecc Changelog

- 1.9.1 [17 December 2023]
  - Renamed Catalan 'preterit' to 'passat-simple'
  - Cont. added more missing conjugation templates for Catalan, decent support for most Catalan verbs now
  - Added `localization` module with localization functions `localize_mood` and `localize_tense`
  - Removed pre-generated model .zip files
  - Added dummy file in models directory as workaround for installation issue
  - fixed KeyError with Spanish verb abolir

- 1.9.0 [December 2023]
  - Added limited support for Catalan language
  - Please help improve support for Catalan verb conjugation, PRs welcome
  - Modernization: added type hints
  - Modernization: switched from setup.py to pyproject.toml
  - Updated dependencies (scikit-learn, etc.)
  - Now targetting Python 3.11

- 1.8.1 [28 December 2022]
  - Updated from Python 3.7 to Python 3.10
  - Updated dependencies
  - Increased SGDClassifier max_iter from 4000 to 40000
  - Regenerated models
