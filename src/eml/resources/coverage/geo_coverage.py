from __future__ import annotations

import re
from typing import Dict, Tuple, List

from lxml import etree as et

from dwca.utils import LengthUnit, GPolygon, GRing
from eml.types import EMLObject, Scope


class GeographicCoverage(EMLObject):
    """
    Geographic coverage information.

    Parameters
    ----------
    description : str
        Short text description of the geographic areal domain of the data set.
    west_bounding : float
        Western-most limit of a bounding box, expressed in degrees of longitude.
    east_bounding : float
        Eastern-most limit of a bounding box, expressed in degrees of longitude.
    north_bounding : float
        Northern-most limit of a bounding box, expressed in degrees of latitude.
    south_bounding : float
        Southern-most limit of a bounding box, expressed in degrees of latitude.
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
    altitude_bounding : Tuple[float, float], optional
        The vertical limits of a data set expressed by altitude.
    altitude_units : LengthUnit, optional
        The unit of altitude.
    g_polygon : List[Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]], optional
        This construct creates a spatial ring with a hollow center.
    """
    PRINCIPAL_TAG = "geographicCoverage"

    def __init__(
            self,
            description: str,
            west_bounding: float,
            east_bounding: float,
            north_bounding: float,
            south_bounding: float,
            _id: str = None,
            scope: Scope = None,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            altitude_bounding: Tuple[float, float] = None,
            altitude_units: LengthUnit = None,
            g_polygon: List[GPolygon] = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__description__ = description
        self.__w__ = west_bounding
        self.__e__ = east_bounding
        self.__n__ = north_bounding
        self.__s__ = south_bounding
        if altitude_bounding is not None:
            self.__max_alt__ = altitude_bounding[0]
            self.__min_alt__ = altitude_bounding[1]
        else:
            self.__max_alt__, self.__min_alt__ = None, None
        if altitude_units is not None:
            self.__alt_units__ = altitude_units
        else:
            self.__alt_units__ = None
        self.__polygons__ = list()
        if g_polygon is not None:
            self.__polygons__.extend(g_polygon)
        return

    @property
    def description(self) -> str:
        """str: Short text description of the geographic areal domain of the data set."""
        return self.__description__

    @property
    def west_bounding(self) -> float:
        """float: Western-most limit of a bounding box, expressed in degrees of longitude."""
        return self.__w__

    @property
    def east_bounding(self) -> float:
        """float: Eastern-most limit of a bounding box, expressed in degrees of longitude."""
        return self.__e__

    @property
    def north_bounding(self) -> float:
        """float: Northern-most limit of a bounding box, expressed in degrees of latitude."""
        return self.__n__

    @property
    def south_bounding(self) -> float:
        """float: Southern-most limit of a bounding box, expressed in degrees of latitude."""
        return self.__s__

    @property
    def max_altitude_bounding(self) -> float:
        """float: The maximum altitude extent of coverage."""
        return self.__max_alt__

    @property
    def min_altitude_bounding(self) -> float:
        """float: The minimum altitude extent of coverage."""
        return self.__min_alt__

    @property
    def altitude_units_bounding(self) -> LengthUnit:
        """LengthUnit: The unit of altitude."""
        return self.__alt_units__

    @property
    def g_polygon(self) -> List[GPolygon]:
        """List[GPolygon]: This construct creates a spatial ring with a hollow center."""
        return self.__polygons__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> GeographicCoverage:
        """
        Generate an GeographicCoverage referencing another GeographicCoverage.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        GeographicCoverage
            Object parsed that reference another.
        """
        references = element.find("references", nmap)
        return GeographicCoverage(
            description="",
            west_bounding=float("nan"),
            east_bounding=float("nan"),
            north_bounding=float("nan"),
            south_bounding=float("nan"),
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None),
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> GeographicCoverage:
        """
        Generate a GeographicCoverage that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        GeographicCoverage
            Object parsed.
        """
        description_elem = element.find("geographicDescription", nmap)
        bounding_elem = element.find("boundingCoordinates", nmap)
        west_bounding_elem = bounding_elem.find("westBoundingCoordinate", nmap)
        west = float(west_bounding_elem.text)
        east_bounding_elem = bounding_elem.find("eastBoundingCoordinate", nmap)
        east = float(east_bounding_elem.text)
        north_bounding_elem = bounding_elem.find("northBoundingCoordinate", nmap)
        north = float(north_bounding_elem.text)
        south_bounding_elem = bounding_elem.find("southBoundingCoordinate", nmap)
        south = float(south_bounding_elem.text)
        alt_bounding_elem = bounding_elem.find("boundingAltitudes", nmap)
        if alt_bounding_elem is not None:
            min_alt_elem = alt_bounding_elem.find("altitudeMinimum", nmap)
            max_alt_elem = alt_bounding_elem.find("altitudeMaximum", nmap)
            altitude_bounding = float(max_alt_elem.text), float(min_alt_elem.text)
            unit_elem = alt_bounding_elem.find("altitudeUnits", nmap)
            unit = LengthUnit.METER
            if unit_elem is not None:
                for candid_unit in LengthUnit:
                    if candid_unit.name.lower() == unit_elem.text.lower():
                        unit = candid_unit
                        break
        else:
            altitude_bounding = None
            unit = None
        polygons = list()
        for polygon_elem in element.findall("datasetGPolygon", nmap):
            polygons.append(cls.xml_to_polygon(polygon_elem, nmap))
        return GeographicCoverage(
            description=description_elem.text if description_elem.text is not None else None,
            west_bounding=west,
            east_bounding=east,
            north_bounding=north,
            south_bounding=south,
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            altitude_bounding=altitude_bounding,
            altitude_units=unit,
            g_polygon=polygons
        )

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the object.

        Returns
        -------
        lxml.tree.Element
            Geographic Coverage in the Element format.
        """
        geo_element = super().to_element()
        geo_element = self._to_element_(geo_element)
        if not self.referencing:
            desc_elem = self.object_to_element("geographicDescription")
            desc_elem.text = self.description
            geo_element.append(desc_elem)
            if (
                self.west_bounding is not None and
                self.east_bounding is not None and
                self.north_bounding is not None and
                self.south_bounding
            ):
                bounding_elem = self.object_to_element("boundingCoordinates")
                west_elem = self.object_to_element("westBoundingCoordinate")
                west_elem.text = str(self.west_bounding)
                bounding_elem.append(west_elem)
                east_elem = self.object_to_element("eastBoundingCoordinate")
                east_elem.text = str(self.east_bounding)
                bounding_elem.append(east_elem)
                north_elem = self.object_to_element("northBoundingCoordinate")
                north_elem.text = str(self.north_bounding)
                bounding_elem.append(north_elem)
                south_elem = self.object_to_element("southBoundingCoordinate")
                south_elem.text = str(self.south_bounding)
                bounding_elem.append(south_elem)
                if (
                    self.max_altitude_bounding is not None and
                    self.min_altitude_bounding is not None and
                    self.altitude_units_bounding is not None
                ):
                    alt_elem = self.object_to_element("boundingAltitudes")
                    min_alt = self.object_to_element("altitudeMinimum")
                    min_alt.text = str(self.min_altitude_bounding)
                    alt_elem.append(min_alt)
                    max_alt = self.object_to_element("altitudeMaximum")
                    max_alt.text = str(self.max_altitude_bounding)
                    alt_elem.append(max_alt)
                    unit_alt = self.object_to_element("altitudeUnits")
                    unit_alt.text = self.altitude_units_bounding.valid_name
                    alt_elem.append(unit_alt)
                    bounding_elem.append(alt_elem)
                geo_element.append(bounding_elem)
            for polygon in self.g_polygon:
                polygon_elem = self.polygon_to_xml(polygon)
                geo_element.append(polygon_elem)
        return geo_element

    @staticmethod
    def xml_to_polygon(element: et.Element, nmap: Dict) -> GPolygon:
        """
        Convert a lxml.tree.Element into a GPolygon object.

        Parameters
        ----------
        element : lxml.tree.Element
            XML element to be parsed into geographical coordinates
        nmap : Dict
            Namespace.

        Returns
        -------
        GPolygon
            A valid polygon.
        """
        outer_elem = element.find("datasetGPolygonOuterGRing")
        outer = GeographicCoverage.xml_to_ring(outer_elem, nmap)
        exclusion = list()
        for excl_elem in element.findall("datasetGPolygonExclusionGRing", nmap):
            exclusion.append(GeographicCoverage.xml_to_ring(excl_elem, nmap))
        return GPolygon(outer, exclusion=exclusion)

    @staticmethod
    def polygon_to_xml(polygon: GPolygon) -> et.Element:
        """
        Convert a GPolygon object into an XML Element.

        Parameters
        ----------
        polygon : GPolygon
            A valid GPolygon object.

        Returns
        -------
        lxml.tree.Element
            XML element with the GPolygon information.
        """
        element = et.Element("datasetGPolygon")
        outer_elem = et.Element("datasetGPolygonOuterGRing")
        outer_elem.append(GeographicCoverage.ring_to_xml(polygon.outer))
        element.append(outer_elem)
        for excl in polygon.exclusion:
            excl_elem = et.Element("datasetGPolygonExclusionGRing")
            excl_elem.append(GeographicCoverage.ring_to_xml(excl))
            element.append(excl_elem)
        return element

    @staticmethod
    def xml_to_ring(element: et.Element, nmap: Dict) -> GRing:
        """
        Convert a lxml.tree.Element into a GRing object.

        Parameters
        ----------
        element : lxml.tree.Element
            XML element to be parsed into geographical coordinates.
        nmap : Dict
            Namespace.

        Returns
        -------
        GRing
            A valid ring.
        """
        g_ring = element.find("gRing", nmap)
        g_ring_points = element.findall("gRingPoint", nmap)
        points = list()
        if g_ring is not None:
            for point in re.split(r'(?<!,)\s', g_ring.text):
                lat, long = point.split(",")
                points.append((float(lat.strip()), float(long.strip())))
        elif len(g_ring_points) > 0:
            for point in g_ring_points:
                lat = float(point.find("gRingLatitude", nmap).text)
                long = float(point.find("gRingLongitude", nmap).text)
                points.append((lat, long))
        return GRing(*points)

    @staticmethod
    def ring_to_xml(ring: GRing) -> et.Element:
        """
        Convert a GRing object into an XML Element.

        Parameters
        ----------
        ring : GRing
            A valid GRing object.

        Returns
        -------
        lxml.tree.Element
            XML element with the GPolygon information.
        """
        element = et.Element("gRing")
        element.text = " ".join(
            [f"{lat}, {long}" for lat, long in ring]
        )
        return element
