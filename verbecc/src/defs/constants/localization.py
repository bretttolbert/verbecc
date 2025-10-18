from typing import Dict

from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.language import Language

MOOD_MAP: Dict[Mood, Dict[Language, Mood]] = {
    Mood.En.Indicative: {
        Language.Català: Mood.Ca.Indicatiu,
        Language.Español: Mood.Es.Indicativo,
        Language.Français: Mood.Fr.Indicatif,
        Language.Italiano: Mood.It.Indicativo,
        Language.Português: Mood.Pt.Indicativo,
        Language.Română: Mood.Ro.Indicativ,
    },
    Mood.En.Subjunctive: {
        Language.Català: Mood.Ca.Subjuntiu,
        Language.Español: Mood.Es.Subjuntivo,
        Language.Français: Mood.Fr.Subjonctif,
        Language.Italiano: Mood.It.Congiuntivo,
        Language.Português: Mood.Pt.Subjuntivo,
        Language.Română: Mood.Ro.Subjunctiv,
    },
    Mood.En.Imperative: {
        Language.Català: Mood.Ca.Imperatiu,
        Language.Español: Mood.Es.Imperativo,
        Language.Français: Mood.Fr.Imperatif,
        Language.Italiano: Mood.It.Imperativo,
        Language.Português: Mood.Pt.Imperativo,
        Language.Română: Mood.Ro.Imperativ,
    },
    Mood.En.Conditional: {
        Language.Català: Mood.Ca.Condicional,
        Language.Español: Mood.Es.Condicional,
        Language.Français: Mood.Fr.Conditionnel,
        Language.Italiano: Mood.It.Condizionale,
        Language.Português: Mood.Pt.Condicional,
        Language.Română: "<not implemented>",  # The conditional mood is formed by combining the conditional particle "ar" with the infinitive form of the verb
    },
    Mood.En.Infinitive: {
        Language.Català: Mood.Ca.Infinitiu,
        Language.Español: Mood.Es.Infinitivo,
        Language.Français: Mood.Fr.Infinitif,
        Language.Italiano: Mood.It.Infinito,
        Language.Português: Mood.Pt.Infinitivo,
        Language.Română: Mood.Ro.Infinitiv,
    },
    # TODO: Make French consistent with other languages i.e.
    # make gerund and past-participle different moods i.e.
    # participe.participe-présent -> participe-présent.participe
    # participe.participe-passé -> participe-passé.participe
    Mood.En.Gerund: {
        Language.Català: Mood.Ca.Gerundi,  # gerundi.gerundi
        Language.Español: Mood.Es.Gerundio,  # gerundio.gerundio
        Language.Français: Mood.Fr.Participe,  # participe.participe-présent is gerund in French
        Language.Italiano: Mood.It.Infinito,  # infinito.gerundio is gerund in Italian
        Language.Português: Mood.Pt.Gerúndio,  # gerúndio.gerúndio
        Language.Română: Mood.Ro.Gerunziu,  # gerunziu.gerunziu
    },
    Mood.En.Participle: {
        Language.Català: Mood.Ca.Participi,  # particip.particip
        Language.Español: Mood.Es.Participo,  # participo.participo
        Language.Français: Mood.Fr.Participe,  # participe.participe-présent, participe.participe-passé
        Language.Italiano: Mood.It.Participio,  # participio.participio
        Language.Português: Mood.Pt.Particípio,  # particípio.particípio
        Language.Română: Mood.Ro.Participiu,  # participiu.participiu
    },
}

TENSE_MAP = {
    Tense.En.Present: {
        Language.Català: Tense.Ca.Present,
        Language.Español: Tense.Es.Presente,
        Language.Français: Tense.Fr.Présent,
        Language.Italiano: Tense.It.Presente,
        Language.Português: Tense.Pt.Presente,
        Language.Română: Tense.Ro.Prezent,
    },
    Tense.En.Imperfect: {
        Language.Català: Tense.Ca.Imperfet,
        Language.Español: Tense.Es.PretéritoImperfecto,
        Language.Français: Tense.Fr.Imparfait,
        Language.Italiano: Tense.It.Imperfetto,
        Language.Português: Tense.Pt.Imperfeito,
    },
    Tense.En.SimplePast: {
        Language.Català: Tense.Ca.PassatSimple,
        Language.Español: Tense.Es.PretéritoPerfectoSimple,
        Language.Français: Tense.Fr.PasséSimple,
        Language.Italiano: Tense.It.PassatoRemoto,  # The passato prossimo (compound tense) is roughly equivalent to the present perfect and past simple tenses
        # however passato-remoto is the literal simple past tense e.g. 'io fui, tu fosti, lui fu, noi fummo',
        Language.Português: Tense.Pt.PretéritoPerfeito,
        Language.Română: Tense.Ro.PerfectSimplu,
    },
    Tense.En.Future: {
        Language.Català: Tense.Ca.Futur,
        Language.Español: Tense.Es.Futuro,
        Language.Français: Tense.Fr.FuturSimple,
        Language.Italiano: Tense.It.Futuro,
        Language.Português: Tense.Pt.FuturoDoPresente,
        Language.Română: Tense.Ro.Viitor1,  # Romanian has viitor-1, viitor-2, viitor-1-popular, viitor-2-popular
    },
    Tense.En.Gerund: {
        Language.Català: Tense.Ca.Gerundi,
        Language.Español: Tense.Es.Gerundio,
        Language.Français: Tense.Fr.ParticipePresent,  # TODO: Make French consistent
        Language.Italiano: Tense.It.Gerundio,
        Language.Português: Tense.Pt.Gerúndio,
        Language.Română: Tense.Ro.Gerunziu,
    },
    Tense.En.PastParticiple: {
        Language.Català: Tense.Ca.Particip,
        Language.Español: Tense.Es.Participo,
        Language.Français: Tense.Fr.ParticipePassé,
        Language.Italiano: Tense.It.ParticipioPassato,
        Language.Português: Tense.Pt.Particípio,
        Language.Română: Tense.Ro.Participiu,
    },
}


def xmood(lang, m):
    """Takes a mood name in English and translates it to the specified language

    :raises: Exception if mood or lang doesn't exist
    """
    return MOOD_MAP[m][lang]


def xtense(lang, t):
    """Takes a tense name in English and translates it to the specified language

    :raises: Exception if tense or lang doesn't exist
    """
    return TENSE_MAP[t][lang]
