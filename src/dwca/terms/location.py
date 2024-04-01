import datetime as dt
from typing import List, Union

from datetime_interval import Interval

from dwca.terms import Field


class LocationID(Field):
    """
    An identifier for the set of Location information.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/locationID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class HigherGeographyID(Field):
    """
    An identifier for the geographic region within which the Location occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/higherGeographyID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class HigherGeography(Field):
    """
    A list of geographic names less specific than the information captured in the locality term.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/higherGeography"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Continent(Field):
    """
    The name of the continent in which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/continent"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class WaterBody(Field):
    """
    The name of the water body in which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/waterBody"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IslandGroup(Field):
    """
    The name of the island group in which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/islandGroup"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Island(Field):
    """
    The name of the island on or near which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/island"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Country(Field):
    """
    The name of the country or major administrative unit in which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/country"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class CountryCode(Field):
    """
    The standard code for the country in which the Location occurs.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/countryCode"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class StateProvince(Field):
    """
    The name of the next smaller administrative region than country in which the Location occurs.

    Smaller administrative region such as state, province, canton, department, region, etc.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/stateProvince"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class County(Field):
    """
    The full name of the next smaller administrative region than stateProvince in which the Location occurs.

    Such as state, province, canton, department, region, etc.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/county"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Municipality(Field):
    """
    The full name of the next smaller administrative region than county in which the Location occurs.

    Such as city, municipality, etc. Do not use this term for a nearby named place that does not
    contain the actual Location.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/municipality"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCLocalityTerm(Field):
    """
    The specific description of the place.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/locality"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimLocality(Field):
    """
    The original textual description of the place.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimLocality"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MinimumElevationInMeters(Field):
    """
    The lower limit of the range of elevation (altitude, usually above sea level), in meters.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/minimumElevationInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaximumElevationInMeters(Field):
    """
    The upper limit of the range of elevation (altitude, usually above sea level), in meters.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/maximumElevationInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimElevation(Field):
    """
    The original description of the elevation (altitude, usually above sea level) of the Location.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimElevation"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerticalDatum(Field):
    """
    The vertical datum used as the reference upon which the values in the elevation terms are based.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verticalDatum"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MinimumDepthInMeters(Field):
    """
    The lesser depth of a range of depth below the local surface, in meters.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/minimumDepthInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaximumDepthInMeters(Field):
    """
    The greater depth of a range of depth below the local surface, in meters.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/maximumDepthInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimDepth(Field):
    """
    The original description of the depth below the local surface.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimDepth"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MinimumDistanceAboveSurfaceInMeters(Field):
    """
    The lesser distance in a range of distance from a reference surface in the vertical direction, in meters.

    Use positive values for locations above the surface, negative values for locations below.
    If depth measures are given, the reference surface is the location given by the depth,
    otherwise the reference surface is the location given by the elevation.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/minimumDistanceAboveSurfaceInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaximumDistanceAboveSurfaceInMeters(Field):
    """
    The greater distance in a range of distance from a reference surface in the vertical direction, in meters.

    Use positive values for locations above the surface, negative values for
    locations below. If depth measures are given, the reference surface is
    the location given by the depth, otherwise the reference surface is
    the location given by the elevation.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/maximumDistanceAboveSurfaceInMeters"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LocationAccordingTo(Field):
    """
    Information about the source of this Location information.

    Could be a publication (gazetteer), institution, or team of individuals.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/locationAccordingTo"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LocationRemarks(Field):
    """
    Comments or notes about the Location.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/locationRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DecimalLatitude(Field):
    """
    The geographic latitude of the geographic center of a Location.

    Latitude in decimal degrees, using the spatial reference system
    given in geodeticDatum. Positive values are north of the Equator,
    negative values are south of it. Legal values lie between -90
    and 90, inclusive.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/decimalLatitude"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DecimalLongitude(Field):
    """
    The geographic longitude of the geographic center of a Location.

    Longitude in decimal degrees, using the spatial reference system
    given in geodeticDatum. Positive values are east of the Greenwich
    Meridian, negative values are west of it. Legal values lie between
    -180 and 180, inclusive.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/decimalLongitude"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeodeticDatum(Field):
    """
    The geodetic datum upon which the geographic coordinates given in decimalLatitude and decimalLongitude are based.

    Ellipsoid, geodetic datum, or spatial reference system (SRS).
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/geodeticDatum"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class CoordinateUncertaintyInMeters(Field):
    """
    The horizontal distance describing the smallest circle containing the whole of the Location.

    Horizontal distance in meters from the given latitude and
    longitude. Leave the value empty if the uncertainty is
    unknown, cannot be estimated, or is not applicable (because
    there are no coordinates). Zero is not a valid value for
    this term.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/coordinateUncertaintyInMeters"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class CoordinatePrecision(Field):
    """
    A decimal representation of the precision of the coordinates given in the latitude and longitude.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/coordinatePrecision"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class PointRadiusSpatialFit(Field):
    """
    The ratio of the area of the point-radius to the area of the spatial representation of the Location.

    Point-radius described by: {decimalLatitude, decimalLongitude, coordinateUncertaintyInMeters}
    Legal values are 0, greater than or equal to 1, or undefined. A value of
    1 is an exact match or 100% overlap. A value of 0 should be used if the
    given point-radius does not completely contain the original representation.
    The pointRadiusSpatialFit is undefined (and should be left empty) if the original
    representation is any geometry without area (e.g., a point or polyline) and
    without uncertainty and the given georeference is not that same geometry
    (without uncertainty). If both the original and the given georeference are the
    same point, the pointRadiusSpatialFit is 1.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/pointRadiusSpatialFit"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimCoordinates(Field):
    """
    The verbatim original spatial coordinates of the Location.

    The coordinate ellipsoid, geodeticDatum, or full Spatial Reference
    System (SRS) for these coordinates should be stored in verbatimSRS
    and the coordinate system should be stored in verbatimCoordinateSystem.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimCoordinates"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimLatitude(Field):
    """
    The verbatim original latitude of the Location.

    The coordinate ellipsoid, geodeticDatum, or full Spatial Reference
    System (SRS) for these coordinates should be stored in verbatimSRS
    and the coordinate system should be stored in verbatimCoordinateSystem.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimLatitude"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimLongitude(Field):
    """
    The verbatim original longitude of the Location.

    The coordinate ellipsoid, geodeticDatum, or full Spatial Reference
    System (SRS) for these coordinates should be stored in verbatimSRS
    and the coordinate system should be stored in verbatimCoordinateSystem.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimLongitude"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimCoordinateSystem(Field):
    """
    The coordinate format for the verbatimLatitude and verbatimLongitude or the verbatimCoordinates of the Location.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimCoordinateSystem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimSRS(Field):
    """
    The geodetic datum upon which coordinates given in (Verbatim) Latitude and Longitude, or Coordinates are based.

    The ellipsoid, geodetic datum, or spatial reference system (SRS)
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimSRS"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class FootprintWKT(Field):
    """
    A Well-Known Text (WKT) representation of the shape (footprint, geometry) that defines the Location.

    A Location may have both a point-radius representation (see :class:`DecimalLatitude`)
    and a footprint representation, and they may differ from each other.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/footprintWKT"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class FootprintSRS(Field):
    """
    The geodetic datum upon which the geometry given in footprintWKT is based.

    The ellipsoid, geodetic datum, or spatial reference system (SRS)
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/footprintSRS"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class FootprintSpatialFit(Field):
    """
    The ratio of the area of the footprintWKT to the area of the spatial representation of the Location.

    Legal values are 0, greater than or equal to 1, or undefined.
    A value of 1 is an exact match or 100% overlap. A value of 0
    should be used if the given footprintWKT does not completely
    contain the original representation. The footprintSpatialFit
    is undefined (and should be left empty) if the original
    representation is any geometry without area (e.g., a point or
    polyline) and without uncertainty and the given georeference is
    ot that same geometry (without uncertainty). If both the
    original and the given georeference are the same point,
    the footprintSpatialFit is 1.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/footprintSpatialFit"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeoreferencedBy(Field):
    """
    A list of names of people, groups, or organizations who determined the georeference for the Location.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferencedBy"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeoreferencedDate(Field):
    """
    The date on which the Location was georeferenced.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferencedDate"
    TYPE = Union[dt.datetime, Interval]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeoreferenceProtocol(Field):
    """
    A description or reference to the methods used to determine the spatial footprint, coordinates, and uncertainties.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferenceProtocol"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeoreferenceSources(Field):
    """
    A list of maps, gazetteers, or other resources used to georeference the Location.

    Described specifically enough to allow anyone in the
    future to use the same resources.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferenceSources"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GeoreferenceRemarks(Field):
    """
    Notes or comments about the spatial description determination.

    Explaining assumptions made in addition or opposition
    to the those formalized in the method referred to in
    georeferenceProtocol.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferenceRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
