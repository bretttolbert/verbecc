from collections import defaultdict
import random

from verbecc.core.mlconjug.mltypes import VerbTemplatePair


class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper methodss for managing Machine Learning tasks like constructing a training and testing set.
    """

    def __init__(self, verb_template_pairs: list[VerbTemplatePair]) -> None:
        self.verbs = [pair[0] for pair in verb_template_pairs]
        self.templates = sorted(set([pair[1] for pair in verb_template_pairs]))
        self.dict_conjug = self._construct_dict_conjug(verb_template_pairs)
        self._split_test_train()
        return

    def _construct_dict_conjug(
        self, verb_template_pairs: list[VerbTemplatePair]
    ) -> dict[str, list[str]]:
        """
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.

        :param verb_template_pairs: list.
            List of tuples of (verb,template) e.g. ('abaisser','aim:er')
        :return: defaultdict.
            defaultdict mapping each template to one or more verbs e.g. {'aim:er': ['abaisser', ...]}
        """
        ret = defaultdict(list)
        random.shuffle(verb_template_pairs)
        for verb, template in verb_template_pairs:
            ret[template].append(verb)
        return ret

    def _split_test_train(self, threshold: int = 8, proportion: float = 0.5) -> None:
        """
        Splits the template:verbs dict into a training and a testing set.

        :param verb_template_pairs: list.
            List of tuples of (verb,template) e.g. ('abaisser','aim:er')
        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set.
            Must be between 0 and 1.

        """
        if proportion <= 0 or proportion > 1:
            raise ValueError(
                f"The split proportion ({proportion}) must be between 0 and 1."
            )
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set: list[VerbTemplatePair] = []
        test_set: list[VerbTemplatePair] = []
        for template, lverbs in self.dict_conjug.items():
            if len(lverbs) <= threshold:
                for verb in lverbs:
                    train_set.append((verb, template))
            else:
                index = round(len(lverbs) * proportion)
                for verb in lverbs[:index]:
                    train_set.append((verb, template))
                for verb in lverbs[index:]:
                    test_set.append((verb, template))
        random.shuffle(train_set)
        random.shuffle(test_set)
        self.train_input: list[str] = [elmt[0] for elmt in train_set]
        self.train_labels: list[int] = [
            self.templates.index(elmt[1]) for elmt in train_set
        ]
        self.test_input: list[str] = [elmt[0] for elmt in test_set]
        self.test_labels: list[int] = [
            self.templates.index(elmt[1]) for elmt in test_set
        ]
