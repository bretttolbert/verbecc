from abc import ABC, abstractmethod

from lxml import etree
from lxml.etree import Element

from verbecc.src.defs.types.data.element import Element


class Parser(ABC):

    @abstractmethod
    def parse(elem: etree._Element) -> Element:
        pass
