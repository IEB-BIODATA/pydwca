from __future__ import annotations
from typing import Dict, List, Tuple, Any

from lxml import etree as et

from dwca.xml import XMLObject
from eml.types import EMLObject, Scope, ResponsibleParty


class TaxonomicCoverage(EMLObject):
    """
    Taxonomic coverage information.

    Parameters
    ----------
    _id : str, optional
        Unique identifier within the scope.
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined.
    references_system : str, optional
        System attribute of reference.
    taxonomic_system : TaxonomicSystem, optional
        Documentation of taxonomic sources, procedures, and treatments.
    general_coverage : str, optional
        A description of the range of taxa addressed in the data set or collection.
    classification : List[ClassificationSystem], optional
        Information about the range of taxa addressed in the data set or collection.
    """
    class ClassificationSystem:
        """
        Information about the classification system or authority used.

        Parameters
        ----------
        citation : EMLCitation
            Relevant literature for documenting the used classification system.
        modifications : str, optional
            A description of any modifications or exceptions made to the classification system or authority used.
        """
        def __init__(self, citation: EMLObject, modifications: str = None) -> None:
            self.__cite__ = citation
            self.__modifications__ = modifications

        @property
        def citation(self) -> EMLObject:
            """EMLCitation: Relevant literature for documenting the used classification system."""
            return self.__cite__

        @property
        def modifications(self) -> str:
            """
            str: A description of any modifications or exceptions made to the classification system or authority used.
            """
            return self.__modifications__

    class Voucher:
        """
        Information on the types of specimen, the repository, and the individuals who identified the vouchers.

        Parameters
        ----------
        specimen : str
            A word or phrase describing the type of specimen collected.
        repository : List[ResponsibleParty]
            Information about the curator or contact person and/or agency responsible for the specimens.
        """
        def __init__(self, specimen: str, repository: List[ResponsibleParty]) -> None:
            self.__specimen__ = specimen
            self.__repository__ = repository

        @property
        def specimen(self) -> str:
            """str: A word or phrase describing the type of specimen collected."""
            return self.__specimen__

        @property
        def repository(self) -> List[ResponsibleParty]:
            """List[ResponsibleParty]: Information about the responsible for the specimens."""
            return self.__repository__

    class TaxonID:
        """
        Element holds an ID and ID-provider for this taxon.

        Parameters
        ----------
        _id: int
            The identifier for this taxon from an authority.
        provider: str
            The taxonomic authority from which the taxonId can be retrieved, defined as the namespace URI.
        """
        def __init__(self, _id: int, provider: str) -> None:
            self.__id__ = _id
            self.__provider__ = provider
            return

        @property
        def id(self) -> int:
            """int: The identifier for this taxon from an authority."""
            return self.__id__

        @property
        def provider(self) -> str:
            """str: The taxonomic authority from which the taxonId can be retrieved, defined as the namespace URI."""
            return self.__provider__

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, int):
                return self.id == other
            elif isinstance(other, TaxonomicCoverage.TaxonID):
                return self.id == other.id and self.provider == other.provider
            else:
                return False

    class TaxonomicSystem(XMLObject):
        """
        Documentation of taxonomic sources, procedures, and treatments.

        Parameters
        ----------
        procedures : str
            Description of the methods used for the taxonomic identification.
        classification_system : List[EMLCitation]
             Relevant literature for documenting the used classification system.
        identifier_name : List[ResponsibleParty]
             Information about the individual(s) responsible for the identification(s) of the specimens or sightings.
        identification_reference : List[EMLCitation], optional
            Information on any non-authoritative materials.
        completeness : str, optional
            Taxonomic completeness.
        vouchers : List[Tuple[str, List[ResponsibleParty]]], optional
            Information on the types of specimen, the repository, and the individuals who identified the vouchers.
        modifications : List[str], optional
            A description of any modifications or exceptions made to the classification system or authority used.
        """
        PRINCIPAL_TAG = "taxonomicSystem"

        def __init__(
                self, procedures: str,
                classification_system: List,
                identifier_name: List[ResponsibleParty],
                identification_reference: List = None,
                completeness: str = None,
                vouchers: List[Tuple[str, List[ResponsibleParty]]] = None,
                modifications: List[str] = None,
        ) -> None:
            super().__init__()
            self.__procedures__ = procedures
            self.__class_system__ = list()
            if len(classification_system) == 0:
                raise ValueError("At least one classification system must be given")
            for i, class_sys in enumerate(classification_system):
                try:
                    class_mod = modifications[i]
                except IndexError:
                    class_mod = None
                except TypeError:
                    class_mod = None
                self.__class_system__.append(
                    TaxonomicCoverage.ClassificationSystem(class_sys, modifications=class_mod)
                )
            self.__id_ref__ = list()
            if identification_reference is not None:
                self.__id_ref__.extend(identification_reference)
            self.__id_name__ = list()
            if len(identifier_name) == 0:
                raise ValueError("At least one identifier name must be given")
            self.__id_name__ = identifier_name
            self.__completeness__ = completeness
            self.__vouchers__ = list()
            if vouchers is not None:
                for specimen, repository in vouchers:
                    self.__vouchers__.append(
                        TaxonomicCoverage.Voucher(specimen, repository)
                    )
            return

        @property
        def procedures(self) -> str:
            """str: Description of the methods used for the taxonomic identification."""
            return self.__procedures__

        @property
        def classification_system(self) -> List[TaxonomicCoverage.ClassificationSystem]:
            """List[ClassificationSystem]: Information about the classification system or authority used."""
            return self.__class_system__

        @property
        def identification_reference(self) -> List:
            """List[EMLCitation]: Information on any non-authoritative materials."""
            return self.__id_ref__

        @property
        def identifier_name(self) -> List[ResponsibleParty]:
            """
            List[ResponsibleParty]: Information about the individual(s) responsible for the identification(s).
            """
            return self.__id_name__

        @property
        def completeness(self) -> str:
            """
            str: Taxonomic completeness.
            """
            return self.__completeness__

        @property
        def vouchers(self) -> List[TaxonomicCoverage.Voucher]:
            """List[Voucher]: Information on the types of specimen and the repository."""
            return self.__vouchers__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> TaxonomicCoverage.TaxonomicSystem | None:
            """
            Generate a TaxonomicSystem instance from an XML element instance.

            Parameters
            ----------
            element : lxml.etree.Element
                XML element to parse.
            nmap : Dict
                Namespace.

            Returns
            -------
            TaxonomicSystem
                Instance with the same information as the XML element.
            """
            if element is None:
                return None
            procedures_elem = element.find("taxonomicProcedures", nmap)
            classification_system = list()
            modifications = list()
            from eml.resources import EMLCitation
            for class_sys in element.findall("classificationSystem", nmap):
                citation_elem = class_sys.find("classificationSystemCitation", nmap)
                classification_system.append(EMLCitation.parse(citation_elem, nmap))
                modification_elem = class_sys.find("classificationSystemModifications", nmap)
                if modification_elem is not None:
                    modifications.append(modification_elem.text)
                else:
                    modifications.append(None)
            identification_ref = list()
            for id_ref in element.findall("identificationReference", nmap):
                identification_ref.append(EMLCitation.parse(id_ref, nmap))
            identification_name = list()
            for id_name in element.findall("identifierName", nmap):
                identification_name.append(ResponsibleParty.parse(id_name, nmap))
            completeness = None
            completeness_elem = element.find("taxonomicCompleteness", nmap)
            if completeness_elem is not None:
                completeness = completeness_elem.text if completeness_elem.text is not None else ""
            vouchers = list()
            for voucher_elem in element.findall("vouchers", nmap):
                specimen = voucher_elem.find("specimen", nmap)
                originator = list()
                for ori_elem in voucher_elem.find("repository", nmap).findall("originator", nmap):
                    originator.append(ResponsibleParty.parse(ori_elem, nmap))
                vouchers.append((
                    specimen.text if specimen.text is not None else "",
                    originator
                ))
            taxonomic_system = TaxonomicCoverage.TaxonomicSystem(
                procedures=procedures_elem.text if procedures_elem.text is not None else "",
                classification_system=classification_system,
                identification_reference=identification_ref,
                identifier_name=identification_name,
                completeness=completeness,
                vouchers=vouchers,
                modifications=modifications,
            )
            taxonomic_system.__namespace__ = nmap
            return taxonomic_system

        def to_element(self) -> et.Element:
            """
            Generate an XML instance using this object.

            Returns
            -------
            lxml.etree.Element
                XML element instance.
            """
            element = super().to_element()
            for class_sys in self.classification_system:
                class_elem = self.object_to_element("classificationSystem")
                cite_elem = class_sys.citation.to_element()
                cite_elem.tag = "classificationSystemCitation"
                class_elem.append(cite_elem)
                if class_sys.modifications is not None:
                    mod_elem = self.object_to_element("classificationSystemModifications")
                    mod_elem.text = class_sys.modifications
                    class_elem.append(mod_elem)
                element.append(class_elem)
            for id_ref in self.identification_reference:
                id_elem = id_ref.to_element()
                id_elem.tag = "identificationReference"
                element.append(id_elem)
            for id_name in self.identifier_name:
                id_name.set_tag("identifierName")
                element.append(id_name.to_element())
            procedures_elem = self.object_to_element("taxonomicProcedures")
            procedures_elem.text = self.procedures
            element.append(procedures_elem)
            if self.completeness:
                completeness_elem = self.object_to_element("taxonomicCompleteness")
                completeness_elem.text = self.completeness
                element.append(completeness_elem)
            for voucher in self.vouchers:
                voucher_elem = self.object_to_element("vouchers")
                specimen_elem = self.object_to_element("specimen")
                specimen_elem.text = voucher.specimen
                voucher_elem.append(specimen_elem)
                repository_elem = self.object_to_element("repository")
                for originator in voucher.repository:
                    originator.set_tag("originator")
                    repository_elem.append(originator.to_element())
                voucher_elem.append(repository_elem)
                element.append(voucher_elem)
            return element

    class TaxonomicClassification(XMLObject):
        """
        Information about the range of taxa addressed in the data set or collection.

        Parameters
        ----------
        _id : str, optional
            A unique identifier for this additional metadata that can be used to reference it elsewhere.
        rank_name : str, optional
            The name of the taxonomic rank for which the Taxon rank value is provided.
        rank_value : str, optional
            The taxonomic rank name being described.
        common_name: List[str], optional
            Specification of applicable common names.
        taxon_id: List[Tuple[int, str]], optional
            Element holds an ID and ID-provider for this taxon.
        classification: List[TaxonClassification], optional
            Taxonomic Classification field is self-referencing to allow for an arbitrary depth of rank, down to species.
        """
        PRINCIPAL_TAG = "taxonomicClassification"

        def __init__(
                self, _id: str = None,
                rank_name: str = None,
                rank_value: str = None,
                common_name: List[str] = None,
                taxon_id: List[Tuple[int, str]] = None,
                classification: List[TaxonomicCoverage.TaxonomicClassification] = None,
        ) -> None:
            super().__init__()
            self.__id__ = _id
            self.__name__ = rank_name
            self.__value__ = rank_value
            self.__common__ = list()
            if common_name is not None:
                self.__common__.extend(common_name)
            self.__id_taxon__ = list()
            if taxon_id is not None:
                for t_id, provider in taxon_id:
                    self.__id_taxon__.append(
                        TaxonomicCoverage.TaxonID(t_id, provider)
                    )
            self.__classification__ = list()
            if classification is not None:
                self.__classification__.extend(classification)
            return

        @property
        def id(self) -> str:
            """str: A unique identifier for this additional metadata that can be used to reference it elsewhere."""
            return self.__id__

        @property
        def rank_name(self) -> str:
            """str: The name of the taxonomic rank for which the Taxon rank value is provided."""
            return self.__name__

        @property
        def rank_value(self) -> str:
            """str: The taxonomic rank name being described."""
            return self.__value__

        @property
        def common_name(self) -> List[str]:
            """List[str]: Specification of applicable common names."""
            return self.__common__

        @property
        def taxon_id(self) -> List[TaxonomicCoverage.TaxonID]:
            """List[TaxonID]: Element holds an ID and ID-provider for this taxon."""
            return self.__id_taxon__

        @property
        def classification(self) -> List[TaxonomicCoverage.TaxonomicClassification]:
            """List[TaxonomicClassification]: Taxonomic Classification field self-referenced."""
            return self.__classification__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> TaxonomicCoverage.TaxonomicClassification | None:
            """
            Generate a TaxonomicClassification instance from an XML element.

            Parameters
            ----------
            element : lxml.etree.Element
                XML Element to be parsed.
            nmap : Dict
                Namespace

            Returns
            -------
            TaxonomicClassification
                An instance with the XML element information.
            """
            if element is None:
                return None
            rank_name = None
            name_elem = element.find("taxonRankName", nmap)
            if name_elem is not None:
                rank_name = name_elem.text if name_elem.text is not None else ""
            rank_value = None
            value_elem = element.find("taxonRankValue", nmap)
            if value_elem is not None:
                rank_value = value_elem.text if value_elem.text is not None else ""
            common_names = list()
            for common_elem in element.findall("commonName", nmap):
                common_names.append(common_elem.text if common_elem.text is not None else "")
            taxon_id = list()
            for taxon_elem in element.findall("taxonId", nmap):
                taxon_id.append((
                    int(taxon_elem.text), taxon_elem.get("provider")
                ))
            classifications = list()
            for classification_elem in element.findall("taxonomicClassification"):
                classifications.append(TaxonomicCoverage.TaxonomicClassification.parse(classification_elem, nmap))
            return TaxonomicCoverage.TaxonomicClassification(
                _id=element.get("id", None),
                rank_name=rank_name,
                rank_value=rank_value,
                common_name=common_names,
                taxon_id=taxon_id,
                classification=classifications
            )

        def to_element(self) -> et.Element:
            """
            Generate an XML element instance with the information of this object.

            Returns
            -------
            lxml.etree.Element
                XML element instance.
            """
            element = super().to_element()
            if self.id is not None:
                element.set("id", self.id)
            if self.rank_name is not None:
                name_elem = self.object_to_element("taxonRankName")
                name_elem.text = self.rank_name
                element.append(name_elem)
            if self.rank_value is not None:
                value_elem = self.object_to_element("taxonRankValue")
                value_elem.text = self.rank_value
                element.append(value_elem)
            for common_name in self.common_name:
                common_elem = self.object_to_element("commonName")
                common_elem.text = common_name
                element.append(common_elem)
            for taxon_id in self.taxon_id:
                taxon_elem = self.object_to_element("taxonId")
                taxon_elem.text = str(taxon_id.id)
                taxon_elem.set("provider", taxon_id.provider)
                element.append(taxon_elem)
            for classification in self.classification:
                element.append(classification.to_element())
            return element

    PRINCIPAL_TAG = "taxonomicCoverage"

    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            taxonomic_system: TaxonomicCoverage.TaxonomicSystem = None,
            general_coverage: str = None,
            classification: List[TaxonomicCoverage.TaxonomicClassification] = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__taxa_system__ = taxonomic_system
        self.__general__ = general_coverage
        self.__classification__ = list()
        if self.referencing:
            return
        if classification is None or len(classification) == 0:
            raise ValueError("At least one taxonomic classification must be given")
        self.__classification__.extend(classification)
        return

    @property
    def taxonomic_system(self) -> TaxonomicCoverage.TaxonomicSystem:
        """TaxonomicSystem: Documentation of taxonomic sources, procedures, and treatments."""
        return self.__taxa_system__

    @property
    def general_coverage(self) -> str:
        """str: A description of the range of taxa addressed in the data set or collection."""
        return self.__general__

    @property
    def classification(self) -> List[TaxonomicCoverage.TaxonomicClassification]:
        """TaxonomicClassification: Information about the range of taxa addressed in the data set or collection."""
        return self.__classification__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLObject:
        """
        Generate a Taxonomic Coverage referencing another Taxonomic Coverage.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        TaxonomicCoverage
            Taxonomic Coverage object parsed that reference another.
        """
        references = element.find("references", nmap)
        return TaxonomicCoverage(
            _id=references.text if references.text is not None else "",
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> TaxonomicCoverage:
        """
        Generate a Taxonomic Coverage instance that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        TaxonomicCoverage
            Object parsed.
        """
        taxon_system = None
        taxon_system_elem = element.find("taxonomicSystem", nmap)
        if taxon_system_elem is not None:
            taxon_system = TaxonomicCoverage.TaxonomicSystem.parse(taxon_system_elem, nmap)
        general_coverage = None
        general_coverage_elem = element.find("generalTaxonomicCoverage", nmap)
        if general_coverage_elem is not None:
            general_coverage = general_coverage_elem.text if general_coverage_elem.text is not None else ""
        classification = list()
        for taxon_class in element.findall("taxonomicClassification", nmap):
            classification.append(
                TaxonomicCoverage.TaxonomicClassification.parse(
                    taxon_class, nmap
                )
            )
        return TaxonomicCoverage(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            taxonomic_system=taxon_system,
            general_coverage=general_coverage,
            classification=classification,
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance using object information.

        Returns
        -------
        lxml.etree.Element
            XML element instance.
        """
        element = super().to_element()
        element = self._to_element_(element)
        if self.referencing:
            return element
        if self.taxonomic_system is not None:
            element.append(self.taxonomic_system.to_element())
        if self.general_coverage is not None:
            general_elem = self.object_to_element("generalTaxonomicCoverage")
            general_elem.text = self.general_coverage
            element.append(general_elem)
        for classification in self.classification:
            element.append(classification.to_element())
        return element
