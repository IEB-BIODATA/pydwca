from __future__ import annotations
from typing import Dict

from lxml import etree as et

from eml.types import I18nString


class OrganizationName(I18nString):
    """
    The full name of the organization being described.
    """
    PRINCIPAL_TAG = "organizationName"

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> OrganizationName | None:
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
        return OrganizationName(element.text, lang=element.get(f"{{{cls.NAMESPACES['xml']}}}lang", "eng"))

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Checks if the tag is "organizationName"

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
        Generate a lxml.tree.Element from the organization name.

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
        return f"<Organization Name ({self.__value__}) [{self.language.name.lower()}]>"
