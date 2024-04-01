from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


# TODO: Implement Protocol Resource (https://eml.ecoinformatics.org/schema/eml_xsd#eml_protocol)
class EMLProtocol(Resource):
    """
    EML Protocol Resource.

    Other Parameters
    ----------------
    **kwargs : :class:`eml.resources.resource.Resource` parameters.
        The parameters of every type of Resource.
    """
    def __init__(self, **kwargs) -> None:
        # To avoid initialization
        # super().__init__(referencing=True, **kwargs)
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
        Generate an EML protocol that do not reference another protocol.

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
