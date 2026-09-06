"""
This module adds an ML-based conjugation template prediction
feature. E.g. given the infinitive form of a verb, it can accurately
predict which conjugation template the verb should be conjugated
with.

The code in this module is based on an early version of mlconjug by Sekou Diao:
https://github.com/SekouD/mlconjug
Sekou Diao notes that a newer version of mjconjug is now available (mlconjug3):
https://github.com/SekouDiaoNlp/mlconjug3
https://github.com/Ars-Linguistica/mlconjug3

However I have made some changes:
- Updated to use importlib_resources instead of the deprecated pkg_resources API
    (the last time I checked mlconjug3 was still using pkg_resources)
- Added type annotations and reorganized the source into mutiple source files

A bit of history:
verbecc predates mlconjug and verbecc's verb conjugation implementation
was developed independently of mlconjug, but credit to Sekou Diao for the ML
template prediction code in this module and for and the XML conjugation templates
for languages other than French and Catalan.

Credit to Pierre Sarrazin (Verbiste) for the developing the original French
XML conjugation template format on which both verbecc and mlconjug are based.

I found mlconjug and was impressed by the machine learning feature and I
so I borrowed this feature and retrofit it onto verbecc.
I chose not to add the entire mlconjug python package as a dependency because
it duplicates much of the functionality of verbecc and would be redundant.
mlconjug and verbecc are independent projects and this file, based on the
origin mlconjug module, has diverged.

verbecc is Open Source Software (GNU LGPL license)
mlconjug is also Open Source Software (MIT license)
Verbiste is Open Source Software (GNU GPL license)

Copyright (c) 2026, Brett Tolbert <http://bretttolbert.com/>
Copyright (c) 2017, SekouD <https://github.com/SekouDiaoNlp/>
Copyright (c) 2003-2016, Pierre Sarrazin <http://sarrazip.com/>
"""

__author__ = ["Sekou Diao", "Brett Tolbert"]
__credits__ = ["Sekou Diao", "Pierre Sarrazin"]
