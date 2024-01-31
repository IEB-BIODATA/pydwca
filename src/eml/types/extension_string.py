from __future__ import annotations
from typing import Dict, Union

from lxml import etree as et

from dwca.xml import XMLObject


class ExtensionString(XMLObject):
    """
    Extension string representing a string value with extra attributes.

    Parameters
    ----------
    value : str
        Value of the string.
    system : str, optional
        The data management system.
    """
    def __init__(self, value: str, system: str = None) -> None:
        super().__init__()
        self.__value__ = value
        self.__system__ = system
        self.__tag__ = None
        return

    @property
    def system(self) -> str:
        """str: The data management system within which an identifier is in scope and therefore unique."""
        return self.__system__

    def __str__(self) -> str:
        return self.__value__

    def __repr__(self) -> str:
        extension = ""
        if self.__system__ is not None:
            extension = f"system='{self.__system__}' "
        return f"<ExtensionString {extension}({self.__value__})>"

    def __eq__(self, other: Union[str, ExtensionString]) -> bool:
        if isinstance(other, str):
            return self.__value__ == other
        elif isinstance(other, ExtensionString):
            return self.__value__ == other.__value__ and self.system == other.system
        else:
            return False

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> ExtensionString | None:
        """
        Parses a lxml element into an Extension String.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        ExtensionString
            Object parsed.
        """
        if element is None:
            return None
        return ExtensionString(element.text, system=element.get("system", None))

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the extended string.

        Returns
        -------
        lxml.tree.Element
            Object in the XML Element format.

        Raises
        ------
        RuntimeError
            If tag is not set before calling this method.
        """
        if self.__tag__ is None:
            raise RuntimeError("First, set tag to call `to_element`")
        element = et.Element(self.__tag__)
        if self.__system__ is not None:
            element.set("system", self.__system__)
        element.text = self.__value__
        return element

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Always return True due tag not existing until set.

        Parameters
        ----------
        tag : str
            Any tag.
        nmap : Dict
            Namespace.
        """
        return

    def set_tag(self, tag: str) -> None:
        """
        Set tag for the element output.

        Parameters
        ----------
        tag : str
            Tag of the XML output element.

        Returns
        -------
        None
            Set tag.
        """
        self.__tag__ = tag
        return
