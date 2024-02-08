from abc import ABC
from typing import Union, List

import datetime as dt

from dwca.utils import Language
from eml.resources import EMLKeywordSet, EMLLicense, EMLDistribution, EMLCoverage
from eml.types import I18nString, EMLObject, Scope, ExtensionString, ResponsibleParty, EMLTextType, SemanticAnnotation


class Resource(EMLObject, ABC):
    """
    Abstract class representing any resources on an EML document

    Parameters
    ----------
    _id : str, optional
        Unique identifier
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined
    references_system : str, optional
        System attribute of reference
    alternative_identifier : List[ExtendedString], optional
        A list of secondary identifier for this entity.
    short_name : str, optional
        A short name that describes the resource, sometimes a filename.
    titles : List[I18nString or str]
        A brief description of the resource. At least one must be given.
    creators : List[ResponsibleParty]
        The people or organizations who created this resource. At least one must be given.
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
    licensed : List[EMLLicense], optional
        Information identifying a well-known license for the metadata and data.
    distribution : List[EMLDistribution], optional
        Information on how the resource is distributed online and offline.
    coverage : EMLCoverage, optional
        Extent of the coverage of the resource.
    annotation : List[SemanticAnnotation], optional
        A precisely-defined semantic statement about this resource.
    """
    def __init__(
            self,
            _id: str = None, scope: Scope = Scope.DOCUMENT, system: str = None,
            referencing: bool = False, references_system: str = None,
            alternative_identifier: List[ExtensionString] = None,
            short_name: str = None, titles: List[Union[I18nString, str]] = None,
            creators: List[ResponsibleParty] = None, metadata_providers: List[ResponsibleParty] = None,
            associated_parties: List[ResponsibleParty] = None, publication_date: dt.date = None,
            language: Union[Language, str] = Language.ENG, series: str = None,
            abstract: EMLTextType = None, keyword_set: List[EMLKeywordSet] = None,
            additional_info: List[EMLTextType] = None, intellectual_rights: EMLTextType = None,
            licensed: List[EMLLicense] = None, distribution: List[EMLDistribution] = None,
            coverage: EMLCoverage = None, annotation: List[SemanticAnnotation] = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        if self.referencing:
            return
        self.__short_name__ = short_name
        self.__titles__: List[I18nString] = list()
        if len(titles) == 0:
            raise ValueError("No titles provided")
        self.__titles__.extend([I18nString(title) for title in titles])
        self.__creators__: List[ResponsibleParty] = list()
        if len(creators) == 0:
            raise ValueError("No creators provided")
        self.__creators__.extend(creators)
        self.__alternative_identifier__: List[ExtensionString] = list()
        if alternative_identifier is not None:
            self.__alternative_identifier__.extend(alternative_identifier)
        self.__metadata_provider__: List[ResponsibleParty] = list()
        if metadata_providers is not None:
            self.__metadata_provider__.extend(metadata_providers)
        self.__associated__: List[ResponsibleParty] = list()
        if associated_parties is not None:
            self.__associated__.extend(associated_parties)
        self.__pub_date__ = publication_date
        self.__lang__ = None
        if isinstance(language, str):
            self.__lang__ = Language.get_language(language)
        elif isinstance(language, Language):
            self.__lang__ = language
        self.__series__ = series
        self.__abstract__ = abstract
        self.__keywords__: List[EMLKeywordSet] = list()
        if keyword_set is not None:
            self.__keywords__.extend(keyword_set)
        self.__add_info__: List[EMLTextType] = list()
        if additional_info is not None:
            self.__add_info__.extend(additional_info)
        self.__int_rights__ = intellectual_rights
        self.__licensed__: List[EMLLicense] = list()
        if licensed is not None:
            self.__licensed__.extend(licensed)
        self.__dist__: List[EMLDistribution] = list()
        if distribution is not None:
            self.__dist__.extend(distribution)
        self.__cover__ = coverage
        self.__annotation__: List[SemanticAnnotation] = list()
        if annotation is not None:
            self.__annotation__.extend(annotation)
        return

    @property
    def title(self) -> I18nString:
        """I18nString: A brief description of the resource."""
        return self.__titles__[0]

    @property
    def titles(self) -> List[I18nString]:
        """List[I18nString]: A brief description of the resource."""
        return self.__titles__

    @property
    def creator(self) -> ResponsibleParty:
        """ResponsibleParty: The person or organization who created this resource (First listed)."""
        return self.__creators__[0]

    @property
    def creators(self) -> List[ResponsibleParty]:
        """List[ResponsibleParty]: The people or organizations who created this resource."""
        return self.__creators__

    @property
    def alternative_identifiers(self) -> List[ExtensionString]:
        """List[ExtensionString]: A secondary identifier for this entity."""
        return self.__alternative_identifier__

    @property
    def short_name(self) -> str:
        """str: A short name that describes the resource, sometimes a filename."""
        return self.__short_name__

    @property
    def metadata_provider(self) -> List[ResponsibleParty]:
        """
        List[ResponsibleParty]: The people or organizations who created provided metadata for this resource.
        """
        return self.__metadata_provider__

    @property
    def associated_party(self) -> List[ResponsibleParty]:
        """
        List[ResponsibleParty]: Other people or organizations who should be associated with this resource.
        """
        return self.__associated__

    @property
    def publication_date(self) -> dt.date:
        """date: The publication date of the resource."""
        return self.__pub_date__

    @property
    def language(self) -> Language:
        """Language: The language in which the resource is written."""
        return self.__lang__

    @property
    def series(self) -> str:
        """str: The series from which the resource came."""
        return self.__series__

    @property
    def abstract(self) -> EMLTextType:
        """EMLTextType: A brief overview of the resource."""
        return self.__abstract__

    @property
    def keyword_set(self) -> List[EMLKeywordSet]:
        """List[EMLKeywordSet]: Keyword information that describes the resource."""
        return self.__keywords__

    @property
    def additional_info(self) -> List[EMLTextType]:
        """List[EMLTextType]: Any extra information pertinent to the resource."""
        return self.__add_info__

    @property
    def intellectual_rights(self) -> EMLTextType:
        """EMLTextType: Any extra information pertinent to the resource."""
        return self.__int_rights__

    @property
    def licensed(self) -> List[EMLLicense]:
        """List[EMLLicense]: Information identifying a well-known license for the metadata and data."""
        return self.__licensed__

    @property
    def distribution(self) -> List[EMLDistribution]:
        """List[EMLDistribution]: Information on how the resource is distributed online and offline."""
        return self.__dist__

    @property
    def coverage(self) -> EMLCoverage:
        """EMLCoverage: Extent of the coverage of the resource."""
        return self.__cover__

    @property
    def annotation(self) -> List[SemanticAnnotation]:
        """List[SemanticAnnotation]: A precisely-defined semantic statement about this resource."""
        return self.__annotation__
