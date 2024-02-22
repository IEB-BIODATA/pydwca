from __future__ import annotations
from typing import Dict

from lxml import etree as et

from eml.types import I18nString


class PositionName(I18nString):
    """
    The name of the title or position associated with the resource.
    """
    PRINCIPAL_TAG = "positionName"

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> PositionName | None:
        """
        Parses a lxml element into an Organization Name.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        OrganizationName
            Object parsed.
        """
        if element is None:
            return None
        return PositionName(element.text, lang=element.get(f"{{{cls.NAMESPACES['xml']}}}lang", "eng"))

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Checks if the tag is "positionName"

        Parameters
        ----------
        tag : str
            Tag obtained from outside source.
        nmap : Dict
            The namespace to check the format of the principal tag.

        Raises
        ------
        AssertionError
            If the tag is not a representation of the principal tag of the object.
        """
        return super(I18nString, cls).check_principal_tag(tag, nmap)

    def set_tag(self, tag: str) -> None:
        """
        To not be used.

        Parameters
        ----------
        tag : str
            Any tag.

        Returns
        -------
        None
        """
        return

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the position name.

        Returns
        -------
        lxml.tree.Element
            Object in the XML Element format.
        """
        element = et.Element(self.PRINCIPAL_TAG)
        element.text = self.__value__
        element.set(f"{{{self.__namespace__['xml']}}}lang", self.__lang__.name.lower())
        return element

    def __repr__(self) -> str:
        return f"<Position Name ({self.__value__}) [{self.language.name.lower()}]>"
