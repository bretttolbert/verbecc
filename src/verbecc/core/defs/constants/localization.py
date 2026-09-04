from typing import Dict

from verbecc.core.defs.types.mood import Mood, Moods
from verbecc.core.defs.types.tense import Tense, Tenses
from verbecc.core.defs.types.lang_code import LangCodeISO639_1

MOOD_MAP: dict[Mood, dict[LangCodeISO639_1, Mood]] = {
    Moods.en.Indicative: {
        LangCodeISO639_1.ca: Moods.ca.Indicatiu,
        LangCodeISO639_1.es: Moods.es.Indicativo,
        LangCodeISO639_1.fr: Moods.fr.Indicatif,
        LangCodeISO639_1.it: Moods.it.Indicativo,
        LangCodeISO639_1.pt: Moods.pt.Indicativo,
        LangCodeISO639_1.ro: Moods.ro.Indicativ,
    },
    Moods.en.Subjunctive: {
        LangCodeISO639_1.ca: Moods.ca.Subjuntiu,
        LangCodeISO639_1.es: Moods.es.Subjuntivo,
        LangCodeISO639_1.fr: Moods.fr.Subjonctif,
        LangCodeISO639_1.it: Moods.it.Congiuntivo,
        LangCodeISO639_1.pt: Moods.pt.Subjuntivo,
        LangCodeISO639_1.ro: Moods.ro.Subjunctiv,
    },
    Moods.en.Imperative: {
        LangCodeISO639_1.ca: Moods.ca.Imperatiu,
        LangCodeISO639_1.es: Moods.es.Imperativo,
        LangCodeISO639_1.fr: Moods.fr.Imperatif,
        LangCodeISO639_1.it: Moods.it.Imperativo,
        LangCodeISO639_1.pt: Moods.pt.Imperativo,
        LangCodeISO639_1.ro: Moods.ro.Imperativ,
    },
    Moods.en.Conditional: {
        LangCodeISO639_1.ca: Moods.ca.Condicional,
        LangCodeISO639_1.es: Moods.es.Condicional,
        LangCodeISO639_1.fr: Moods.fr.Conditionnel,
        LangCodeISO639_1.it: Moods.it.Condizionale,
        LangCodeISO639_1.pt: Moods.pt.Condicional,
        LangCodeISO639_1.ro: Moods.ro.NA,  # The conditional mood is formed by combining the conditional particle "ar" with the infinitive form of the verb
    },
    Moods.en.Infinitive: {
        LangCodeISO639_1.ca: Moods.ca.Infinitiu,
        LangCodeISO639_1.es: Moods.es.Infinitivo,
        LangCodeISO639_1.fr: Moods.fr.Infinitif,
        LangCodeISO639_1.it: Moods.it.Infinito,
        LangCodeISO639_1.pt: Moods.pt.Infinitivo,
        LangCodeISO639_1.ro: Moods.ro.Infinitiv,
    },
    # TODO: Make French consistent with other languages i.e.
    # make gerund and past-participle different moods i.e.
    # participe.participe-présent -> participe-présent.participe
    # participe.participe-passé -> participe-passé.participe
    Moods.en.Gerund: {
        LangCodeISO639_1.ca: Moods.ca.Gerundi,  # gerundi.gerundi
        LangCodeISO639_1.es: Moods.es.Gerundio,  # gerundio.gerundio
        LangCodeISO639_1.fr: Moods.fr.Participe,  # participe.participe-présent is gerund in French
        LangCodeISO639_1.it: Moods.it.Infinito,  # infinito.gerundio is gerund in Italian
        LangCodeISO639_1.pt: Moods.pt.Gerúndio,  # gerúndio.gerúndio
        LangCodeISO639_1.ro: Moods.ro.Gerunziu,  # gerunziu.gerunziu
    },
    Moods.en.Participle: {
        LangCodeISO639_1.ca: Moods.ca.Participi,  # particip.particip
        LangCodeISO639_1.es: Moods.es.Participo,  # participo.participo
        LangCodeISO639_1.fr: Moods.fr.Participe,  # participe.participe-présent, participe.participe-passé
        LangCodeISO639_1.it: Moods.it.Participio,  # participio.participio
        LangCodeISO639_1.pt: Moods.pt.Particípio,  # particípio.particípio
        LangCodeISO639_1.ro: Moods.ro.Participiu,  # participiu.participiu
    },
}

TENSE_MAP: dict[Tense, dict[LangCodeISO639_1, Tense]] = {
    Tenses.en.Present: {
        LangCodeISO639_1.ca: Tenses.ca.Present,
        LangCodeISO639_1.es: Tenses.es.Presente,
        LangCodeISO639_1.fr: Tenses.fr.Présent,
        LangCodeISO639_1.it: Tenses.it.Presente,
        LangCodeISO639_1.pt: Tenses.pt.Presente,
        LangCodeISO639_1.ro: Tenses.ro.Prezent,
    },
    Tenses.en.Imperfect: {
        LangCodeISO639_1.ca: Tenses.ca.Imperfet,
        LangCodeISO639_1.es: Tenses.es.PretéritoImperfecto,
        LangCodeISO639_1.fr: Tenses.fr.Imparfait,
        LangCodeISO639_1.it: Tenses.it.Imperfetto,
        LangCodeISO639_1.pt: Tenses.pt.Imperfeito,
    },
    Tenses.en.PastSimple: {
        LangCodeISO639_1.ca: Tenses.ca.PassatSimple,
        LangCodeISO639_1.es: Tenses.es.PretéritoPerfectoSimple,
        LangCodeISO639_1.fr: Tenses.fr.PasséSimple,
        LangCodeISO639_1.it: Tenses.it.PassatoRemoto,  # The passato prossimo (compound tense) is roughly equivalent to the present perfect and past simple tenses
        # however passato-remoto is the literal simple past tense e.g. 'io fui, tu fosti, lui fu, noi fummo',
        LangCodeISO639_1.pt: Tenses.pt.PretéritoPerfeito,
        LangCodeISO639_1.ro: Tenses.ro.PerfectSimplu,
    },
    Tenses.en.Future: {
        LangCodeISO639_1.ca: Tenses.ca.Futur,
        LangCodeISO639_1.es: Tenses.es.Futuro,
        LangCodeISO639_1.fr: Tenses.fr.FuturSimple,
        LangCodeISO639_1.it: Tenses.it.Futuro,
        LangCodeISO639_1.pt: Tenses.pt.FuturoDoPresente,
        LangCodeISO639_1.ro: Tenses.ro.Viitor1,  # Romanian has viitor-1, viitor-2, viitor-1-popular, viitor-2-popular
    },
    Tenses.en.Gerund: {
        LangCodeISO639_1.ca: Tenses.ca.Gerundi,
        LangCodeISO639_1.es: Tenses.es.Gerundio,
        LangCodeISO639_1.fr: Tenses.fr.ParticipePresent,  # TODO: Make French consistent
        LangCodeISO639_1.it: Tenses.it.Gerundio,
        LangCodeISO639_1.pt: Tenses.pt.Gerúndio,
        LangCodeISO639_1.ro: Tenses.ro.Gerunziu,
    },
    Tenses.en.PastParticiple: {
        LangCodeISO639_1.ca: Tenses.ca.Participi,
        LangCodeISO639_1.es: Tenses.es.Participo,
        LangCodeISO639_1.fr: Tenses.fr.ParticipePassé,
        LangCodeISO639_1.it: Tenses.it.ParticipioPassato,
        LangCodeISO639_1.pt: Tenses.pt.Particípio,
        LangCodeISO639_1.ro: Tenses.ro.Participiu,
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
