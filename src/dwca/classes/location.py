from typing import List, Union

from dwca.classes import DataFile
from dwca.terms import LocationID, HigherGeographyID, HigherGeography, Continent, WaterBody, IslandGroup, Island, \
    Country, CountryCode, StateProvince, County, Municipality, DWCLocalityTerm, VerbatimLocality, \
    MinimumElevationInMeters, MaximumElevationInMeters, VerbatimElevation, VerticalDatum, MinimumDepthInMeters, \
    MaximumDepthInMeters, VerbatimDepth, MinimumDistanceAboveSurfaceInMeters, MaximumDistanceAboveSurfaceInMeters, \
    LocationAccordingTo, LocationRemarks, DecimalLatitude, DecimalLongitude, GeodeticDatum, \
    CoordinateUncertaintyInMeters, CoordinatePrecision, PointRadiusSpatialFit, VerbatimCoordinates, VerbatimLatitude, \
    VerbatimLongitude, VerbatimCoordinateSystem, VerbatimSRS, FootprintWKT, FootprintSRS, FootprintSpatialFit, \
    GeoreferencedBy, GeoreferencedDate, GeoreferenceProtocol, GeoreferenceSources, GeoreferenceRemarks, Field


class Location(DataFile):
    """
    A spatial region or named place.

    Parameters
    ----------
    _id : int
        Unique identifier for the core entity.
    files : str
        File location, in the archive, this is inside the `zip` file.
    fields : List[Field]
        A list of the Field (columns) in the Core data entity.
    encoding : str, optional
        Encoding of the file location (`files` parameter), default is "utf-8".
    lines_terminated_by : str, optional
        Delimiter of lines on the file, default `"\\\\n"`.
    fields_terminated_by : str, optional
        Delimiter of the file (cells) on the file, default `","`.
    fields_enclosed_by : str, optional
        Specifies the character used to enclose (mark the start and end of) each field, default empty `""`.
    ignore_header_lines : List[int|str] | int | str, optional
        Ignore headers at the start of document, can be one line or a list of them, default 0 (first line).
    """
    URI = "http://purl.org/dc/terms/Location"
    __field_class__ = DataFile.__field_class__ + [
        LocationID, HigherGeographyID, HigherGeography,
        Continent, WaterBody, IslandGroup, Island, Country,
        CountryCode, StateProvince, County, Municipality,
        DWCLocalityTerm, VerbatimLocality, MinimumElevationInMeters,
        MaximumElevationInMeters, VerbatimElevation, VerticalDatum,
        MinimumDepthInMeters, MaximumDepthInMeters, VerbatimDepth,
        MinimumDistanceAboveSurfaceInMeters, MaximumDistanceAboveSurfaceInMeters,
        LocationAccordingTo, LocationRemarks, DecimalLatitude,
        DecimalLongitude, GeodeticDatum, CoordinateUncertaintyInMeters,
        CoordinatePrecision, PointRadiusSpatialFit, VerbatimCoordinates,
        VerbatimLatitude, VerbatimLongitude, VerbatimCoordinateSystem,
        VerbatimSRS, FootprintWKT, FootprintSRS, FootprintSpatialFit,
        GeoreferencedBy, GeoreferencedDate, GeoreferenceProtocol,
        GeoreferenceSources, GeoreferenceRemarks
    ]

    def __init__(
            self, _id: int, files: str,
            fields: List[Field],
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: Union[List[Union[int, str]], int, str] = 0,
            _principal_tag: str = "core"
    ) -> None:
        super().__init__(
            _id, files, fields, encoding, lines_terminated_by,
            fields_terminated_by, fields_enclosed_by,
            ignore_header_lines, _principal_tag
        )
        return
