from __future__ import annotations

from typing import Dict, Union, List

from lxml import etree as et
import datetime as dt

from dwca.utils import Language
from eml.resources import Resource, EMLKeywordSet, EMLLicense
from eml.types import ExtensionString, I18nString, EMLTextType
from eml.types import Scope, ResponsibleParty


class EMLDataset(Resource):
    """
    Dataset represents the base type for the dataset element on an EML document.

    Parameters
    ----------
    titles : List[I18nString or str]
        A brief description of the resource. At least one must be given.
    creators : List[ResponsibleParty]
        The people or organizations who created this resource. At least one must be given.
    _id : str, optional
        Identifier of the dataset.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    scope : str, optional
        The scope of the identifier.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined.
    references_system : str, optional
        System attribute of reference.
    alternative_identifier : List[ExtendedString], ExtendedString, optional
        An or a list of secondary identifier for this entity.
    short_name : str, optional
        A short name that describes the resource, sometimes a filename.
    metadata_providers : List[ResponsibleParty], optional
        The people or organizations who created provided documentation and other metadata for this resource.
    associated_parties : List[ResponsibleParty], optional
        Other people or organizations who should be associated with this resource.
    publication_date : date, optional
        The publication date of the resource.
    language : Language or str, optional
        The language in which the resource is written.
    series : str, optional
        The series from which the resource came.
    abstract : EMLTextType, optional
        A brief overview of the resource.
    keyword_set : List[EMLKeywordSet], optional
        Keyword information that describes the resource.
    additional_info: List[EMLTextType], optional
        Any extra information pertinent to the resource.
    intellectual_rights : EMLTextType, optional
        Intellectual property rights regarding usage and licensing of this resource.
    """
    PRINCIPAL_TAG = "dataset"
    """str: Principal tag `dataset`"""

    def __init__(
            self, titles: List[Union[I18nString, str]], creators: List[ResponsibleParty],
            _id: str = None, scope: Scope = Scope.DOCUMENT, system: str = None,
            referencing: bool = False, references_system: str = None,
            alternative_identifier: Union[List[ExtensionString], ExtensionString] = None,
            short_name: str = None, metadata_providers: List[ResponsibleParty] = None,
            associated_parties: List[ResponsibleParty] = None, publication_date: dt.date = None,
            language: Union[Language, str] = Language.ENG, series: str = None,
            abstract: str = EMLTextType, keyword_set: List[EMLKeywordSet] = None,
            additional_info: List[EMLTextType] = None, intellectual_rights: EMLTextType = None,
            licence: List[EMLLicense] = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__system__ = system
        self.__scope__ = scope
        self.__short_name__ = short_name
        self.__titles__: List[I18nString] = list()
        for title in titles:
            self.__titles__.append(I18nString(title))
        self.__creators__: List[ResponsibleParty] = creators
        self.__metadata_provider__ = None
        self.__alternative_identifier__: List[ExtensionString] = list()
        if alternative_identifier is not None:
            if isinstance(alternative_identifier, list):
                self.__alternative_identifier__.extend(alternative_identifier)
            else:
                self.__alternative_identifier__.append(alternative_identifier)
        self.__extra_titles__ = list()
        return

    @property
    def title(self) -> I18nString:
        """I18nString: A brief description of the resource"""
        return self.__titles__[0]

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
