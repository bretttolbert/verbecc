from typing import Dict

from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.lang_code import LangCodeISO639_1

MOOD_MAP: Dict[Mood, Dict[LangCodeISO639_1, Mood]] = {
    Mood.en.Indicative: {
        LangCodeISO639_1.ca: Mood.ca.Indicatiu,
        LangCodeISO639_1.es: Mood.es.Indicativo,
        LangCodeISO639_1.fr: Mood.fr.Indicatif,
        LangCodeISO639_1.it: Mood.it.Indicativo,
        LangCodeISO639_1.pt: Mood.pt.Indicativo,
        LangCodeISO639_1.ro: Mood.ro.Indicativ,
    },
    Mood.en.Subjunctive: {
        LangCodeISO639_1.ca: Mood.ca.Subjuntiu,
        LangCodeISO639_1.es: Mood.es.Subjuntivo,
        LangCodeISO639_1.fr: Mood.fr.Subjonctif,
        LangCodeISO639_1.it: Mood.it.Congiuntivo,
        LangCodeISO639_1.pt: Mood.pt.Subjuntivo,
        LangCodeISO639_1.ro: Mood.ro.Subjunctiv,
    },
    Mood.en.Imperative: {
        LangCodeISO639_1.ca: Mood.ca.Imperatiu,
        LangCodeISO639_1.es: Mood.es.Imperativo,
        LangCodeISO639_1.fr: Mood.fr.Imperatif,
        LangCodeISO639_1.it: Mood.it.Imperativo,
        LangCodeISO639_1.pt: Mood.pt.Imperativo,
        LangCodeISO639_1.ro: Mood.ro.Imperativ,
    },
    Mood.en.Conditional: {
        LangCodeISO639_1.ca: Mood.ca.Condicional,
        LangCodeISO639_1.es: Mood.es.Condicional,
        LangCodeISO639_1.fr: Mood.fr.Conditionnel,
        LangCodeISO639_1.it: Mood.it.Condizionale,
        LangCodeISO639_1.pt: Mood.pt.Condicional,
        LangCodeISO639_1.ro: "<not implemented>",  # The conditional mood is formed by combining the conditional particle "ar" with the infinitive form of the verb
    },
    Mood.en.Infinitive: {
        LangCodeISO639_1.ca: Mood.ca.Infinitiu,
        LangCodeISO639_1.es: Mood.es.Infinitivo,
        LangCodeISO639_1.fr: Mood.fr.Infinitif,
        LangCodeISO639_1.it: Mood.it.Infinito,
        LangCodeISO639_1.pt: Mood.pt.Infinitivo,
        LangCodeISO639_1.ro: Mood.ro.Infinitiv,
    },
    # TODO: Make French consistent with other languages i.e.
    # make gerund and past-participle different moods i.e.
    # participe.participe-présent -> participe-présent.participe
    # participe.participe-passé -> participe-passé.participe
    Mood.en.Gerund: {
        LangCodeISO639_1.ca: Mood.ca.Gerundi,  # gerundi.gerundi
        LangCodeISO639_1.es: Mood.es.Gerundio,  # gerundio.gerundio
        LangCodeISO639_1.fr: Mood.fr.Participe,  # participe.participe-présent is gerund in French
        LangCodeISO639_1.it: Mood.it.Infinito,  # infinito.gerundio is gerund in Italian
        LangCodeISO639_1.pt: Mood.pt.Gerúndio,  # gerúndio.gerúndio
        LangCodeISO639_1.ro: Mood.ro.Gerunziu,  # gerunziu.gerunziu
    },
    Mood.en.Participle: {
        LangCodeISO639_1.ca: Mood.ca.Participi,  # particip.particip
        LangCodeISO639_1.es: Mood.es.Participo,  # participo.participo
        LangCodeISO639_1.fr: Mood.fr.Participe,  # participe.participe-présent, participe.participe-passé
        LangCodeISO639_1.it: Mood.it.Participio,  # participio.participio
        LangCodeISO639_1.pt: Mood.pt.Particípio,  # particípio.particípio
        LangCodeISO639_1.ro: Mood.ro.Participiu,  # participiu.participiu
    },
}

TENSE_MAP = {
    Tense.en.Present: {
        LangCodeISO639_1.ca: Tense.ca.Present,
        LangCodeISO639_1.es: Tense.es.Presente,
        LangCodeISO639_1.fr: Tense.fr.Présent,
        LangCodeISO639_1.it: Tense.it.Presente,
        LangCodeISO639_1.pt: Tense.pt.Presente,
        LangCodeISO639_1.ro: Tense.ro.Prezent,
    },
    Tense.en.Imperfect: {
        LangCodeISO639_1.ca: Tense.ca.Imperfet,
        LangCodeISO639_1.es: Tense.es.PretéritoImperfecto,
        LangCodeISO639_1.fr: Tense.fr.Imparfait,
        LangCodeISO639_1.it: Tense.it.Imperfetto,
        LangCodeISO639_1.pt: Tense.pt.Imperfeito,
    },
    Tense.en.SimplePast: {
        LangCodeISO639_1.ca: Tense.ca.PassatSimple,
        LangCodeISO639_1.es: Tense.es.PretéritoPerfectoSimple,
        LangCodeISO639_1.fr: Tense.fr.PasséSimple,
        LangCodeISO639_1.it: Tense.it.PassatoRemoto,  # The passato prossimo (compound tense) is roughly equivalent to the present perfect and past simple tenses
        # however passato-remoto is the literal simple past tense e.g. 'io fui, tu fosti, lui fu, noi fummo',
        LangCodeISO639_1.pt: Tense.pt.PretéritoPerfeito,
        LangCodeISO639_1.ro: Tense.ro.PerfectSimplu,
    },
    Tense.en.Future: {
        LangCodeISO639_1.ca: Tense.ca.Futur,
        LangCodeISO639_1.es: Tense.es.Futuro,
        LangCodeISO639_1.fr: Tense.fr.FuturSimple,
        LangCodeISO639_1.it: Tense.it.Futuro,
        LangCodeISO639_1.pt: Tense.pt.FuturoDoPresente,
        LangCodeISO639_1.ro: Tense.ro.Viitor1,  # Romanian has viitor-1, viitor-2, viitor-1-popular, viitor-2-popular
    },
    Tense.en.Gerund: {
        LangCodeISO639_1.ca: Tense.ca.Gerundi,
        LangCodeISO639_1.es: Tense.es.Gerundio,
        LangCodeISO639_1.fr: Tense.fr.ParticipePresent,  # TODO: Make French consistent
        LangCodeISO639_1.it: Tense.it.Gerundio,
        LangCodeISO639_1.pt: Tense.pt.Gerúndio,
        LangCodeISO639_1.ro: Tense.ro.Gerunziu,
    },
    Tense.en.PastParticiple: {
        LangCodeISO639_1.ca: Tense.ca.Particip,
        LangCodeISO639_1.es: Tense.es.Participo,
        LangCodeISO639_1.fr: Tense.fr.ParticipePassé,
        LangCodeISO639_1.it: Tense.it.ParticipioPassato,
        LangCodeISO639_1.pt: Tense.pt.Particípio,
        LangCodeISO639_1.ro: Tense.ro.Participiu,
    },
}


def xmood(lang: LangCodeISO639_1, m: Mood) -> Mood:
    """Takes a mood name in EN and translates it to the specified language

    :raises: Exception if mood or lang doesn't exist
    """
    return MOOD_MAP[m][lang]


def xtense(lang: LangCodeISO639_1, t: Tense) -> Tense:
    """Takes a tense name in EN and translates it to the specified language

    :raises: Exception if tense or lang doesn't exist
    """
    return TENSE_MAP[t][lang]
