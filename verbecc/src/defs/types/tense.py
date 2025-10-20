import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class TenseEn(StrEnum):
    Future = "future"
    FuturePerfect = "future-perfect"
    Gerund = "gerund"
    ImperativePresent = "imperative-present"
    Imperfect = "imperfect"
    Indicative = "indicative"
    InfinitivePresent = "infinitive-present"
    PastParticiple = "past-participle"
    Pluperfect = "pluperfect"
    Present = "present"
    Preterite = "preterite"
    PreteriteAnterior = "preterite-anterior"
    PreteritePerfectCompound = "preterite-perfect-compound"
    PreteritePluperfect = "preterite-pluperfect"
    SimplePast = "simple-past"


class TenseCa(StrEnum):
    Futur = "futur"
    FuturPerfet = "futur-perfet"
    Gerundi = "gerundi"
    ImperatiuPresent = "imperatiu-present"
    Imperfet = "imperfect"
    Indicatiu = "indicatiu"
    InfinitiuPresent = "infinitiu-present"
    Particip = "particip"
    PassatSimple = "passat-simple"
    Pluscuamperfet = "pluscuamperfet"
    Present = "present"
    Pretèrit = "pretèrit"
    PretèritAnterior = "pretèrit-anterior"
    PretèritPerfetCompuest = "pretèrit-perfet-compuest"
    PretèritPluscuamperfet = "pretèrit-pluscuamperfet"


class TenseEs(StrEnum):
    Afirmativo = "afirmativo"
    Futuro = "futuro"
    FuturoPerfecto = "futuro-perfecto"
    Gerundio = "gerundio"
    Indicativo = "indicativo"
    Infinitivo = "infinitivo"
    Negativo = "negativo"
    Participo = "participo"
    Perfecto = "perfecto"
    Presente = "presente"
    PretéritoAnterior = "pretérito-anterior"
    PretéritoImperfecto = "pretérito-imperfecto"
    PretéritoImperfecto1 = "pretérito-imperfecto-1"
    PretéritoImperfecto2 = "pretérito-imperfecto-2"
    PretéritoPerfecto = "pretérito-perfecto"
    PretéritoPerfectoCompuesto = "pretérito-perfecto-compuesto"
    PretéritoPerfectoSimple = "pretérito-perfecto-simple"
    PretéritoPluscuamperfecto = "pretérito-pluscuamperfecto"
    PretéritoPluscuamperfecto1 = "pretérito-pluscuamperfecto-1"
    PretéritoPluscuamperfecto2 = "pretérito-pluscuamperfecto-2"


class TenseFr(StrEnum):
    FutureAntériuer = "futur-antérieur"
    FuturSimple = "futur-simple"
    Imparfait = "imparfait"
    ImperatifPassé = "imperatif-passé"
    ImperatifPrésent = "imperatif-présent"
    InfinitifPrésent = "infinitif-présent"
    ParticipePassé = "participe-passé"
    ParticipePresent = "participe-présent"
    Passé = "passé"
    PasséAntérieur = "passé-antérieur"
    PasséCompose = "passé-composé"
    PasséSimple = "passé-simple"
    PlusQueParfait = "plus-que-parfait"
    Présent = "présent"


class TenseIt(StrEnum):
    Affermativo = "affermativo"
    Futuro = "futuro"
    FuturoAnteriore = "futuro-anteriore"
    Gerundio = "gerundio"
    Imperfetto = "imperfetto"
    Infinitivo = "infinitivo"
    negativo = "negativo"
    Negativo = "Negativo"
    ParticipioPassato = "participio-passato"
    ParticipioPresente = "participio-presente"
    Passato = "passato"
    PassatoProssimo = "passato-prossimo"
    PassatoRemoto = "passato-remoto"
    Presente = "presente"
    Trapassato = "trapassato"
    TrapassatoProssimo = "trapassato-prossimo"
    TrapassatoRemoto = "trapassato-remoto"


class TensePt(StrEnum):
    Afirmativo = "afirmativo"
    Futuro = "futuro"
    FuturoComposto = "futuro-composto"
    FuturoDoPresente = "futuro-do-presente"
    FuturoDoPresenteComposto = "futuro-do-presente-composto"
    FuturoDoPretérito = "futuro-do-pretérito"
    FuturoDoPretéritoComposto = "futuro-do-pretérito-composto"
    FuturoPerfeito = "futuro-perfeito"
    Gerúndio = "gerúndio"
    ImperativoPresente = "imperativo-presente"
    Imperfeito = "imperfeito"
    Infinitivo = "infinitivo"
    InfinitivoPessoalComposto = "infinitivo-pessoal-composto"
    InfinitivoPessoalPresente = "infinitivo-pessoal-presente"
    InfinitivoPresente = "infinitivo-presente"
    Negativo = "negativo"
    Particípio = "particípio"
    ParticípioPassado = "particípio-passado"
    Presente = "presente"
    PretéritoImperfeito = "pretérito-imperfeito"
    PretéritoMaisQuePerfeito = "pretérito-mais-que-perfeito"
    PretéritoMaisQuePerfeitoAnterior = "pretérito-mais-que-perfeito-anterior"
    PretéritoMaisQuePerfeitoComposto = "pretérito-mais-que-perfeito-composto"
    PretéritoPerfeito = "pretérito-perfeito"
    PretéritoPerfeitoComposto = "pretérito-perfeito-composto"


class TenseRo(StrEnum):
    Afirmativ = "afirmativ"
    Indicativ = "indicativ"
    Gerunziu = "gerunziu"
    Imperativ = "imperativ"
    Imperfect = "imperfect"
    Infinitiv = "infinitiv"
    MaiMultCaPerfect = "mai-mult-ca-perfect"
    Negativ = "negativ"
    Participiu = "participiu"
    Perfect = "perfect"
    PerfectCompus = "perfect-compus"
    PerfectSimplu = "perfect-simplu"
    Prezent = "prezent"
    Viitor = "viitor"
    Viitor1 = "viitor-1"
    Viitor1Popular = "viitor-1-popular"
    Viitor2 = "viitor-2"
    Viitor2Popular = "viitor-2-popular"
    ViitorAnterior = "viitor-anterior"


class Tense:
    fr = TenseFr
    es = TenseEs
    en = TenseEn
    it = TenseIt
    ca = TenseCa
    ro = TenseRo
    pt = TensePt
