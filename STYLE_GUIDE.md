# verbecc Style Guide

## The Python `@property` decorator shall not be used

This is primarily because I intend to port verbecc to Java and other languages and I wish to keep the implementations as consistent as possible, preferably a _1:1_ equivalence in all symbol names, _mutata mutandis_.

## There shall not be more than class definition per file

This simplifies porting to Java, allowing _1:1_ source file correspondence. This rule is enforced by the `test_ast` unit-tests.

## Type annotations are required for all parameters and return statements

This rule is enforced by the `test_ast` unit-tests.

## Don't use parentheses in import statements

Without parentheses, I can easily sort the import statements (_Ctrl+P Sort Lines Ascending_), 
but with parentheses, I can't do that.

Do this:
```python
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptionsEs
from verbecc.src.defs.types.lang_specific_options import LangSpecificOptionsFactory
from verbecc.src.defs.types.lang_specific_options import VoseoOptions
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.utils.string_utils import strip_accents
```

Don't do this:
```python
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
    LangSpecificOptionsEs,
    LangSpecificOptionsFactory,
    VoseoOptions,
)
from verbecc.src.defs.types.mood import Mood, Moods
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.tense import Tense, Tenses
from verbecc.src.inflectors.inflector import Inflector
from verbecc.src.utils.string_utils import strip_accents
```