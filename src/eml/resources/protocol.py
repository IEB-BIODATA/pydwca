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
    PRINCIPAL_TAG = "protocol"

    def __init__(
            self, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        return

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
        references = element.find("references", nmap)
        return EMLProtocol(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

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
        """
        protocol_elem = super().to_element()
        protocol_elem = self._to_element_(protocol_elem)
        return protocol_elem
