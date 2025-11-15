import logging

from verbecc.src.defs.constants.config import DEVEL_MODE

logging_level = logging.CRITICAL + 1  # effectively disables logging
if DEVEL_MODE:
    logging_level = logging.DEBUG

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("verbecc.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

import copy
from typing import List, Optional

from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.constants import grammar_defines
from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.number import Number
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.data.verb import Verb
from verbecc.src.defs.types.exceptions import (
    VerbNotFoundError,
    InvalidMoodError,
    InvalidTenseError,
)
from verbecc.src.defs.types.conjugation import (
    Conjugation,
    TenseConjugation,
    MoodConjugation,
    MoodConjugationUtil,
    MoodsConjugation,
    VerbInfo,
    CompleteConjugation,
)
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.defs.types.data.tense_template import TenseTemplate
from verbecc.src.defs.types.data.conjugation_template import ConjugationTemplate
from verbecc.src.defs.types.data.person_ending import PersonEnding
from verbecc.src.inflectors.inflector_factory import InflectorFactory
from verbecc.src.utils.string_utils import strip_accents


class Conjugator:
    """
    Conjugator encapsulates all conjugation logic that is not language-specific.
    Conjugator uses a concrete instance of Inflector for all language-specific
    conjugation logic.
    """

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions] = None,
    ) -> None:
        self._inflector = InflectorFactory.make_inflector(lang, lang_specific_options)

    def conjugate(
        self,
        infinitive: str,
        conjugate_pronouns: bool = True,
    ) -> CompleteConjugation:
        """
        :param infinitive: the infinitive form of the verb to conjugate
        :type infinitive: str

        :param conjugate_pronouns: if True, verbecc will conjugate the pronoun together with
        its inflected form, e.g. for the French verb apprendre, for the first-person singular
        present tense you'd get "j'apprends" if True or "apprends" if False.
        :type conjugate_pronouns: bool

        :param lang_specific_options: options specific to certain languages.
        :type lang_specific_options: LangSpecificOptions
        """
        co = self._get_conj_obs(infinitive)
        moods = MoodsConjugation()
        for mood, _ in co.template.mood_templates.items():
            moods[mood] = self._conjugate_mood(
                co,
                mood,
                conjugate_pronouns,
            )
        return CompleteConjugation(
            VerbInfo(
                self._inflector.get_lang(),
                co.verb.infinitive,
                co.verb.predicted,
                co.verb.pred_score,
                co.verb.template,
                co.verb.translation_en,
                co.verb_stem,
            ),
            moods,
        )

    def conjugate_mood(
        self,
        infinitive: str,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood(co, mood, conjugate_pronouns)

    def _get_conj_obs(self, infinitive: str) -> ConjugationObjects:
        infinitive = infinitive.lower()
        is_reflexive, infinitive = self._inflector.split_reflexive(infinitive)
        if is_reflexive and not self._inflector.verb_can_be_reflexive(infinitive):
            raise VerbNotFoundError("Verb cannot be reflexive")
        verb = self.find_verb_by_infinitive(infinitive)
        template = self.find_template(verb.template)
        verb_stem = self._inflector.get_verb_stem_from_template_name(
            verb.infinitive, template.name
        )
        return ConjugationObjects(infinitive, verb, template, verb_stem, is_reflexive)

    def get_verbs(self) -> List[Verb]:
        return self._inflector.get_verbs()

    def get_infinitives(self) -> List[str]:
        return self._inflector.get_infinitives()

    def get_templates(self) -> List[ConjugationTemplate]:
        return self._inflector.get_templates()

    def get_template_names(self) -> List[str]:
        return self._inflector.get_template_names()

    def find_verb_by_infinitive(self, infinitive: str) -> Verb:
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name: str) -> ConjugationTemplate:
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query: str, max_results: int) -> List[str]:
        return self._inflector.get_verbs_that_start_with(query, max_results)

    def conjugate_mood_tense(
        self,
        infinitive: str,
        mood: Mood,
        tense: Tense,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood_tense(
            co,
            mood,
            tense,
            conjugate_pronouns=conjugate_pronouns,
        )

    def _conjugate_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        if mood not in co.template.mood_templates.keys():
            raise InvalidMoodError
        ret = self._get_simple_conjugations_for_mood(
            co,
            mood,
            conjugate_pronouns,
        )
        ret = MoodConjugationUtil.combine(
            ret,
            self._get_compound_conjugations_for_mood(
                co,
                mood,
                conjugate_pronouns,
            ),
        )
        return ret

    def _conjugate_mood_tense(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map and tense in comp_conj_map[mood]:
            aux_mood, aux_tense = comp_conj_map[mood][tense]
            aux_uses_alternate = (
                self._inflector.auxiliary_verb_uses_alternate_conjugation(tense)
            )
            return self._conjugate_compound(
                co,
                mood,
                tense,
                aux_mood,
                aux_tense,
                aux_uses_alternate,
                conjugate_pronouns=conjugate_pronouns,
            )
        else:
            mood_template = co.template.mood_templates[mood]
            if tense not in mood_template.tense_templates:
                raise InvalidTenseError
            tense_template = mood_template.tense_templates[tense]
            return self._conjugate_simple_mood_tense(
                co.verb_stem,
                mood,
                tense,
                tense_template,
                is_reflexive=co.is_reflexive,
                modify_stem_strip_accents=bool(
                    co.template.modify_stem == "strip-accents"
                ),
                conjugate_pronouns=conjugate_pronouns,
            )

    def _get_simple_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(mood)
        mood_template = co.template.mood_templates[mood]
        for tense in mood_template.tense_templates:
            ret[tense] = self._conjugate_mood_tense(
                co,
                mood,
                tense,
                conjugate_pronouns=conjugate_pronouns,
            )
        return ret

    def _get_compound_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        conjugate_pronouns: bool = True,
    ) -> MoodConjugation:
        ret = MoodConjugation(mood)
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map:
            for tense in comp_conj_map[mood]:
                ret[tense] = self._conjugate_mood_tense(
                    co,
                    mood,
                    tense,
                    conjugate_pronouns=conjugate_pronouns,
                )
        return ret

    def _conjugate_compound(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        aux_mood: Mood,
        aux_tense: Tense,
        aux_uses_alternate: bool,
        conjugate_pronouns: bool = True,
    ) -> TenseConjugation:
        ret = TenseConjugation(tense)
        if self._inflector.compound_conjugation_not_applicable(
            co.is_reflexive, mood, aux_tense
        ):
            return ret
        persons_mood = mood
        if mood not in co.template.mood_templates.keys():
            persons_mood = self._inflector.get_indicative_mood()
        person_endings = (
            co.template.mood_templates[persons_mood]
            .tense_templates[aux_tense]
            .person_endings
        )
        aux_verb = self._inflector.get_auxiliary_verb(co, mood, tense)
        aux_co = self._get_conj_obs(aux_verb)
        aux_tense_template = copy.deepcopy(
            aux_co.template.mood_templates[aux_mood].tense_templates[aux_tense]
        )
        aux_person_endings = []
        for aux_pe in aux_tense_template.person_endings:
            if aux_pe.person is not None and aux_pe.person in [
                pe.person for pe in person_endings if pe.person is not None
            ]:
                aux_person_endings.append(aux_pe)
        aux_tense_template.person_endings = aux_person_endings
        aux_conj = self._conjugate_simple_mood_tense(
            aux_co.verb_stem,
            aux_mood,  # todo: investigate (used to be "")
            aux_tense,
            aux_tense_template,
            co.is_reflexive,
            conjugate_pronouns=conjugate_pronouns,
        )
        # need to skip conjugating primary verb for certain tenses e.g. romanian viitor-1
        ret = self._conjugate_compound_primary_verb(
            co,
            mood,
            tense,
            aux_mood,
            aux_tense,
            aux_verb,
            aux_conj,
            aux_uses_alternate,
        )

        return ret

    def _conjugate_compound_primary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        aux_mood: Mood,
        aux_tense: Tense,
        aux_verb: str,
        aux_conj: TenseConjugation,
        aux_uses_alternate: bool,
    ) -> TenseConjugation:
        """
        :param: person_endings = ?
        :param: aux_conj e.g. ["suis", "es", "est", etc.]

        Forms a compound conjugation composed of an auxiliary verb (aka helping verb)
        conjugation and a primary verb, typically the participle tense.
        Typically the primary verb is a participle but there are exceptions e.g.
        the Romanian indicativ viitor-1 uses the inifitive form instead of the participle

        E.g. in the French conjugation "j'ai parlé", "ai" is the conjugated form of the
        auxiliary verb "avoir" and "parlé" is the participle tense of the primary verb "parler".
        With avoir, the participle is not inflected, it's always "parlé".

        With être, however, the participle is inflected (modified based on gender and number).
        E.g.:

            je suis allé
            tu es allé
            il est allé
            nous sommes allé(e)s
            vous êtes allé(e)s
            ils/elles sont allé(e)s
        """
        ret = TenseConjugation(tense)
        aux_conj_scalar: List[str] = []
        for pc in aux_conj:
            conjugations = pc.get_conjugations()
            if aux_uses_alternate and len(conjugations) > 1:
                aux_conj_scalar.append(conjugations[1])
            else:
                aux_conj_scalar.append(conjugations[0])

        p_mood = self._inflector.get_participle_mood()
        p_tense = self._inflector.get_participle_tense()
        p_conj = TenseConjugation(p_tense)
        # the Romanian indicativ viitor-1 uses the infinitive form instead of the participle
        # TODO: Move this language-specific logic into inflector
        if self._inflector.compound_primary_verb_conjugation_uses_infinitive(
            mood, tense
        ):
            p_conj.append(Conjugation(None, None, None, None, [co.infinitive]))
        else:
            p_conj = self._conjugate_simple_mood_tense(
                co.verb_stem,
                p_mood,
                p_tense,
                co.template.mood_templates[p_mood].tense_templates[p_tense],
                False,
            )

        if not self._inflector.is_auxiliary_verb_inflected(aux_verb):
            # participle is not inflected, e.g. French passé composé with avoir
            # where aux_verb = "avoir"
            # e.g. j'ai parlé, tu as parlé, il a parlé, nous avons parlé, vous avez parlé, ils ont parlé

            # special case: Romanian conjunctiv perfect
            # TODO: Refactor further
            if self._inflector.compound_has_no_aux_verb(mood, tense):
                participle_c = p_conj[0]
                for i, c in enumerate(aux_conj_scalar):
                    pronoun, _ = aux_conj_scalar[i].split()
                    aux_conj_scalar[i] = pronoun + " " + str(participle_c[0])

            # Normally Romanian aux_conj would be the indicativ prezent tense of avea i.e.
            # ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"]
            # but for conditional it's supposed to be
            # ["eu aş", "tu ai", "el ar", "noi am", "voi aţi", "ei ar"]
            aux_conj_scalar = self._inflector.modify_aux_verb_conj_if_applicable(
                aux_conj_scalar, mood, tense
            )

            # for Romanian insert " să fi" or " o să " when appropriate
            # e.g. "eu o să face, tu o să faci, ..."
            aux_conj_scalar = [
                self._inflector.insert_compound_aux_verb_prefix_if_applicable(
                    i, mood, tense
                )
                for i in aux_conj_scalar
            ]

            # for Romanian append " fi", " să fi" etc. when appropriate
            aux_conj_scalar = [
                self._inflector.add_compound_aux_verb_suffix_if_applicable(
                    i, mood, tense
                )
                for i in aux_conj_scalar
            ]

            # Compound verb conjugation is usually this:
            # {aux_conj(pronoun + aux_conj)} + {compound_suffix} + {primary_conj}
            # where primary_conj is usually the participle of the aux_verb
            #
            # Notable exceptions:
            # 1.
            # The Romanian viitor-1-popular doesn't have a "primary verb", at least not the
            # way it's currently implemented in verbecc. This function just calls the inflector
            # function that adds the " o să" compound suffix.
            # e.g. to get the indicativ viitor-1-popular of the verb 'face' i.e.
            # "eu o să fac, tu o să faci, ..."
            # the verb is coming from aux_conj and p_conj isn't used
            # 2.
            # The Romanian conjunctiv present e.g. 'eu să fi făcut'
            # Doesn't use aux_conj, or rather sets aux_conj = p_conj
            # (see above)

            if self._inflector.compound_has_no_primary_verb(
                mood, tense
            ) or self._inflector.compound_has_no_aux_verb(mood, tense):
                for i, c in enumerate(aux_conj_scalar):
                    aux_pc: Conjugation = aux_conj[i]
                    ret.append(
                        Conjugation(
                            aux_pc.get_person(),
                            aux_pc.get_number(),
                            aux_pc.get_gender(),
                            aux_pc.get_pronoun(),
                            [c],
                        )
                    )
            else:
                for i, hv in enumerate(aux_conj_scalar):
                    aux_pc: Conjugation = aux_conj[i]
                    pc_value = grammar_defines.NO_VALUE
                    if len(p_conj):
                        pc = p_conj[0]
                        pc_value = str(pc[0])
                    else:
                        logger.warning(
                            "(aux verb not inflected) primary (participle) conjugation is empty: co=%s p_mood=%s p_tense=%s",
                            co,
                            p_mood,
                            p_tense,
                        )
                    hv = self._inflector.get_alternate_hv_inflection(hv)
                    ret.append(
                        Conjugation(
                            aux_pc.get_person(),
                            aux_pc.get_number(),
                            aux_pc.get_gender(),
                            aux_pc.get_pronoun(),
                            [hv + " " + pc_value],
                        )
                    )
        else:
            # participle is inflected, e.g. French passé composé with être
            # where aux_verb = "être"
            #
            # e.g.
            # je suis allé,
            # tu es allé,
            # il est allé,
            # nous sommes allé(e)s,
            # vous êtes allé(e)s,
            # ils/elles sont allé(e)s
            #
            # or Italian verbs conjugated with essere
            #
            # Only include feminine conjugation if different from masculine.
            # For the feminine conjugations for ambiguous pronouns like nous, vous, that is.
            # The conjugations for

            # person_endings are the template endings for the primary verb
            # e.g. for the infinitive "aller" in the PasséAntérieur:
            # Tenses.fr.PasséAntérieur: (Moods.fr.Indicatif, Tenses.fr.PasséSimple),
            # person_endings would be allai, allas, alla, etc.
            # so they are irrelevant here, since we are using the PasséSimple
            # of the auxiliary verb rather than the primary verb,
            # but we can use them to get number.

            for i, hv in enumerate(aux_conj_scalar):
                aux_pc = aux_conj[i]  # e.g. "suis"
                # need to get person_ending, e.g. "allé", based on gender and number of aux_pc
                gender = Gender.m
                number = Number.Singular

                aux_pc_gender = aux_pc.get_gender()
                if aux_pc_gender is not None:
                    gender = aux_pc_gender

                aux_pc_number = aux_pc.get_number()
                if aux_pc_number is not None:
                    number = aux_pc_number

                genders = []
                if (
                    aux_pc.get_person() == Person.Third
                    and aux_pc.get_gender() is not None
                ):
                    genders.append(aux_pc.get_gender())
                else:
                    genders.extend([Gender.f, Gender.m])
                conjugations = [
                    self._conjugate_compound_participle_inflected(
                        gender, number, aux_pc, p_conj
                    )
                    for gender in genders
                ]
                ret.extend(conjugations)

        return ret

    def _conjugate_compound_participle_inflected(
        self,
        gender: Gender,
        number: Number,
        aux_pc: Conjugation,
        p_conj: TenseConjugation,
    ) -> Conjugation:
        """
        :param aux_pc: Conjugation of aux verb e.g. "suis"
        :param pc: Conjugation in participle tense of primary verb
            e.g. "allée"
        """
        pc = self.get_conjugation_by_gender_and_number(p_conj, gender, number)
        # TODO: Alternates?
        return Conjugation(
            aux_pc.get_person(),
            aux_pc.get_number(),
            gender,
            aux_pc.get_pronoun(),
            [f"{aux_pc[0]} {pc[0]}"],
        )

    def _conjugate_simple_mood_tense(
        self,
        verb_stem: str,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        is_reflexive: bool = False,
        conjugate_pronouns: bool = True,
        modify_stem_strip_accents: bool = False,
    ) -> TenseConjugation:
        if modify_stem_strip_accents and mood != self._inflector.get_infinitive_mood():
            verb_stem = strip_accents(verb_stem)
        ret = TenseConjugation(tense)
        tense = tense_template.tense
        tense_conjugated_with_pronoun = True
        if (
            tense in self._inflector.get_tenses_conjugated_without_pronouns()
            or not conjugate_pronouns
        ):
            tense_conjugated_with_pronoun = False

        # There will be at least one conjugation per person-ending and
        # potentially one or more alternate conjugations
        for person_ending in tense_template.person_endings:
            person = person_ending.get_person()
            number = person_ending.get_number()

            pronouns = self._inflector.get_pronouns(
                person=person,
                number=number,
            )
            # note: tense_conjugated_with_pronoun is False
            # for imperative tense but we still want to set the
            # `pronoun` field.
            # the only case where we don't set the `pronoun` field
            # is when it's participle mood because the PersonEndings
            # are participle type, i.e. each PersonEnding has
            # gender and number instead of person and number.
            if mood == self._inflector.get_participle_mood():
                # we're only conjugating person-endings
                pronouns = [None]

            for pronoun in pronouns:

                # here's where the voseo magic happens
                person_ending = self._inflector.modify_person_ending_if_applicable(
                    person_ending, mood, tense, tense_template, pronoun
                )

                # person_ending.gender will be None unless it's a participle ending
                # gender will be None/null unless it matters.
                conjugation_gender = None
                if pronoun is not None:
                    conjugation_gender = self._inflector.get_pronoun_gender(pronoun)
                if conjugation_gender is None and person_ending.gender is not None:
                    conjugation_gender = person_ending.gender

                conjugation = Conjugation(
                    person,
                    number,
                    conjugation_gender,
                    pronoun,
                )
                if is_reflexive and pronoun is not None:
                    pronoun = self._inflector.make_pronoun_reflexive(pronoun)

                # get endings i.e. primary and optional alternate(s)
                endings: List[str] = []
                endings.extend(person_ending.get_endings())

                # there may be one or more alternate endings
                for ending in endings:
                    s = grammar_defines.NO_VALUE
                    if tense_conjugated_with_pronoun:
                        if ending != grammar_defines.NO_VALUE:
                            conj = self._inflector.combine_verb_stem_and_ending(
                                verb_stem, ending
                            )
                            if pronoun is not None:
                                s = self._inflector.combine_pronoun_and_conj(
                                    pronoun, conj
                                )
                            if mood == self._inflector.get_subjunctive_mood():
                                s = self._inflector.add_subjunctive_relative_pronoun(
                                    s, tense
                                )
                    else:
                        # conjugation without pronoun
                        # e.g. fr:participe:participe-passé
                        s = self._inflector.add_present_participle_if_applicable(
                            "", is_reflexive, tense
                        )
                        if ending != grammar_defines.NO_VALUE:
                            s += self._inflector.combine_verb_stem_and_ending(
                                verb_stem, ending
                            )
                        else:
                            s += ending
                        if ending != grammar_defines.NO_VALUE:
                            person = person_ending.get_person()
                            number = person_ending.get_number()
                            if person is not None:
                                s = self._inflector.add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
                                    s,
                                    is_reflexive,
                                    mood,
                                    tense,
                                    person,
                                    number,
                                )
                            else:
                                logger.warning("person is None")
                        if ending != grammar_defines.NO_VALUE:
                            s = self._inflector.add_adverb_if_applicable(s, mood, tense)
                    conjugation.append(s)
                ret.append(conjugation)
        return ret

    def get_person_ending_by_gender_and_number(
        self,
        person_endings: List[PersonEnding],
        gender: Optional[Gender],
        number: Optional[Number],
    ) -> PersonEnding:
        resolved_gender = Gender.m
        resolved_number = Number.Singular
        if gender is not None:
            resolved_gender = gender
        if number is not Number:
            resolved_number = number
        for pe in person_endings:
            if pe.gender == resolved_gender and pe.number == resolved_number:
                return pe
        logger.warning(
            "Failed find matching PersonEnding for gender=%s number=%s", gender, number
        )
        return person_endings[0]

    def get_conjugation_by_gender_and_number(
        self,
        tense_conjugation: TenseConjugation,
        gender: Optional[Gender],
        number: Optional[Number],
    ) -> Conjugation:
        resolved_gender = Gender.m
        resolved_number = Number.Singular
        if gender is not None:
            resolved_gender = gender
        if number is not Number:
            resolved_number = number
        for c in tense_conjugation:
            if c.get_gender() == resolved_gender and c.get_number() == resolved_number:
                return c
        logger.warning(
            "Failed find matching Conjugation for gender=%s number=%s", gender, number
        )
        return tense_conjugation[0]
