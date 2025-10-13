from verbecc.src.parsers.verb import Verb
from verbecc.src.parsers.conjugation_template import ConjugationTemplate


class ConjugationObjects:
    def __init__(
        self,
        infinitive: str,
        verb: Verb,
        template: ConjugationTemplate,
        verb_stem: str,
        is_reflexive: bool,
    ):
        """
        :param verb_stem: the verb stem after applicable template
                            stem modifications i.e. modify-stem="strip-accents"
        :type verb_stem: str
        """
        self.infinitive = infinitive
        self.verb = verb
        self.template = template
        self.verb_stem = verb_stem
        self.is_reflexive = is_reflexive

    def __repr__(self):
        return "infinitive={} verb={} template={} verb_stem={} is_reflexive={}".format(
            self.infinitive,
            self.verb,
            self.template,
            self.verb_stem,
            self.is_reflexive,
        )
