from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


class EMLSoftware(Resource):
    """
    EML Software Resource.

    Other Parameters
    ----------------
    """
    def __init__(self, **kwargs) -> None:
        # To avoid initialization
        super().__init__(referencing=True, **kwargs)
        raise NotImplementedError("Software EML class not implemented yet")

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLSoftware:
        """
        Generate an EML Software referencing another EML Software.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references another software.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLSoftware
            Object parsed that reference another software.
        """
        pass

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLSoftware:
        """
        Generate an EML software that do not reference another software.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLSoftware
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
            Software functionality not implemented yet
        """
        raise NotImplementedError("Software functionality not implemented yet")
