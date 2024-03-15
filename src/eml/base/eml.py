from __future__ import annotations

from typing import Dict, List, Tuple, Any

import datetime as dt
from lxml import etree as et

from dwca.utils import Language
from eml.base import EMLMetadata, EMLVersion
from eml.resources import EMLResource, EMLDataset, EMLCitation, EMLProtocol, EMLSoftware, Resource, EMLKeywordSet, \
    EMLLicense, EMLDistribution, EMLCoverage
from eml.types import Scope, SemanticAnnotation, AccessType, EMLObject, I18nString, ResponsibleParty, ExtensionString, \
    Role, EMLTextType


class EML(EMLObject):
    """
    Class representing an `Ecological Metadata Language <https://eml.ecoinformatics.org/>`_

    Parameters
    ----------
    package_id : str
        A globally unique identifier for the data package described by this EML that can be used to cite it elsewhere.
    system : str
        The data management system within which an identifier is in scope and therefore unique.
    resource_type : EMLResource
        Type of the resource: `dataset`, `citation`, `protocol` or `software.`
    version: EMLVersion, optional
        Version of the EML standard. Default: latest (2.2.0).
    language : Language, optional
        Language abbreviation to be used, defaults to `"eng"`
    access : AccessType, optional
        Access control rules for the entire resource, which can be overridden by access rules in distribution trees.
    additional_metadata : List[None], optional
        A flexible field for including any other relevant metadata that pertains to the resource being described.
    annotation: List[Tuple[SemanticAnnotation, str]], optional
        A list of precisely-defined semantic statements about this resource.
    """
    PRINCIPAL_TAG = "eml"
    NAMESPACE_TAG = "eml"
    """str: Namespace tag `eml`, to be replace for `{uri}tag`"""

    class Annotation:
        """
        A precisely-defined semantic statement about an element in the EML document.

        Parameters
        ----------
        semantic_annotation: SemanticAnnotation
            A semantically-precise statement about an EML element.
        references : str
            The id of the element being annotated.
        """
        def __init__(self, semantic_annotation: SemanticAnnotation, references: str) -> None:
            self.__annotation__ = semantic_annotation
            self.__ref__ = references
            return

        @property
        def annotation(self) -> SemanticAnnotation:
            """SemanticAnnotation: A semantically-precise statement about an EML element."""
            return self.__annotation__

        @property
        def references(self) -> str:
            """str: The id of the element being annotated."""
            return self.__ref__

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, EML.Annotation):
                return (
                        self.annotation == other.annotation and
                        self.references == other.references
                )
            elif isinstance(other, SemanticAnnotation):
                return self.annotation == other
            else:
                return False

    def __init__(
            self,
            package_id: str,
            system: str,
            resource_type: EMLResource,
            version: EMLVersion = EMLVersion.LATEST,
            language: Language = Language.ENG,
            access: AccessType = None,
            additional_metadata: List[Any] = None,
            annotation: List[Tuple[SemanticAnnotation, str]] = None
    ) -> None:
        super().__init__(None, Scope.SYSTEM, system, False)
        self.__schema_location__ = ""
        self.__package__ = package_id
        self.__lang__ = language
        self.__access__ = None
        self.__resource_type__ = resource_type
        self.__version__ = version
        if resource_type == EMLResource.DATASET:
            self.__resource_class__ = EMLDataset
        elif resource_type == EMLResource.CITATION:
            self.__resource_class__ = EMLCitation
        elif resource_type == EMLResource.SOFTWARE:
            self.__resource_class__ = EMLSoftware
        elif resource_type == EMLResource.PROTOCOL:
            self.__resource_class__ = EMLProtocol
        else:
            raise ValueError(f"{resource_type.name.lower()} is not allowed")
        self.__resource__ = None
        self.__kwargs__ = dict()
        self.__access__ = access
        self.__additional__ = list()
        if additional_metadata is not None:
            self.__additional__.extend(additional_metadata)
        self.__annotation__ = list()
        if annotation is not None:
            self.__annotation__.extend([EML.Annotation(a[0], a[1]) for a in annotation])
        return

    @property
    def package_id(self) -> str:
        """str: A globally unique identifier for the data package described by this EML that can be used to cite it."""
        return self.__package__

    @property
    def system(self) -> str:
        """str: The data management system within which an identifier is in scope and therefore unique."""
        return self.__system__

    @property
    def scope(self) -> Scope:
        """Scope: The scope of the identifier."""
        return self.__scope__

    @property
    def language(self) -> Language:
        """Language: The language of the resource."""
        return self.__lang__

    @property
    def resource_type(self) -> EMLResource:
        """EMLResource: The type of the resource."""
        return self.__resource_type__

    @property
    def resource(self) -> Resource:
        """Resource: The resource instance."""
        if self.__resource__ is None:
            try:
                self.__resource__ = self.__resource_class__(**self.__kwargs__)
                return self.__resource__
            except Exception as _:
                raise RuntimeError("Resource not initialized yet")
        return self.__resource__

    @property
    def access(self) -> AccessType:
        """None: Access control rules for the entire resource."""
        return self.__access__

    @property
    def additional_metadata(self) -> List[Any]:
        """List[Any]: A flexible field for including any other relevant metadata."""
        return self.__additional__

    @property
    def annotations(self) -> List[EML.Annotation]:
        """Annotation: A list of precisely-defined semantic statements about this resource."""
        return self.__annotation__

    def initialize_resource(
            self,
            titles: str | I18nString | List[str | I18nString],
            creators: ResponsibleParty | List[ResponsibleParty],
            **kwargs
    ) -> None:
        """
        Initialize the resource instance of this EML.

        Parameters
        ----------
        titles : str | I18nString | List[str | I18nString]
            The titles to initialize the resource with.
        creators : ResponsibleParty | List[ResponsibleParty]+
            The creators to initialize the resource with.

        Other Parameters
        ----------------
        **kwargs : Parameters given in :class:`eml.resources.resource.Resource` or any subclass.

        Returns
        -------
        None
        """
        proper_titles = list()
        if isinstance(titles, list):
            for title in titles:
                proper_titles.append(I18nString(title))
        else:
            proper_titles.append(I18nString(titles))
        self.__resource__ = self.__resource_class__(
            titles=proper_titles,
            creators=creators if isinstance(creators, list) else [creators],
            **kwargs
        )
        return

    def add_title(self, title: str | I18nString, language: Language = Language.ENG) -> None:
        """
        Add a new title to the EML.

        Parameters
        ----------
        title : str | I18nString
            The title as string or with language already
        language : Language, optional
            The language of the title. If the title given is a I18nString, this argument is discarded.

        Returns
        -------
        None
        """
        self.resource.__titles__.append(I18nString(title, language))
        return

    def add_creator(self, creator: ResponsibleParty) -> None:
        """
        Add a new creator to the EML.

        Parameters
        ----------
        creator : ResponsibleParty
            The creator to be added to the resource.

        Returns
        -------
        None
        """
        self.resource.__creators__.append(creator)
        return

    def add_alternative_identifier(self, alternative_identifier: str | ExtensionString) -> None:
        """
        Add an alternative identifier to the EML.

        Parameters
        ----------
        alternative_identifier : str | ExtensionString
            An alternative identifier.

        Returns
        -------
        None
        """
        self.resource.__alternative_identifier__.append(ExtensionString(alternative_identifier))
        return

    def set_short_name(self, short_name: str) -> None:
        """
        Set short name of Resource in the EML.

        Parameters
        ----------
        short_name : str
            A short name for the resource.

        Returns
        -------
        None
        """
        self.resource.__short_name__ = short_name
        return

    def add_metadata_provider(self, metadata_provider: ResponsibleParty) -> None:
        """
        Add metadata provider to the EML.

        Parameters
        ----------
        metadata_provider : ResponsibleParty
            A Metadata Provider of the resource in the EML.

        Returns
        -------
        None
        """
        self.resource.__metadata_provider__.append(metadata_provider)
        return

    def add_associated_party(self, associated_party: ResponsibleParty, role: Role) -> None:
        """
        Add metadata provider to the EML.

        Parameters
        ----------
        associated_party : ResponsibleParty
            An Associated Party of the resource in the EML.
        role : Role
            The role of the Associated Party.

        Returns
        -------
        None
        """
        self.resource.__associated__.append((associated_party, role))
        return

    def set_pub_date(self, date: dt.date) -> None:
        """
        Set publication date of the resource in the EML.

        Parameters
        ----------
        date : datetime.date
            Publication date.

        Returns
        -------
        None
        """
        self.resource.__pub_date__ = date
        return

    def set_language(self, language: Language) -> None:
        """
        Set language of the resource in the EML.

        Parameters
        ----------
        language : Language
            A Language enum instance.

        Returns
        -------
        None
        """
        self.resource.__lang__ = language
        return

    def set_series(self, series: str) -> None:
        """
        Set series of the resource in the EML.

        Parameters
        ----------
        series : str
            The series from which the resource came.

        Returns
        -------
        None
        """
        self.resource.__series__ = series
        return

    def set_abstract(self, abstract: EMLTextType) -> None:
        """
        Set abstract of the resource in the EML.

        Parameters
        ----------
        abstract : EMLTextType
            An abstract in the required :class:`eml.types.text_type.EMLTextType` instance format.

        Returns
        -------
        None
        """
        self.resource.__abstract__ = abstract
        return

    def add_keyword_set(self, keyword_set: EMLKeywordSet) -> None:
        """
        Add keyword set to the resource in the EML.

        Parameters
        ----------
        keyword_set : EMLKeywordSet
            An instance of :class:`eml.resources.keyword_set.EMLKeywordSet`.

        Returns
        -------
        None
        """
        self.resource.__keywords__.append(keyword_set)
        return

    def add_additional_info(self, additional_info: EMLTextType) -> None:
        """
        Add additional info to the resource in the EML.

        Parameters
        ----------
        additional_info : EMLTextType
            Additional info in the required :class:`eml.types.text_type.EMLTextType` instance format.

        Returns
        -------
        None
        """
        self.resource.__add_info__.append(additional_info)
        return

    def set_intellectual_rights(self, intellectual_rights: EMLTextType) -> None:
        """
        Set intellectual rights of the resource in the EML.

        Parameters
        ----------
        intellectual_rights : EMLTextType
            The intellectual rights in the required :class:`eml.types.text_type.EMLTextType` instance format.

        Returns
        -------
        None
        """
        self.resource.__int_rights__ = intellectual_rights
        return

    def add_licensed(self, licensed: EMLLicense) -> None:
        """
        Add licensed to the resource in the EML.

        Parameters
        ----------
        licensed : EMLLicense
            An license instance.

        Returns
        -------
        None
        """
        self.resource.__licensed__.append(licensed)
        return

    def add_distribution(self, distribution: EMLDistribution) -> None:
        """
        Add distribution to the resource in the EML.

        Parameters
        ----------
        distribution : EMLDistribution
            An instance of :class:`eml.resources.distribution.distribution.EMLDistribution`.

        Returns
        -------
        None
        """
        self.resource.__dist__.append(distribution)
        return

    def set_coverage(self, coverage: EMLCoverage) -> None:
        """
        Set coverage of the resource in the EML.

        Parameters
        ----------
        coverage : EMLCoverage
            An instance of :class:`eml.resources.coverage.coverage.EMLCoverage`.

        Returns
        -------
        None
        """
        self.resource.__cover__ = coverage
        return

    def add_annotation(self, annotation: SemanticAnnotation) -> None:
        """
        Add annotation to the resource in the EML.

        Parameters
        ----------
        annotation : SemanticAnnotation
            An annotation in the :class:`eml.types.semantic_annotation.SemanticAnnotation` instance format.

        Returns
        -------
        None
        """
        self.resource.annotate(annotation)
        return

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLObject:
        """
        EML cannot have references.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Raises
        ------
        ValueError
            EML cannot reference another EML.
        """
        raise ValueError("EML cannot reference another EML")

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EML:
        """
        Generate an EML instance object using an XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EML
            EML instance.
        """
        assert element.get("packageId", None) is not None, "`packageId` attribute is not present in document"
        access = None
        access_elem = element.find("access", nmap)
        if access_elem is not None:
            access = AccessType.parse(access_elem, nmap)
        additional_metadata = list()
        for add_metadata in element.findall("additionalMetadata", nmap):
            additional_metadata.append(EMLMetadata.parse(add_metadata, nmap))
        annotation = list()
        annotations_elem = element.find("annotations", nmap)
        if annotations_elem is not None:
            for annotation_elem in annotations_elem.findall("annotation", nmap):
                annotation.append((
                    SemanticAnnotation.parse(annotation_elem, nmap),
                    annotation_elem.get("references", None)
                ))
        eml = EML(
            package_id=element.get("packageId"),
            system=element.get("system"),
            resource_type=EMLResource.get_resource_type(element),
            version=EMLVersion.get_version(element.get(f"{{{nmap['xsi']}}}schemaLocation", None)),
            language=Language.get_language(element.get(f"{{{nmap['xml']}}}lang", "eng")),
            access=access,
            additional_metadata=additional_metadata,
            annotation=annotation
        )
        eml.__resource__ = eml.__resource_class__.parse(
            element.find(eml.__resource_type__.name.lower()), nmap
        )
        eml.__namespace__ = nmap
        return eml

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance using the EML information.

        Returns
        -------
        :class:`lxml.etree.Element`
            XML element instance.
        """
        try:
            root = super().to_element()
        except KeyError:
            for key, value in self.__version__.get_namespace().items():
                self.__namespace__[key] = value
            root = super().to_element()
        root.set("packageId", self.package_id)
        root.set(f"{{{self.__namespace__['xsi']}}}schemaLocation", " ".join(self.__version__.schema_location()))
        root.set("system", self.system)
        root.set("scope", self.scope.name.lower())
        root.set(f"{{{self.__namespace__['xml']}}}lang", self.language.name.lower())
        root.append(self.resource.to_element())
        if self.access is not None:
            root.append(self.access.to_element())
        for add_meta in self.additional_metadata:
            root.append(add_meta.to_element())
        if len(self.annotations) > 0:
            annotations_elem = self.object_to_element("annotations")
            for annotation in self.annotations:
                annotation.annotation.set_tag("annotation")
                annotation_elem = annotation.annotation.to_element()
                annotation_elem.set("references", annotation.references)
                annotations_elem.append(annotation_elem)
            root.append(annotations_elem)
        return root

    def __str__(self) -> str:
        return f"EML:\n\tResource Type: {self.resource_type.name}\n{self.resource}"

    # TODO: Method to make sure elements added references existing ones.
