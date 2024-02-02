from abc import ABC
from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class _NoTagObject(XMLObject, ABC):
    """
    Abstract class of object with no tag on EML schema
    """
    def __init__(self) -> None:
        super().__init__()
        self.__tag__ = None
        return

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the Responsible Party object.

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
        return et.Element(self.__tag__)

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Always return True due tag not existing until set

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
