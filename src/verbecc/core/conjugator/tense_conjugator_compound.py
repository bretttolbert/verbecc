import copy
from typing import Optional

from verbecc.core.conjugator.conjugation_object import ConjugationObjects
from verbecc.core.defs.constants import grammar_defines
from verbecc.core.defs.types.data.person_ending import PersonEnding
from verbecc.core.defs.types.gender import Gender
from verbecc.core.defs.types.number import Number
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.mood import Mood
from verbecc.core.defs.types.tense import Tense
from verbecc.core.defs.types.conjugation.tense_conjugation import TenseConjugation
from verbecc.core.defs.types.conjugation.conjugation import Conjugation
from verbecc.core.defs.types.lang_specific_options import LangSpecificOptions
from verbecc.core.defs.types.lang_code import LangCodeISO639_1
from verbecc.core.conjugator.abstract_conjugator import AbstractConjugator
from verbecc.core.conjugator.tense_conjugator_simple import TenseConjugatorSimple


class TenseConjugatorCompound(AbstractConjugator):

    def __init__(
        self,
        lang: LangCodeISO639_1,
        lang_specific_options: Optional[LangSpecificOptions],
        tense_conjugator_simple: TenseConjugatorSimple,
    ) -> None:
        super().__init__(
            lang,
            lang_specific_options,
            self.__class__.__name__,
            tense_conjugator_simple._inflector,
        )
        self._tense_conjugator_simple = tense_conjugator_simple
        pass

    def co_conjugate_compound_mood_tense(
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
        aux_co = self.get_co(aux_verb)
        aux_tense_template = copy.deepcopy(
            aux_co.template.mood_templates[aux_mood].tense_templates[aux_tense]
        )
        aux_person_endings: list[PersonEnding] = []
        for aux_pe in aux_tense_template.person_endings:
            if aux_pe.person is not None and aux_pe.person in [
                pe.person for pe in person_endings if pe.person is not None
            ]:
                aux_person_endings.append(aux_pe)
        aux_tense_template.person_endings = aux_person_endings
        aux_conj = self._tense_conjugator_simple.conjugate_simple_mood_tense(
            aux_co.verb_stem,
            aux_mood,  # todo: investigate (used to be "")
            aux_tense,
            aux_tense_template,
            primary_tense=tense,
            is_reflexive=co.is_reflexive,
            conjugate_pronouns=(
                conjugate_pronouns
                and tense
                not in self._inflector.get_tenses_conjugated_without_pronouns()
            ),
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
            conjugate_pronouns,
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
        conjugate_pronouns: bool,
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
        aux_conj_scalar: list[str] = []
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
            p_conj = self._tense_conjugator_simple.conjugate_simple_mood_tense(
                co.verb_stem,
                p_mood,
                p_tense,
                co.template.mood_templates[p_mood].tense_templates[p_tense],
                is_reflexive=False,
                conjugate_pronouns=False,
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
                        self._logger.warning(
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
                number = Number.Singular

                aux_pc_number = aux_pc.get_number()
                if aux_pc_number is not None:
                    number = aux_pc_number

                genders: list[Gender | None] = []
                if (
                    aux_pc.get_person() == Person.Third
                    and aux_pc.get_gender() is not None
                ):
                    genders.append(aux_pc.get_gender())
                else:
                    genders.extend([Gender.f, Gender.m])
                p_conj_len = len(p_conj)
                if p_conj_len > 0:
                    ret.extend(
                        [
                            self._conjugate_compound_participle_inflected(
                                gender, number, aux_pc, p_conj
                            )
                            for gender in genders
                        ]
                    )
                else:
                    # probably some verb like absoudre that isn't
                    # conjugated in certain tenses
                    self._logger.warning(
                        "Skipping compound conjugation, "
                        + "participle conjugation is empty. "
                        + "aux_pc=%s aux_verb=%s",
                        aux_pc,
                        aux_verb,
                    )
        return ret

    def _conjugate_compound_participle_inflected(
        self,
        gender: Gender | None,
        number: Number,
        aux_pc: Conjugation,
        p_conj: TenseConjugation,
    ) -> Conjugation:
        """
        :param aux_pc: Conjugation of aux verb e.g. "suis"
        :param p_conj: Conjugation in participle tense of primary verb
            e.g. ["allé", "allée", "allés", "allées"]
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
