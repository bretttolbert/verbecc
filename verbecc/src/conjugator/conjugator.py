import logging

from verbecc.src.defs.types.gender import Gender
from verbecc.src.defs.types.mood import Mood
from verbecc.src.defs.types.tense import Tense
from verbecc.src.defs.types.conjugation import ConjugationInfo
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
from typing import cast, List

from verbecc.src.parsers.verb import Verb
from verbecc.src.parsers.tense_template import TenseTemplate
from verbecc.src.parsers.conjugation_template import ConjugationTemplate
from verbecc.src.inflectors.inflector_factory import InflectorFactory
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.person import Person
from verbecc.src.defs.types.exceptions import (
    VerbNotFoundError,
    InvalidMoodError,
    InvalidTenseError,
)
from verbecc.src.defs.types.conjugation import (
    PersonConjugation,
    TenseConjugation,
    MoodConjugation,
    MoodsConjugation,
    Conjugation,
)
from verbecc.src.defs.types.lang_specific_options import (
    LangSpecificOptions,
)
from verbecc.src.conjugator.conjugation_object import ConjugationObjects
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.utils.string_utils import strip_accents
from verbecc.src.defs.types.alternates_behavior import AlternatesBehavior


class Conjugator:
    """
    Conjugator encapsulates all conjugation logic that is not language-specific.
    Conjugator uses a concrete instance of Inflector for all language-specific
    conjugation logic.
    """

    def __init__(self, lang: LangCodeISO639_1) -> None:
        self._inflector = InflectorFactory.make_inflector(lang)

    def conjugate(
        self,
        infinitive: str,
        include_alternates: bool = False,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> Conjugation:
        """
        :param infinitive: the infinitive form of the verb to conjugate
        :type infinitive: str

        :param include_alternates: whether to include alternate conjugations
        e.g. the Catalan verbs ser/ésser have alternate conjugations in
        the conditional tense and the participle
        See test_inflector_ca.test_inflector_conjugate_with_alternates
        :type include_alternates: bool

        :param gender: controls gender of third-person singular and plural
        :type gender: Gender

        :param conjugate_pronouns: if True, verbecc will conjugate the pronoun together with
        its inflected form, e.g. for the French verb apprendre, for the first-person singular
        present tense you'd get "j'apprends" if True or "apprends" if False.
        :type conjugate_pronouns: bool

        :param lang_specific_options: options specific to certain languages.
        :type lang_specific_options: LangSpecificOptions
        """
        alternates_behavior = AlternatesBehavior.FirstOnly
        if include_alternates:
            alternates_behavior = AlternatesBehavior.All
        co = self._get_conj_obs(infinitive)
        moods: MoodsConjugation = {}
        for mood, _ in co.template.mood_templates.items():
            moods[mood] = self._conjugate_mood(
                co,
                mood,
                alternates_behavior,
                gender,
                conjugate_pronouns,
                lang_specific_options,
            )
        return {
            "verb": ConjugationInfo(
                co.verb.infinitive,
                co.verb.predicted,
                co.verb.pred_score,
                co.verb.template,
                co.verb.translation_en,
                co.verb_stem,
            ).data,
            "moods": moods,
        }

    def conjugate_mood(
        self,
        infinitive: str,
        mood: Mood,
        alternates_behavior: AlternatesBehavior = AlternatesBehavior.FirstOnly,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> MoodConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood(
            co, mood, alternates_behavior, gender, conjugate_pronouns
        )

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
        alternates_behavior: AlternatesBehavior = AlternatesBehavior.FirstOnly,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> TenseConjugation:
        co = self._get_conj_obs(infinitive)
        return self._conjugate_mood_tense(
            co,
            mood,
            tense,
            alternates_behavior=alternates_behavior,
            gender=gender,
            conjugate_pronouns=conjugate_pronouns,
            lang_specific_options=lang_specific_options,
        )

    def _conjugate_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        alternates_behavior: AlternatesBehavior,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> MoodConjugation:
        if mood not in co.template.mood_templates.keys():
            raise InvalidMoodError
        ret = {}
        ret.update(
            self._get_simple_conjugations_for_mood(
                co,
                mood,
                alternates_behavior,
                gender,
                conjugate_pronouns,
                lang_specific_options,
            )
        )
        ret.update(
            self._get_compound_conjugations_for_mood(
                co,
                mood,
                alternates_behavior,
                gender,
                conjugate_pronouns,
                lang_specific_options,
            )
        )
        return ret

    def _conjugate_mood_tense(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        alternates_behavior: AlternatesBehavior,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> TenseConjugation:
        """
        :param gender: controls gender of third-person singular and plural
        pronouns, if conjugate_pronouns is enabled. Otherwise ignored.
        """
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map and tense in comp_conj_map[mood]:
            aux_mood, aux_tense = comp_conj_map[mood][tense]
            return self._conjugate_compound(
                co,
                mood,
                tense,
                aux_mood,
                aux_tense,
                self._inflector.auxiliary_verb_uses_alternate_conjugation(tense),
                alternates_behavior,
                gender=gender,
                conjugate_pronouns=conjugate_pronouns,
                lang_specific_options=lang_specific_options,
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
                alternates_behavior=alternates_behavior,
                gender=gender,
                modify_stem_strip_accents=bool(
                    co.template.modify_stem == "strip-accents"
                ),
                conjugate_pronouns=conjugate_pronouns,
                lang_specific_options=lang_specific_options,
            )

    def _get_simple_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        alternates_behavior: AlternatesBehavior,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> MoodConjugation:
        ret = {}
        mood_template = co.template.mood_templates[mood]
        for tense in mood_template.tense_templates:
            ret[tense] = self._conjugate_mood_tense(
                co,
                mood,
                tense,
                alternates_behavior,
                gender,
                conjugate_pronouns=conjugate_pronouns,
                lang_specific_options=lang_specific_options,
            )
        return ret

    def _get_compound_conjugations_for_mood(
        self,
        co: ConjugationObjects,
        mood: Mood,
        alternates_behavior: AlternatesBehavior,
        gender: Gender,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> MoodConjugation:
        ret = {}
        comp_conj_map = self._inflector.get_compound_conjugations_aux_verb_map()
        if mood in comp_conj_map:
            for tense in comp_conj_map[mood]:
                ret[tense] = self._conjugate_mood_tense(
                    co,
                    mood,
                    tense,
                    alternates_behavior,
                    gender,
                    conjugate_pronouns=conjugate_pronouns,
                    lang_specific_options=lang_specific_options,
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
        alternates_behavior: AlternatesBehavior,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        lang_specific_options: LangSpecificOptions = None,
    ) -> TenseConjugation:
        """
        :param gender: controls gender of third-person singular and plural
        pronouns, if conjugate_pronouns is enabled. Otherwise ignored.
        """
        ret = []
        if self._inflector.compound_conjugation_not_applicable(
            co.is_reflexive, mood, aux_tense
        ):
            return ret
        persons_mood = mood
        if mood not in co.template.mood_templates.keys():
            persons_mood = self._inflector.get_indicative_mood()
        persons = [
            pe.person
            for pe in co.template.mood_templates[persons_mood]
            .tense_templates[aux_tense]
            .person_endings
        ]
        aux_verb = self._inflector.get_auxiliary_verb(co, mood, tense)
        aux_co = self._get_conj_obs(aux_verb)
        aux_tense_template = copy.deepcopy(
            aux_co.template.mood_templates[aux_mood].tense_templates[aux_tense]
        )
        aux_person_endings = []
        for pe in aux_tense_template.person_endings:
            if pe.person in persons:
                aux_person_endings.append(pe)
        aux_tense_template.person_endings = aux_person_endings
        aux_alternates_behavior = AlternatesBehavior.FirstOnly
        if aux_uses_alternate:
            aux_alternates_behavior = AlternatesBehavior.SecondOnly
        aux_conj = self._conjugate_simple_mood_tense(
            aux_co.verb_stem,
            "",
            aux_tense,
            aux_tense_template,
            co.is_reflexive,
            aux_alternates_behavior,
            gender=gender,
            conjugate_pronouns=conjugate_pronouns,
            lang_specific_options=lang_specific_options,
        )
        # cast below is safe because we're not using AlternatesBehavior.All
        aux_conj_scalar_list = cast(List[str], aux_conj)
        # need to skip conjugating primary verb for certain tenses e.g. romanian viitor-1
        ret = self._conjugate_compound_primary_verb(
            co,
            mood,
            tense,
            persons,
            aux_verb,
            aux_conj_scalar_list,
            alternates_behavior,
            gender,
        )
        if mood == self._inflector.get_subjunctive_mood():
            if alternates_behavior == AlternatesBehavior.All:
                ret = [
                    [
                        self._inflector.add_subjunctive_relative_pronoun(i, tense)
                        for i in j
                    ]
                    for j in ret
                ]
            else:
                # cast is safe because we're not using AlternatesBehavior.All
                ret = cast(List[str], ret)
                ret = [
                    self._inflector.add_subjunctive_relative_pronoun(i, tense)
                    for i in ret
                ]
        return cast(TenseConjugation, ret)

    def _conjugate_compound_primary_verb(
        self,
        co: ConjugationObjects,
        mood: Mood,
        tense: Tense,
        persons: List[Person],
        aux_verb: str,
        aux_conj: List[str],
        alternates_behavior: AlternatesBehavior,
        gender: Gender = Gender.m,
        lang_specific_options: LangSpecificOptions = None,
    ) -> TenseConjugation:
        """
        Forms a compound conjugation composed of an auxiliary verb (aka helping verb)
        conjugation and a primary verb, typically the participle tense.
        Typically the primary verb is a participle but there are exceptions e.g.
        the Romanian indicativ viitor-1 uses the inifitive form instead of the participle

        E.g. in the French conjugation "j'ai parlé", "ai" is the conjugated form of the
        auxiliary verb "avoir" and "parlé" is the participle tense of the primary verb "parler".
        With avoir, the participle is not inflected, it's always "parlé".

        With être, however, the participle is inflected (modified based on gender and number). E.g.:
        je suis allé, tu es allé, il est allé, nous sommes allé(e)s, vous êtes allé(e)s, ils/elles sont allé(e)s

        :param gender: controls gender of third-person singular and plural
        pronouns, if conjugate_pronouns is enabled. Otherwise ignored.
        """
        ret: List[str] = []

        p_conj = []
        # the Romanian indicativ viitor-1 uses the infinitive form instead of the participle
        if self._inflector.compound_primary_verb_conjugation_uses_infinitive(
            mood, tense
        ):
            p_conj = [co.infinitive]
        else:
            p_mood = self._inflector.get_participle_mood()
            p_tense = self._inflector.get_participle_tense()
            p_conj = self._conjugate_simple_mood_tense(
                co.verb_stem,
                p_mood,
                p_tense,
                co.template.mood_templates[p_mood].tense_templates[p_tense],
                False,
                AlternatesBehavior.FirstOnly,
                gender=gender,
            )
            # cast is safe since we're not using AlternatesBehavior.All
            p_conj = cast(List[str], p_conj)

        if not self._inflector.is_auxiliary_verb_inflected(aux_verb):
            # participle is not inflected, e.g. French passé composé with avoir
            # where aux_verb = "avoir"
            # e.g. j'ai parlé, tu as parlé, il a parlé, nous avons parlé, vous avez parlé, ils ont parlé

            # special case: Romanian conjunctiv perfect
            # TODO: Refactor further
            if self._inflector.compound_has_no_aux_verb(mood, tense):
                participle = p_conj[0]
                for i, c in enumerate(aux_conj):
                    pronoun, _ = aux_conj[i].split()
                    aux_conj[i] = pronoun + " " + participle

            # Normally Romanian aux_conj would be the indicativ prezent tense of avea i.e.
            # ["eu am", "tu ai", "el a", "noi am", "voi aţi", "ei au"]
            # but for conditional it's supposed to be
            # ["eu aş", "tu ai", "el ar", "noi am", "voi aţi", "ei ar"]
            aux_conj = self._inflector.modify_aux_verb_conj_if_applicable(
                aux_conj, mood, tense
            )

            # for Romanian insert " o să " when appropriate
            # e.g. "eu o să face, tu o să faci, ..."
            aux_conj = [
                self._inflector.insert_compound_aux_verb_prefix_if_applicable(
                    i, mood, tense
                )
                for i in aux_conj
            ]

            # for Romanian append " fi", " să fi" etc. when appropriate
            aux_conj = [
                self._inflector.add_compound_aux_verb_suffix_if_applicable(
                    i, mood, tense
                )
                for i in aux_conj
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
                ret = aux_conj
            else:
                for hv in aux_conj:
                    p = "-"
                    if len(p_conj):
                        p = p_conj[0]
                    else:
                        logger.warning(
                            "(aux verb not inflected) primary (participle) conjugation is empty: co=%s p_mood=%s p_tense=%s",
                            co,
                            p_mood,
                            p_tense,
                        )
                    hv = self._inflector.get_alternate_hv_inflection(hv)
                    ret.append(hv + " " + p)
        else:
            # participle is inflected, e.g. French passé composé with être
            # where aux_verb = "être"
            # e.g. je suis allé, tu es allé, il est allé, nous sommes allé(e)s, vous êtes allé(e)s, ils/elles sont allé(e)s
            # or Italian verbs conjugated with essere

            for i, hv in enumerate(aux_conj):
                participle_inflection = (
                    self._inflector.get_default_participle_inflection_for_person(
                        persons[i], gender
                    )
                )
                p = "-"
                participle_idx = (
                    self._inflector.get_participle_index_for_participle_inflection(
                        participle_inflection
                    )
                )
                if len(p_conj) > participle_idx:
                    p = p_conj[participle_idx]
                else:
                    logger.warning(
                        "(aux verb inflected) primary (participle) conjugation is empty: co=%s p_mood=%s t_tense=%s",
                        co,
                        p_mood,
                        p_tense,
                    )
                ret.append(hv + " " + p)
        if alternates_behavior == AlternatesBehavior.All:
            return [[i] for i in ret]
        else:
            return cast(TenseConjugation, ret)

    def _conjugate_simple_mood_tense(
        self,
        verb_stem: str,
        mood: Mood,
        tense: Tense,
        tense_template: TenseTemplate,
        is_reflexive: bool = False,
        alternates_behavior: AlternatesBehavior = AlternatesBehavior.FirstOnly,
        gender: Gender = Gender.m,
        conjugate_pronouns: bool = True,
        modify_stem_strip_accents: bool = False,
        lang_specific_options: LangSpecificOptions = None,
    ) -> TenseConjugation:
        """
        :param gender: controls gender of third-person singular and plural
        pronouns, if conjugate_pronouns is enabled. Otherwise ignored.
        """
        if modify_stem_strip_accents and mood != self._inflector.get_infinitive_mood():
            verb_stem = strip_accents(verb_stem)
        ret: TenseConjugation = []
        tense = tense_template.name
        compound = True
        if (
            tense in self._inflector.get_tenses_conjugated_without_pronouns()
            or not conjugate_pronouns
        ):
            compound = False

        for person_ending in tense_template.person_endings:
            person_ending = self._inflector.modify_person_ending_if_applicable(
                person_ending,
                mood,
                tense,
                tense_template,
                lang_specific_options,
            )
            # There will be at least one conjugation per person-ending and
            # potentially one or more alternate conjugations
            person_conjugation: PersonConjugation = []
            endings: List[str] = []
            if alternates_behavior == AlternatesBehavior.FirstOnly:
                endings.append(person_ending.get_ending())
            elif alternates_behavior == AlternatesBehavior.SecondOnly:
                endings.append(person_ending.get_alternate_ending_if_available())
            else:  # default: AlternatesBehavior.All
                endings.extend(person_ending.get_endings())
            # there may be one or more alternate endings
            for ending in endings:
                if compound:
                    # compound conjugation
                    pronoun = self._inflector.get_default_pronoun(
                        person=person_ending.get_person(),
                        gender=gender,
                        is_reflexive=is_reflexive,
                        lang_specific_options=lang_specific_options,
                    )
                    s = "-"
                    if ending != "-":
                        conj = self._inflector.combine_verb_stem_and_ending(
                            verb_stem, ending
                        )
                        s = self._inflector.combine_pronoun_and_conj(pronoun, conj)
                        if mood == self._inflector.get_subjunctive_mood():
                            s = self._inflector.add_subjunctive_relative_pronoun(
                                s, tense
                            )
                else:
                    # simple conjugation
                    s = self._inflector.add_present_participle_if_applicable(
                        "", is_reflexive, tense
                    )
                    if ending != "-":
                        s += self._inflector.combine_verb_stem_and_ending(
                            verb_stem, ending
                        )
                    else:
                        s += ending
                    if ending != "-":
                        s = self._inflector.add_reflexive_pronoun_or_pronoun_suffix_if_applicable(
                            s,
                            is_reflexive,
                            mood,
                            tense,
                            person_ending.get_person(),
                        )
                    if ending != "-":
                        s = self._inflector.add_adverb_if_applicable(s, mood, tense)
                person_conjugation.append(s)
            if alternates_behavior == AlternatesBehavior.All:
                ret.append(list(person_conjugation))
            elif (
                alternates_behavior == AlternatesBehavior.SecondOnly
                and len(person_conjugation) > 1
            ):
                ret.append(person_conjugation[1])
            else:
                ret.append(person_conjugation[0])

        return ret
