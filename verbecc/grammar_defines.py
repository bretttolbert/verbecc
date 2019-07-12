# -*- coding: utf-8 -*-

# This refers to grammatical person ('usted' is 3s despite being semantically 2p)
PERSONS = ('1s', '2s', '3s', '1p', '2p', '3p')

IMPERATIVE_PRESENT_PERSONS = ('2s', '1p', '2p')

PARTICIPLE_INFLECTIONS = ('ms', 'mp', 'fs', 'fp')

ALPHABET = {'fr': {'vowels': 'aáàâeêéèiîïoôöœuûùy',
                    'consonants': 'bcçdfghjklmnpqrstvwxyz'},
             'en': {'vowels': 'aeiouy',
                    'consonants': 'bcdfghjklmnpqrstvwxyz'},
             'es': {'vowels': 'aáeiíoóuúy',
                    'consonants': 'bcdfghjklmnñpqrstvwxyz'},
             'it': {'vowels': 'aàeéèiìîoóòuùy',
                    'consonants': 'bcdfghjklmnpqrstvwxyz'},
             'pt': {'vowels': 'aàãááeêéiíoóõuúy',
                    'consonants': 'bcçdfghjklmnpqrstvwxyz'},
             'ro': {'vowels': 'aăâeiîouy',
                    'consonants': 'bcdfghjklmnpqrsșştțţvwxyz'},
             }
