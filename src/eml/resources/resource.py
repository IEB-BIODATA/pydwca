from __future__ import annotations

from abc import ABC
from typing import Union, List, Dict, Tuple

import datetime as dt

from lxml import etree as et

from dwca.utils import Language
from eml.resources import EMLKeywordSet, EMLLicense, EMLDistribution, EMLCoverage
from eml.types import I18nString, EMLObject, Scope, ExtensionString, ResponsibleParty, EMLTextType, SemanticAnnotation, \
    Role


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
    associated_parties : List[Tuple[ResponsibleParty, Role]], optional
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
            associated_parties: List[Tuple[ResponsibleParty, Role]] = None, publication_date: dt.date = None,
            language: Union[Language, str] = None, series: str = None,
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
        if titles is None or len(titles) == 0:
            raise ValueError("No titles provided")
        self.__titles__.extend([I18nString(title) for title in titles])
        self.__creators__: List[ResponsibleParty] = list()
        if creators is None or len(creators) == 0:
            raise ValueError("No creators provided")
        self.__creators__.extend(creators)
        self.__alternative_identifier__: List[ExtensionString] = list()
        if alternative_identifier is not None:
            self.__alternative_identifier__.extend(alternative_identifier)
        self.__metadata_provider__: List[ResponsibleParty] = list()
        if metadata_providers is not None:
            self.__metadata_provider__.extend(metadata_providers)
        self.__associated__: List[Tuple[ResponsibleParty, Role]] = list()
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
        if len(self.__annotation__) > 0 and self.__id__ is None:
            raise ValueError("If annotations are given, resource must have an id.")
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
    def associated_party(self) -> List[Tuple[ResponsibleParty, Role]]:
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

    def annotate(self, annotation: SemanticAnnotation) -> None:
        """
        Annotate this resource.

        Parameters
        ----------
        annotation : SemanticAnnotation
            An annotation in the :class:`eml.types.semantic_annotation.SemanticAnnotation` instance format.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the resource does not have a unique id, it cannot be annotated.
        """
        if self.__id__ is None:
            raise ValueError("If annotations are given, resource must have an id.")
        self.__annotation__.append(annotation)
        return

    @classmethod
    def parse_kwargs(cls, element: et.Element, nmap: Dict) -> Dict:
        """
        Parse an element to generate the common parameters of Resource classes.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        Dict
            Other arguments (kwargs) of the recourse class.
        """
        kwargs = dict()
        references_elem = element.find("references", nmap)
        kwargs["scope"] = cls.get_scope(element)
        kwargs["system"] = element.get("system", None)
        if references_elem is not None:
            kwargs["_id"] = references_elem.text
            kwargs["referencing"] = True
            kwargs["references_system"] = references_elem.get("system", None)
            return kwargs
        kwargs["_id"] = element.get("id", None)
        kwargs["referencing"] = False
        short_elem = element.find("shortName", nmap)
        if short_elem is not None:
            kwargs["short_name"] = short_elem.text
        kwargs["titles"] = list()
        for title in element.findall("title", nmap):
            kwargs["titles"].append(I18nString.parse(title, nmap))
        kwargs["creators"] = list()
        for creator in element.findall("creator", nmap):
            kwargs["creators"].append(ResponsibleParty.parse(creator, nmap))
        kwargs["alternative_identifier"] = list()
        for alt_id in element.findall("alternateIdentifier", nmap):
            kwargs["alternative_identifier"].append(ExtensionString.parse(alt_id, nmap))
        kwargs["metadata_providers"] = list()
        for meta_prov in element.findall("metadataProvider", nmap):
            kwargs["metadata_providers"].append(ResponsibleParty.parse(meta_prov, nmap))
        kwargs["associated_parties"] = list()
        for assoc_party in element.findall("associatedParty", nmap):
            kwargs["associated_parties"].append((
                ResponsibleParty.parse(assoc_party, nmap),
                ResponsibleParty.get_role(assoc_party, nmap)
            ))
        pub_date_elem = element.find("pubDate", nmap)
        if pub_date_elem is not None:
            kwargs["publication_date"] = dt.datetime.strptime(pub_date_elem.text, "%Y-%m-%d").date()
        lang_elem = element.find("language", nmap)
        if lang_elem is not None:
            kwargs["language"] = lang_elem.text
        series_elem = element.find("series", nmap)
        if series_elem is not None:
            kwargs["series"] = series_elem.text
        abs_elem = element.find("abstract", nmap)
        if abs_elem is not None:
            kwargs["abstract"] = EMLTextType.parse(abs_elem, nmap)
        kwargs["keyword_set"] = list()
        for keyword_elem in element.findall("keywordSet", nmap):
            kwargs["keyword_set"].append(EMLKeywordSet.parse(keyword_elem, nmap))
        kwargs["additional_info"] = list()
        for add_info in element.findall("additionalInfo", nmap):
            kwargs["additional_info"].append(EMLTextType.parse(add_info, nmap))
        int_right_elem = element.find("intellectualRights", nmap)
        if int_right_elem is not None:
            kwargs["intellectual_rights"] = EMLTextType.parse(int_right_elem, nmap)
        kwargs["licensed"] = list()
        for licensed_elem in element.findall("licensed", nmap):
            kwargs["licensed"].append(EMLLicense.parse(licensed_elem, nmap))
        kwargs["distribution"] = list()
        for dist_elem in element.findall("distribution", nmap):
            kwargs["distribution"].append(EMLDistribution.parse(dist_elem, nmap))
        cover_elem = element.find("coverage", nmap)
        if cover_elem is not None:
            kwargs["coverage"] = EMLCoverage.parse(cover_elem, nmap)
        kwargs["annotation"] = list()
        for annotation_elem in element.findall("annotation", nmap):
            kwargs["annotation"].append(SemanticAnnotation.parse(annotation_elem, nmap))
        return kwargs

    def to_element(self) -> et.Element:
        """
        Generate an XML Element instance from the Resource.

        Returns
        -------
        lxml.etree.Element
            XML element instance.
        """
        element = super().to_element()
        element = self._to_element_(element)
        if self.referencing:
            return element
        for alt_id in self.alternative_identifiers:
            alt_id.set_tag("alternateIdentifier")
            element.append(alt_id.to_element())
        if self.short_name is not None:
            short_elem = self.object_to_element("shortName")
            short_elem.text = self.short_name
            element.append(short_elem)
        for title in self.titles:
            title.set_tag("title")
            element.append(title.to_element())
        for creator in self.creators:
            creator.set_tag("creator")
            element.append(creator.to_element())
        for meta_prov in self.metadata_provider:
            meta_prov.set_tag("metadataProvider")
            element.append(meta_prov.to_element())
        for assoc_party in self.associated_party:
            assoc_party[0].set_tag("associatedParty")
            assoc_elem = assoc_party[0].to_element()
            role_elem = self.object_to_element("role")
            role_elem.text = assoc_party[1].to_camel_case()
            assoc_elem.append(role_elem)
            element.append(assoc_elem)
        if self.publication_date is not None:
            pub_elem = self.object_to_element("pubDate")
            pub_elem.text = self.publication_date.strftime("%Y-%m-%d")
            element.append(pub_elem)
        if self.language is not None:
            lang_elem = self.object_to_element("language")
            lang_elem.text = self.language.name.lower()
            element.append(lang_elem)
        if self.series is not None:
            series_elem = self.object_to_element("series")
            series_elem.text = self.series
            element.append(series_elem)
        if self.abstract is not None:
            self.abstract.set_tag("abstract")
            element.append(self.abstract.to_element())
        for keyword in self.keyword_set:
            element.append(keyword.to_element())
        for add_info in self.additional_info:
            add_info.set_tag("additionalInfo")
            element.append(add_info.to_element())
        if self.intellectual_rights is not None:
            self.intellectual_rights.set_tag("intellectualRights")
            element.append(self.intellectual_rights.to_element())
        for licence in self.licensed:
            element.append(licence.to_element())
        for dist in self.distribution:
            element.append(dist.to_element())
        if self.coverage is not None:
            element.append(self.coverage.to_element())
        for annotation in self.annotation:
            annotation.set_tag("annotation")
            element.append(annotation.to_element())
        return element

    def __str__(self) -> str:
        creators = "\n\t\t".join([str(creator) for creator in self.creators])
        creator_label = "Creator" if len(self.creators) <= 1 else "Creators"
        metadata_provider = "\n\t\t".join([str(metadata_provider) for metadata_provider in self.metadata_provider])
        associated_party = list()
        for assoc, role in self.associated_party:
            associated_party.append(f"\t{role}: {assoc}")
        assoc_text = "\n".join(associated_party)
        return (f"\tTitle: {self.title}\n"
                f"\t{creator_label}: {creators}\n"
                f"\tMetadataProvider: {metadata_provider}\n"
                f"{assoc_text}")
