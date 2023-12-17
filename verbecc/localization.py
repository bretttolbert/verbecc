
MOOD_MAP = {
    'indicative': {
            'ca': 'indicatiu',
            'es': 'indicativo',
            'fr': 'indicatif',
            'it': 'indicativo',
            'pt': 'indicativo',
            'ro': 'indicativ'
    },
    'subjunctive': {
        'ca': 'subjuntiu',
        'es': 'subjuntivo',
        'fr': 'subjonctif',
        'it': 'congiuntivo',
        'pt': 'subjuntivo',
        'ro': 'conjunctiv'
    },
    'imperative': {
        'ca': 'imperatiu',
        'es': 'imperativo',
        'fr': 'imperatif',
        'it': 'imperativo',
        'pt': 'imperativo',
        'ro': 'imperativ'
    },
    'conditional': {
        'ca': 'condicional',
        'es': 'condicional',
        'fr': 'conditionnel',
        'it': 'condizionale',
        'pt': 'condicional',
        'ro': '<not implemented>' # The conditional mood is formed by combining the conditional particle "ar" with the infinitive form of the verb 
    },
    'infinitive': {
        'ca': 'infinitiu',
        'es': 'infinitivo',
        'fr': 'infinitif',
        'it': 'infinito',
        'pt': 'infinitivo',
        'ro': 'infinitiv'
    },
    # TODO: Make French consistent with other languages i.e.
    # make gerund and past-participle different moods i.e.
    # participe.participe-présent -> participe-présent.participe
    # participe.participe-passé -> participe-passé.participe
    'gerund': {
        'ca': 'gerundi', # gerundi.gerundi
        'es': 'gerundio', # gerundio.gerundio
        'fr': 'participe',  # participe.participe-présent is gerund in French
        'it': 'infinito', # infinito.gerundio is gerund in Italian
        'pt': 'gerúndio', # gerúndio.gerúndio
        'ro': 'gerunziu' # gerunziu.gerunziu
    },
    'participle': {
        'ca': 'particip', # particip.particip
        'es': 'participo', # participo.participo
        'fr': 'participe', # participe.participe-présent, participe.participe-passé
        'it': 'participio', # participio.participio
        'pt': 'particípio', # particípio.particípio
        'ro': 'participiu' # participiu.participiu
    }
}

TENSE_MAP = {
    'present': {
        'ca': 'present',
        'es': 'presente',
        'fr': 'présent',
        'fr': 'indicatif',
        'it': 'presente',
        'pt': 'presente',
        'ro': 'prezent'
    },
    'imperfect': {
        'ca': 'imperfet',
        'es': 'pretérito-imperfecto',
        'fr': 'imparfait',
        'it': 'imperfetto',
        'pt': 'pretérito-imperfeito'
    },
    'simple-past': {
        'ca': 'pretèrit',
        'es': 'pretérito-perfecto-simple',
        'fr': 'passé-simple',
        'it': 'passato-remoto',
        'pt': 'pretérito-perfeito',
        'ro': 'perfect-simplu'
    },
    'future': {
        'ca': 'futur',
        'es': 'futuro',
        'fr': 'futur-simple',
        'it': 'futuro',
        'pt': 'futuro-do-presente',
        'ro': 'viitor-1' # Romanian has viitor-1, viitor-2, viitor-1-popular, viitor-2-popular
    },
    'gerund': {
        'ca': 'gerundi',
        'es': 'gerundio',
        'fr': 'participe-présent',
        'it': 'gerundio',
        'pt': 'gerúndio',
        'ro': 'gerunziu'
    },
    'past-participle': {
        'ca': 'particip',
        'es': 'participo',
        'fr': 'participe-passé',
        'it': 'participio',
        'pt': 'particípio',
        'ro': 'participiu'
    }
}

def localize_mood(lang, m):
    """Takes a mood name in English and converts to the specified language
    
    :raises: Exception if it doesn't exist
    """
    return MOOD_MAP[m]

def localize_tense(lang, t):
    """Takes a tense name in English and converts to the specified language
    
    :raises: Exception if it doesn't exist
    """
    return TENSE_MAP[t]
