from __future__ import annotations

from typing import Dict, List

from lxml import etree as et

from eml.resources import Resource
from eml.types import ExtensionString, I18nString, ResponsibleParty


class EMLDataset(Resource):
    """
    Dataset represents the base type for the dataset element on an EML document.

    Parameters
    ----------
    contact: List[ResponsibleParty]
        The contact for this dataset.

    Other Parameters
    ----------------
    **kwargs : :class:`eml.resources.resource.Resource` parameters.
        The parameters of every type of Resource.
    """
    PRINCIPAL_TAG = "dataset"

    def __init__(
            self,
            contact: List[ResponsibleParty] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__contact__ = list()
        if self.referencing:
            return
        if contact is None or len(contact) == 0:
            raise ValueError("No contact provided")
        self.__contact__.extend(contact)
        return

    @property
    def contacts(self) -> List[ResponsibleParty]:
        """List[ResponsibleParty]: The contact for this dataset."""
        return self.__contact__

    # TODO: Implement other attributes (https://eml.ecoinformatics.org/schema/eml_xsd#eml_dataset)

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLDataset:
        """
        Generate an EML Dataset referencing another EML Dataset.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references another dataset.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLDataset
            Object parsed that reference another dataset.
        """
        kwargs = super().parse_kwargs(element, nmap)
        return EMLDataset(**kwargs)

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLDataset:
        """
        Generate an EML Dataset that do not reference another dataset.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLDataset
            Object parsed.
        """
        kwargs = super().parse_kwargs(element, nmap)
        contact = list()
        for contact_elem in element.findall("contact", nmap):
            contact.append(ResponsibleParty.parse(contact_elem, nmap))
        return EMLDataset(
            contact=contact,
            **kwargs
        )

    def to_element(self) -> et.Element:
        """
        Generates an XML `Element` from this instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` from this instance
        """
        dataset = super().to_element()
        for contact in self.contacts:
            contact.set_tag("contact")
            dataset.append(contact.to_element())
        return dataset
