from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


class EMLProtocol(Resource):
    """
    EML Protocol Resource
    """
    def __init__(self) -> None:
        super().__init__("None")
        raise NotImplementedError("Protocol EML class not implemented yet")

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLProtocol:
        """
        Generate an EML Protocol referencing another EML Protocol.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references another protocol.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLProtocol
            Object parsed that reference another protocol.
        """
        pass

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLProtocol:
        """
        Generate an EML protocol that not reference another protocol.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLProtocol
            Object parsed.
        """
        pass

    def to_element(self) -> et.Element:
        """
        Generate an XML `Element` from this object

        Returns
        -------
        lxml.etree.Element
            XML `Element` from this object

        Raises
        ------
        NotImplementedError
            Protocol functionality not implemented yet
        """
        raise NotImplementedError("Protocol functionality not implemented yet")
