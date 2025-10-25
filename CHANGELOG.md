# verbecc Changelog

- 1.11.5 [24 October 2025]
  - Fixed Spanish Voseo imperativo

- 1.11.4 [24 October 2025]
  - Added support for Spanish Voseo

- 1.11.3 [19 October 2025]
  - improved typing
  - changed `Language` enum to `LangCodeISO639_1`

- 1.12.2 [17 October 2025]
  - Added typing for mood and tense using `StrEnum` (backwards-compatible with string values)
  - Fixed typo in new `Language` enum
  - Corrected Romanian conditional tense spelling from `conditional` to `condițional`

- 1.11.1 [13 October 2025]
  - Fixed issues with Italian
  - Further typing improvements
  - Added `gender` option to top-level `conjugate` method

- 1.11.0 [12 October 2025]
  - (mega refactor)
  - **Changes should be transparent to users of top level `Conjugator.conjugate` function, however in sub-level conjugate methods the `alternate: bool` parameter has been replaced with the `alternate_options: AlternateOptions` parameter.**
  - **Officially dropping support for python <=3.8. Python 3.8 has been EOL for over a year now. Update to python 3.9 or later. Now supporting Python 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14.**
  - Significant refactoring
      - Eliminated a lot of code duplication introduced during initial implementation of `include_alternates` option
      - Moved most language-specific conjugation logic into the `Inflector` sub-classes
      - Moved most language-agnostic conjugation logic into `Conjugator`
  - Improved typing, now have typehint definitions for all returned data structures
  - Organized source tree into subdirectories
  - Added fixtures to optimize unit tests
  - Updated dependencies

- 1.10.5 [5 October 2025]
  - Fixed issue #26 (issue with compound verb conjugations with `include_alternates=True`)

- 1.10.4
  - Improved French conjugation templates

- 1.10.3 [28 September 2025]
  - GitLab actions integration
  - added `importlib_resources` to `requirements.txt`

- 1.10.2 [28 September 2025]
  - Improved Italian conjugation template (split participle into _presente_ and _passato_)
  - Improved Italian conjugation (verbs conjugated with _essere_)

- 1.10.1 [28 September 2025]
  - Properly conjugate h non aspiré en FR
  - Reverted back to uncompressed XML files

- 1.10.0 [28 September 2025]
  - Switched from deprecated `pkg_resources` library to new `importlib_resources` library
  - Compressed XML files

- 1.9.7 [5 January 2024]
  - Added option to include alternate conjugations
  - Added option to not conjugate pronouns e.g. return _apprends_ rather than _j'apprends_
  - Example: `include_alternates=False, conjugate_pronouns=True` (equivalent to classic verbecc behavior)
    ```json
                "condicional": {
                    "present": [
                        "jo seria",
                        "tu series",
                        "ell seria",
                        "nosaltres seríem",
                        "vosaltres seríeu",
                        "ells serien",
                    ]
                },
    ```
  - Example: `include_alternates=True, conjugate_pronouns=False` (observe now a list of one or more conjugations is returned in place of the scalar value)
    ```json
                "condicional": {
                    "present": [
                        ["seria", "fora"],
                        ["series", "fores"],
                        ["seria", "fora"],
                        ["seríem", "fórem"],
                        ["seríeu", "fóreu"],
                        ["serien", "foren"],
                    ]
                },
    ```

- 1.9.6 [26 December 2023]
  - Improved Catalan Support
    - Added remaining missing templates for all 8616 verbs
    - See `test_inflector_ca.test_all_verbs_have_templates`

- 1.9.5 [24 December 2023]
  - Improved Catalan Support
    - Added more missing templates (7+)
    - TODO: Still missing 9 templates for 28 out of 8616 verbs
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
  - Added `gender` flag to support F pronouns
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
