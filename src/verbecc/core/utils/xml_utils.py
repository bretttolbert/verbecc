from pathlib import Path
from typing import cast

from lxml import etree
from lxml import objectify

from verbecc.core.defs.types.data.xml_types import XmlElement, XmlElementTree, XmlParser

"""
XML Utility functions for working with lxml.etree._Element objects in order
to abstract away the dependency on lxml.etree, improving readability and maintainability.
This module provides utility functions for converting XML elements to string representations.
This also defines type aliases for XML elements and XML element trees to improve code readability 
and type safety.
Type Aliases:
    XmlElement: An alias for lxml.etree._Element, representing an XML element.
    XmlElementTree: An alias for lxml.etree._ElementTree, representing an entire XML document tree.
"""

def xml_element_to_string(elem: XmlElement,
        encoding: str="utf-8",
        method: str="xml",
        pretty_print: bool=True,
        xml_declaration: bool=True) -> str:
    """
    Converts an XML element to a string representation.
    Args:
        elem (XmlElement): The XML element to convert.
    Returns:
        str: A string representation of the XML element."""
    return str(etree.tostring(cast(etree._Element, elem), encoding=encoding, method=method, xml_declaration=xml_declaration, pretty_print=pretty_print))  # type: ignore


def xml_parse(path: Path, parser: XmlParser) -> XmlElementTree:
    """
    Parses an XML file and returns the corresponding XML element tree.
    Args:
        path (Path): The path to the XML file to parse.
        parser (XmlParser): An instance of lxml.etree.XMLParser to use for parsing.
    Returns:
        XmlElementTree: The parsed XML element tree."""
    return etree.parse(path, parser)


def xml_element_deannotate(elem: XmlElement) -> None:
    """
    Removes annotations from an XML element and its descendants.
    Args:
        elem (XmlElement): The XML element to deannotate.
    """
    objectify.deannotate(elem, cleanup_namespaces=True)


def xml_element_get_tag(elem: XmlElement) -> str:
    """
    Returns the tag name of an XML element.
    Args:
        elem (XmlElement): The XML element to get the tag name from.
    Returns:
        str: The tag name of the XML element."""
    return cast(str, elem.tag) # type: ignore


def xml_element_repr(elem: XmlElement) -> str:
    return f"{xml_element_get_tag(elem)}: {elem} {xml_element_to_string(elem)}"


def xml_element_xpath(elem: XmlElement, xpath_expr: str) -> list[XmlElement]:
    """
    Evaluates an XPath expression on an XML element and returns the matching elements.
    Args:
        elem (XmlElement): The XML element to evaluate the XPath expression on.
        xpath_expr (str): The XPath expression to evaluate.
    Returns:
        list[XmlElement]: A list of matching XML elements."""
    return cast(list[XmlElement], elem.xpath(xpath_expr)) # type: ignore


def xml_element_remove(parent_elem: XmlElement, target_elem: XmlElement) -> None:
    """
    Removes an XML element from its parent.
    Args:
        parent_elem (XmlElement): The parent XML element.
        target_elem (XmlElement): The target XML element to remove.
    """
    cast(etree._Element, parent_elem).remove(cast(etree._Element, target_elem))  # type: ignore


def xml_element_get_attr(elem: XmlElement, attr_name: str, default: str | None = None) -> str | None:
    """
    Retrieves the value of an attribute from an XML element.
    Args:
        elem (XmlElement): The XML element to retrieve the attribute from.
        attr_name (str): The name of the attribute to retrieve.
        default (str, optional): The default value to return if the attribute is not found. Defaults to None.
    Returns:
        str: The value of the attribute, or the default value if not found."""
    return cast(str, elem.get(attr_name, default=default))  # type: ignore


def xml_element_find(elem: XmlElement, tag: str) -> XmlElement | None:
    """
    Finds a child element with a specific tag name.
    Args:
        elem (XmlElement): The XML element to search within.
        tag (str): The tag name to search for.
    Returns:
        list[XmlElement]: A list of matching child XML elements."""
    return cast(XmlElement | None, elem.find(tag))  # type: ignore


def xml_element_findall(elem: XmlElement, tag: str) -> list[XmlElement]:
    """
    Finds all child elements with a specific tag name.
    Args:
        elem (XmlElement): The XML element to search within.
        tag (str): The tag name to search for.
    Returns:
        list[XmlElement]: A list of matching child XML elements."""
    return cast(list[XmlElement], elem.findall(tag))  # type: ignore


def xml_element_get_text(elem: XmlElement) -> str | None:
    """
    Retrieves the text content of an XML element.
    Args:
        elem (XmlElement): The XML element to retrieve the text from.
    Returns:
        str: The text content of the XML element."""
    return cast(str, elem.text)  # type: ignore