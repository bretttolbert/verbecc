from typing import Dict

from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.language_codes import LangISOCode639_1

MOOD_MAP: Dict[Mood, Dict[LangISOCode639_1, Mood]] = {
    Mood.En.Indicative: {
        LangISOCode639_1.Ca: Mood.Ca.Indicatiu,
        LangISOCode639_1.Es: Mood.Es.Indicativo,
        LangISOCode639_1.Fr: Mood.Fr.Indicatif,
        LangISOCode639_1.It: Mood.It.Indicativo,
        LangISOCode639_1.Pt: Mood.Pt.Indicativo,
        LangISOCode639_1.Ro: Mood.Ro.Indicativ,
    },
    Mood.En.Subjunctive: {
        LangISOCode639_1.Ca: Mood.Ca.Subjuntiu,
        LangISOCode639_1.Es: Mood.Es.Subjuntivo,
        LangISOCode639_1.Fr: Mood.Fr.Subjonctif,
        LangISOCode639_1.It: Mood.It.Congiuntivo,
        LangISOCode639_1.Pt: Mood.Pt.Subjuntivo,
        LangISOCode639_1.Ro: Mood.Ro.Subjunctiv,
    },
    Mood.En.Imperative: {
        LangISOCode639_1.Ca: Mood.Ca.Imperatiu,
        LangISOCode639_1.Es: Mood.Es.Imperativo,
        LangISOCode639_1.Fr: Mood.Fr.Imperatif,
        LangISOCode639_1.It: Mood.It.Imperativo,
        LangISOCode639_1.Pt: Mood.Pt.Imperativo,
        LangISOCode639_1.Ro: Mood.Ro.Imperativ,
    },
    Mood.En.Conditional: {
        LangISOCode639_1.Ca: Mood.Ca.Condicional,
        LangISOCode639_1.Es: Mood.Es.Condicional,
        LangISOCode639_1.Fr: Mood.Fr.Conditionnel,
        LangISOCode639_1.It: Mood.It.Condizionale,
        LangISOCode639_1.Pt: Mood.Pt.Condicional,
        LangISOCode639_1.Ro: "<not implemented>",  # The conditional mood is formed by combining the conditional particle "ar" with the infinitive form of the verb
    },
    Mood.En.Infinitive: {
        LangISOCode639_1.Ca: Mood.Ca.Infinitiu,
        LangISOCode639_1.Es: Mood.Es.Infinitivo,
        LangISOCode639_1.Fr: Mood.Fr.Infinitif,
        LangISOCode639_1.It: Mood.It.Infinito,
        LangISOCode639_1.Pt: Mood.Pt.Infinitivo,
        LangISOCode639_1.Ro: Mood.Ro.Infinitiv,
    },
    # TODO: Make French consistent with other languages i.e.
    # make gerund and past-participle different moods i.e.
    # participe.participe-présent -> participe-présent.participe
    # participe.participe-passé -> participe-passé.participe
    Mood.En.Gerund: {
        LangISOCode639_1.Ca: Mood.Ca.Gerundi,  # gerundi.gerundi
        LangISOCode639_1.Es: Mood.Es.Gerundio,  # gerundio.gerundio
        LangISOCode639_1.Fr: Mood.Fr.Participe,  # participe.participe-présent is gerund in French
        LangISOCode639_1.It: Mood.It.Infinito,  # infinito.gerundio is gerund in Italian
        LangISOCode639_1.Pt: Mood.Pt.Gerúndio,  # gerúndio.gerúndio
        LangISOCode639_1.Ro: Mood.Ro.Gerunziu,  # gerunziu.gerunziu
    },
    Mood.En.Participle: {
        LangISOCode639_1.Ca: Mood.Ca.Participi,  # particip.particip
        LangISOCode639_1.Es: Mood.Es.Participo,  # participo.participo
        LangISOCode639_1.Fr: Mood.Fr.Participe,  # participe.participe-présent, participe.participe-passé
        LangISOCode639_1.It: Mood.It.Participio,  # participio.participio
        LangISOCode639_1.Pt: Mood.Pt.Particípio,  # particípio.particípio
        LangISOCode639_1.Ro: Mood.Ro.Participiu,  # participiu.participiu
    },
}

TENSE_MAP = {
    Tense.En.Present: {
        LangISOCode639_1.Ca: Tense.Ca.Present,
        LangISOCode639_1.Es: Tense.Es.Presente,
        LangISOCode639_1.Fr: Tense.Fr.Présent,
        LangISOCode639_1.It: Tense.It.Presente,
        LangISOCode639_1.Pt: Tense.Pt.Presente,
        LangISOCode639_1.Ro: Tense.Ro.Prezent,
    },
    Tense.En.Imperfect: {
        LangISOCode639_1.Ca: Tense.Ca.Imperfet,
        LangISOCode639_1.Es: Tense.Es.PretéritoImperfecto,
        LangISOCode639_1.Fr: Tense.Fr.Imparfait,
        LangISOCode639_1.It: Tense.It.Imperfetto,
        LangISOCode639_1.Pt: Tense.Pt.Imperfeito,
    },
    Tense.En.SimplePast: {
        LangISOCode639_1.Ca: Tense.Ca.PassatSimple,
        LangISOCode639_1.Es: Tense.Es.PretéritoPerfectoSimple,
        LangISOCode639_1.Fr: Tense.Fr.PasséSimple,
        LangISOCode639_1.It: Tense.It.PassatoRemoto,  # The passato prossimo (compound tense) is roughly equivalent to the present perfect and past simple tenses
        # however passato-remoto is the literal simple past tense e.g. 'io fui, tu fosti, lui fu, noi fummo',
        LangISOCode639_1.Pt: Tense.Pt.PretéritoPerfeito,
        LangISOCode639_1.Ro: Tense.Ro.PerfectSimplu,
    },
    Tense.En.Future: {
        LangISOCode639_1.Ca: Tense.Ca.Futur,
        LangISOCode639_1.Es: Tense.Es.Futuro,
        LangISOCode639_1.Fr: Tense.Fr.FuturSimple,
        LangISOCode639_1.It: Tense.It.Futuro,
        LangISOCode639_1.Pt: Tense.Pt.FuturoDoPresente,
        LangISOCode639_1.Ro: Tense.Ro.Viitor1,  # Romanian has viitor-1, viitor-2, viitor-1-popular, viitor-2-popular
    },
    Tense.En.Gerund: {
        LangISOCode639_1.Ca: Tense.Ca.Gerundi,
        LangISOCode639_1.Es: Tense.Es.Gerundio,
        LangISOCode639_1.Fr: Tense.Fr.ParticipePresent,  # TODO: Make French consistent
        LangISOCode639_1.It: Tense.It.Gerundio,
        LangISOCode639_1.Pt: Tense.Pt.Gerúndio,
        LangISOCode639_1.Ro: Tense.Ro.Gerunziu,
    },
    Tense.En.PastParticiple: {
        LangISOCode639_1.Ca: Tense.Ca.Particip,
        LangISOCode639_1.Es: Tense.Es.Participo,
        LangISOCode639_1.Fr: Tense.Fr.ParticipePassé,
        LangISOCode639_1.It: Tense.It.ParticipioPassato,
        LangISOCode639_1.Pt: Tense.Pt.Particípio,
        LangISOCode639_1.Ro: Tense.Ro.Participiu,
    },
}


def xmood(lang: LangISOCode639_1, m: Mood) -> Mood:
    """Takes a mood name in EN and translates it to the specified language

    :raises: Exception if mood or lang doesn't exist
    """
    return MOOD_MAP[m][lang]


def xtense(lang: LangISOCode639_1, t: Tense) -> Tense:
    """Takes a tense name in EN and translates it to the specified language

    :raises: Exception if tense or lang doesn't exist
    """
    return TENSE_MAP[t][lang]
