from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


class EMLCitation(Resource):
    """
    EML Citation Resource.

    Other Parameters
    ----------------
    **kwargs : :class:`eml.resources.resource.Resource` parameters.
        The parameters of every type of Resource.
    """
    PRINCIPAL_TAG = "citation"

    def __init__(
            self, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        return

    # TODO: Implement citation attributes (https://eml.ecoinformatics.org/schema/eml_xsd#eml_citation)

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
        references = element.find("references", nmap)
        return EMLCitation(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLCitation:
        """
        Generate an EML citation that do not reference another citation.

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
        """
        cite_elem = super().to_element()
        cite_elem = self._to_element_(cite_elem)
        return cite_elem
