# verbecc Changelog

- 1.9.5 [24 December 2023]
  - Improved Catalan Support
    - Added more missing templates (5+)
    - TODO: Still missing 18 templates for 73 out of 8616 verbs
    - See `test_inflector_ca.test_all_verbs_have_templates`

- 1.9.4 [23 December 2023]
  - Improved Catalan Support
    - Added more missing templates (8+)
    - TODO: Still missing 26 templates for 172 out of 8616 verbs
    - See `test_inflector_ca.test_all_verbs_have_templates`

- 1.9.3 [22 December 2023]
  - Improved Catalan support
    - Added more missing verb conjugation templates
      - Can now conjugate 8578 verbs using 42 templates
      - TODO: Still missing 38 templates for 200+ verbs
      - See `test_inflector_ca.test_all_verbs_have_templates`
    - Made Catalan inflector template matching more loose
      - Added `verbecc.string_utils.get_common_letter_count`
      - Now matches if template ending has len()-1 chars in common with infinitive ending (not counting accents)
      - E.g. Not just `aure` and `eure` match, but also `çar` and `cer`
  - Enhanced conjugation template syntax: now supports stem-changing verbs through two new features:
    - 1. New stem-modifying XML attribute: `modify-stem="strip-accents"`
    - 2. Stem-modifying delete operator '`-`'
    - e.g. 
    ```xml
    <template name="conèix:er" modify-stem="strip-accents">
    		<passat-simple>
			<p><i>--guí</i></p>
    ```
    - With the above template, `conèix` + `--guí` = `jo coneguí` and `reconèix` + `--guí` = `jo reconeguí`
  - Added `gender` flag to support feminine pronouns
  - Modified to put `-` placeholder in conjugation for tenses that aren't conjugated e.g.
  ```python
    "caldre",
    "indicatiu",
    "present",
    False,
    "f",
    [
        "-",
        "-",
        "ella cal",
        "-",
        "-",
        "elles calen",
    ]
  ```

- 1.9.2 [17 December 2023]
  - Fixed bug in new `localization` module
  - Renamed `localize_mood` and `localize_tense` to `xmood` and `xtense`
  - Added `localization` example
  - Fixed Catalan verbs: mentir, pagar, naixer, néixer
  - Ran autoformatter

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
