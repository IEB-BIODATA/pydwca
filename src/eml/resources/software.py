from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource


# TODO: Implement Software Resource (https://eml.ecoinformatics.org/schema/eml_xsd#eml_software)
class EMLSoftware(Resource):
    """
    EML Software Resource.

    Other Parameters
    ----------------
    **kwargs : :class:`eml.resources.resource.Resource` parameters.
        The parameters of every type of Resource.
    """
    PRINCIPAL_TAG = "software"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        return

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
        references = element.find("references", nmap)
        return EMLSoftware(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

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
        """
        software_elem = super().to_element()
        software_elem = self._to_element_(software_elem)
        return software_elem
