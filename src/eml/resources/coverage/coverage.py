from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources.coverage import GeographicCoverage, TemporalCoverage, TaxonomicCoverage
from eml.types import EMLObject, Scope


class EMLCoverage(EMLObject):
    """
    Extent of the coverage of the resource.

    Parameters
    ----------
    geographic: GeographicCoverage
        Geographic coverage information.
    temporal: TemporalCoverage
        Temporal coverage information.
    taxonomic: TaxonomicCoverage
        Taxonomic coverage information.
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
    """
    PRINCIPAL_TAG = "coverage"

    def __init__(
            self,
            geographic: GeographicCoverage = None,
            temporal: TemporalCoverage = None,
            taxonomic: TaxonomicCoverage = None,
            _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        if self.referencing:
            return
        if (
            geographic is None and
            temporal is None and
            taxonomic is None
        ):
            raise TypeError("EMLCoverage() required at least one of geographic, temporal and taxonomic coverages")
        self.__geo__ = geographic
        self.__time__ = temporal
        self.__taxa__ = taxonomic
        return

    @property
    def geographic(self) -> GeographicCoverage:
        """GeographicCoverage: Geographic coverage information."""
        return self.__geo__

    @property
    def temporal(self) -> TemporalCoverage:
        """TemporalCoverage: Temporal coverage information."""
        return self.__time__

    @property
    def taxonomic(self) -> TaxonomicCoverage:
        """TaxonomicCoverage: Taxonomic coverage information."""
        return self.__taxa__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLCoverage:
        """
        Generate an EML Coverage referencing another EML Coverage.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLCoverage
            Object parsed that reference another.
        """
        references = element.find("references", nmap)
        return EMLCoverage(
            _id=references.text if references.text is not None else "",
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None),
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLCoverage:
        """
        Generate an EML Coverage that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLCoverage
            Object parsed.
        """
        return EMLCoverage(
            geographic=GeographicCoverage.parse(element.find("geographicCoverage", nmap), nmap),
            temporal=TemporalCoverage.parse(element.find("temporalCoverage", nmap), nmap),
            taxonomic=TaxonomicCoverage.parse(element.find("taxonomicCoverage", nmap), nmap),
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance.

        Returns
        -------
        lxml.etree.Element
            XML element instance.
        """
        element = super().to_element()
        element = self._to_element_(element)
        if not self.referencing:
            element.append(self.geographic.to_element()) if self.geographic is not None else None
            element.append(self.temporal.to_element()) if self.temporal is not None else None
            element.append(self.taxonomic.to_element()) if self.taxonomic is not None else None
        return element
