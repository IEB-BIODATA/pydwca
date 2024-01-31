from __future__ import annotations

from typing import Dict, Union, List

import lxml.etree as et

from dwca.utils import Language
from eml.types import Scope
from eml.resources import Resource
from eml.types import ExtensionString, I18nString


class EMLDataset(Resource):
    """
    Dataset represents the base type for the dataset element on an EML document.

    Parameters
    ----------
    _id : str, optional
        Identifier of the dataset.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    scope : str, optional
        The scope of the identifier.
    title : I18nString
        A brief description of the resource.
    creator : Placeholder
        The people or organizations who created this resource.
    short_name : str, optional
        A short name that describes the resource, sometimes a filename.
    alternative_identifier : List[ExtendedString], ExtendedString, optional
        An or a list of secondary identifier for this entity.
    other_titles : List[I18nString]
        Others brief description of the resource.
    other_creators : List[Placeholder]
        Others creators of this resource.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined.
    references_system : str, optional
        System attribute of reference.
    """
    PRINCIPAL_TAG = "dataset"
    """str: Principal tag `dataset`"""

    def __init__(
            self, _id: str = None, scope: Scope = Scope.DOCUMENT, system: str = None, title: I18nString = None,
            short_name: str = None, alternative_identifier: Union[List[ExtensionString], ExtensionString] = None,
            other_titles: List[I18nString] = None, referencing: bool = False, references_system: str = None
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__system__ = system
        self.__scope__ = scope
        self.__short_name__ = short_name
        self.__title__ = title
        self.__creator__ = None
        self.__metadata_provider__ = None
        self.__alternative_identifier__: List[ExtensionString] = list()
        if alternative_identifier is not None:
            if isinstance(alternative_identifier, list):
                self.__alternative_identifier__.extend(alternative_identifier)
            else:
                self.__alternative_identifier__.append(alternative_identifier)
        self.__extra_titles__ = list()
        if other_titles is not None:
            for other_title in other_titles:
                self.__extra_titles__.append(other_title)
        return

    @property
    def title(self) -> I18nString:
        """I18nString: A brief description of the resource"""
        return self.__title__

    @property
    def short_name(self) -> str:
        """str: A short name that describes the resource, sometimes a filename."""
        return self.__short_name__

    @property
    def alternative_identifiers(self) -> List[ExtensionString]:
        """List[ExtensionString]: A secondary identifier for this entity."""
        return self.__alternative_identifier__

    @property
    def extra_titles(self) -> List[I18nString]:
        """List[I18nString]: Others brief description of the resource"""
        return self.__extra_titles__

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
            references.text,
            element.get("system", None),
            element.get("scope", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLDataset:
        """
        Generate an EML Dataset that not reference another dataset.

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
            element.get("id", None),
            element.get("system", None),
            element.get("scope", None),
            title=the_title,
            short_name=short_name,
            alternative_identifier=alternative_identifier,
            other_titles=extra_titles,
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
