from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources import Resource
from eml.types import ExtensionString, I18nString
from eml.types import Scope


class EMLDataset(Resource):
    """
    Dataset represents the base type for the dataset element on an EML document.

    Other Parameters
    ----------------
    """
    PRINCIPAL_TAG = "dataset"
    """str: Principal tag `dataset`"""

    def __init__(
            self, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        return

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
        references = element.find("references")
        return EMLDataset(
            _id=references.text,
            scope=element.get("scope", None),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

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
        titles = element.findall("title", nmap)
        extra_titles = list()
        if len(titles) == 0:
            raise ValueError("At least one Title must be present")
        the_title = None
        for title in titles:
            if the_title is None:
                the_title = I18nString.parse(title, nmap)
            else:
                extra_titles.append(I18nString.parse(title, nmap))
        short_name = element.find("shortName", nmap)
        if short_name is not None:
            short_name = short_name.text
        alternative_identifier = list()
        for ai in element.findall("alternativeIdentifier", nmap):
            alternative_identifier.append(ExtensionString.parse(ai, nmap))
        return EMLDataset(
            _id=element.get("id", None),
            scope=element.get("scope", None),
            system=element.get("system", None),
            titles=[the_title],
            short_name=short_name,
            alternative_identifier=alternative_identifier,
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
        references = self.generate_references_element()
        if references is not None:
            dataset.append(references)
        else:
            for title in [self.title] + self.extra_titles:
                title.set_tag("title")
                dataset.append(title.to_element())
            if self.short_name is not None:
                short_name = self.object_to_element("shortName")
                dataset.append(short_name)
            for alternative_id in self.alternative_identifiers:
                alternative_id.set_tag("alternativeIdentifier")
                dataset.append(alternative_id.to_element())
        return dataset
