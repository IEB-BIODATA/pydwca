from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


class EMLCitation(Resource):
    """
    EML Citation Resource
    """
    def __init__(self) -> None:
        super().__init__("None")
        raise NotImplementedError("Citation EML class not implemented yet")

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLCitation:
        """
        Generate an EML Citation referencing another EML Citation.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references another citation.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLCitation
            Object parsed that reference another citation.
        """
        pass

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLCitation:
        """
        Generate an EML citation that not reference another citation.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLCitation
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
            Citation functionality not implemented yet
        """
        raise NotImplementedError("Citation functionality not implemented yet")
