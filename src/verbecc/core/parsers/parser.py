from abc import ABC, abstractmethod
from typing import Optional

from verbecc.core.defs.types.data.element import Element
from verbecc.core.defs.types.data.xml_types import XmlElement

class Parser(ABC):

    @abstractmethod
    def parse(self, elem: Optional[XmlElement] = None) -> Element:
        pass
