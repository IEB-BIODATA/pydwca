from __future__ import annotations
from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class EMLInline(XMLObject):
    """
    Inline distribution.
    """
    PRINCIPAL_TAG = "inline"

    def __init__(self) -> None:
        super().__init__()
        return

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLInline | None:
        """
        Generate an EMLInline instance from an XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to be parsed.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLInline
            An instance with the information of the XML element.
        """
        if element is None:
            return None
        else:
            return EMLInline()

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance with the information of the EMLInline object.

        Returns
        -------
        lxml.etree.Element
            XML element instance.
        """
        return super().to_element()
