import yaml

"""
from verbecc.core.defs.types.person import Person
from verbecc.core.defs.types.pronoun import Pronoun


class VerbeccYamlDumper(yaml.Dumper):
    # You can override methods here to customize dumping behavior.
    # For example, to handle custom objects, you'd add representers.
    pass


def represent_person(dumper: yaml.Dumper, data: Person):
    return dumper.represent_mapping("!Person", int(str(data)))


def represent_pronoun(dumper: yaml.Dumper, data: Pronoun):
    return dumper.represent_mapping("!Pronoun", str(data))


VerbeccYamlDumper.add_representer(Pronoun, represent_pronoun)
"""


class YAMLUtils:

    @classmethod
    def to_yaml(cls, data: object) -> str:
        return yaml.dump(data, allow_unicode=True)
