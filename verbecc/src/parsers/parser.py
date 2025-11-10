from abc import ABC, abstractmethod
from lxml import etree
from typing import Optional

from verbecc.src.defs.types.data.element import Element


class Parser(ABC):

    @abstractmethod
    def parse(self, elem: Optional[etree._Element] = None) -> Element:
        pass
