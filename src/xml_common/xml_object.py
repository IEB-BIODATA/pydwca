from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Union

from lxml import etree as et


class XMLObject(ABC):
    """
    Abstract class for XML Object, to be parsed on the read of the Darwin Core Archive file.
    """
    PRINCIPAL_TAG = "placeholder"
    """str : The principal tag of the XML document."""
    NAMESPACE_TAG = None
    """str : If the principal tag has a namespace attribute, this must be used."""
    NAMESPACES = {
        "xml": "http://www.w3.org/XML/1998/namespace"
    }
    """Dict[str, str] : Namespaces to use on the particular XML portion that represent the object."""

    def __init__(self) -> None:
        self.__namespace__ = dict()
        for prefix, uri in self.NAMESPACES.items():
            self.__namespace__[prefix] = uri
        return

    @classmethod
    def from_xml(cls, file: str, encoding: str = "utf-8") -> XMLObject:
        """
        Generates an XML Object from an XML file.

        Parameters
        ----------
        file : str
            Path to XML file.
        encoding : str, default "utf-8"
            Encoding of the XML file.

        Returns
        -------
        XMLObject
            Parsed XML object from XML file.
        """
        with open(file, "r", encoding=encoding) as file:
            content = file.read()
        return cls.from_string(content)

    @classmethod
    def from_string(cls, text: str) -> XMLObject:
        """
        Generates XML Object from a string of an XML file.

        Parameters
        ----------
        text : str
            XML File as a string.

        Returns
        -------
        XMLObject
            Object parsed from the string.
        """
        root = et.fromstring(text)
        nmap = dict()
        for prefix, uri in cls.NAMESPACES.items():
            nmap[prefix] = uri
        for prefix, uri in root.nsmap.items():
            nmap[prefix] = uri
        cls.check_principal_tag(root.tag, nmap)
        xml_object = cls.parse(root, nmap)
        xml_object.__namespace__ = nmap
        return xml_object

    @classmethod
    @abstractmethod
    def parse(cls, element: et.Element, nmap: Dict) -> XMLObject | None:
        """
        Parses a lxml element into an XMLObject.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        XMLObject
            Object parsed.
        """
        pass

    def to_xml(self) -> str:
        """
        Generates text of an XML file.

        Returns
        -------
        str
            Text of an XML File from the object.
        """
        return et.tostring(self.to_element(), pretty_print=True).decode()

    @abstractmethod
    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        return et.Element(self.get_principal_tag(), nsmap=self.__namespace__)

    def object_to_element(self, tag: str, prefix: Union[str, None] = None) -> et.Element:
        """
        Generates an element using tag, adding namespace tag.

        Parameters
        ----------
        tag : str
            Tag for XML Element.
        prefix : str, optional
            Prefix of namespace, default None.

        Returns
        -------
        lxml.tree.Element
            Generated element.
        """
        if prefix in self.__namespace__:
            return et.Element(f"{{{self.__namespace__[prefix]}}}{tag}")
        else:
            return et.Element(tag)

    def get_principal_tag(self) -> str:
        """
        Returns the principal tag with namespaces if it is present.

        Returns
        -------
        str
            Principal tag of the XML file.
        """
        if self.NAMESPACE_TAG is not None:
            return f"{{{self.__namespace__[self.NAMESPACE_TAG]}}}{self.PRINCIPAL_TAG}"
        if None in self.__namespace__:
            return f"{{{self.__namespace__[None]}}}{self.PRINCIPAL_TAG}"
        return self.PRINCIPAL_TAG

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Checks if the tag is the Principal tag of the object.

        Parameters
        ----------
        tag : str
            Tag obtained from outside source.
        nmap : Dict
            The namespace to check the format of the Principal tag.

        Raises
        ------
        AssertionError
            If the tag is not a representation of the principal tag of the object.
        """
        if cls.NAMESPACE_TAG is not None:
            expected = f"{{{nmap[cls.NAMESPACE_TAG]}}}{cls.PRINCIPAL_TAG}"
        elif None in nmap:
            expected = f"{{{nmap[None]}}}{cls.PRINCIPAL_TAG}"
        else:
            expected = f"{cls.PRINCIPAL_TAG}"
        assert tag == expected, f"{tag} is not {expected}"

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"<XMLObject tag={self.PRINCIPAL_TAG}>"
