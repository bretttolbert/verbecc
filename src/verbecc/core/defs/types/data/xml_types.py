from typing import TypeAlias
from lxml import etree

"""
Type alias for an XML element, which is an instance of lxml.etree._Element.
This alias is used to provide type hints for functions that work with XML elements.
The XmlElement type is used throughout the codebase to represent XML elements in a type-safe manner
and to improve code readability.
The XmlElementTree type is an alias for lxml.etree._ElementTree, which represents an entire XML document tree.
"""

XmlParser : TypeAlias = etree.XMLParser
XmlElement : TypeAlias = etree._Element # type: ignore
XmlElementTree : TypeAlias = etree._ElementTree  # type: ignore
