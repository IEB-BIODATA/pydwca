import math
import unittest

from lxml import etree as et

from dwca.utils import LengthUnit, GPolygon, GRing
from eml.resources.coverage import GeographicCoverage
from test_xml.test_xml import TestXML


class TestGeoCoverage(TestXML):
    def test_parse(self):
        text_xml = """
<geographicCoverage id="" scope="document" system="">
    <geographicDescription>Manistee River watershed</geographicDescription>
    <boundingCoordinates>
        <westBoundingCoordinate>-118.25</westBoundingCoordinate>
        <eastBoundingCoordinate>-118.25</eastBoundingCoordinate>
        <northBoundingCoordinate>-18.25</northBoundingCoordinate>
        <southBoundingCoordinate>-118.25</southBoundingCoordinate>
        <boundingAltitudes>
            <altitudeMinimum>-10</altitudeMinimum>
            <altitudeMaximum>100.6</altitudeMaximum>
            <altitudeUnits>Yard_Indian</altitudeUnits>
        </boundingAltitudes>
    </boundingCoordinates>
    <datasetGPolygon>
        <datasetGPolygonOuterGRing>
            <gRing>12, 2.0987 12, -7.5555 34.345,10.40</gRing>
        </datasetGPolygonOuterGRing>
    </datasetGPolygon>
</geographicCoverage>
        """
        geo_coverage = GeographicCoverage.from_string(text_xml)
        self.assertEqual(
            "Manistee River watershed",
            geo_coverage.description,
            "Geographic description error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.west_bounding,
            "West bounding error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.east_bounding,
            "East bounding error on parsing"
        )
        self.assertEqual(
            -18.25,
            geo_coverage.north_bounding,
            "North bounding error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.south_bounding,
            "South bounding error on parsing"
        )
        self.assertEqual(
            100.6,
            geo_coverage.max_altitude_bounding,
            "Altitude maximum bounding error on parsing"
        )
        self.assertEqual(
            -10,
            geo_coverage.min_altitude_bounding,
            "Altitude minimum bounding error on parsing"
        )
        self.assertEqual(
            LengthUnit.YARD_INDIAN,
            geo_coverage.altitude_units_bounding,
            "Altitude units bounding error on parsing"
        )
        self.assertEqual(
            [(12, 2.0987), (12, -7.5555), (34.345, 10.40)],
            geo_coverage.g_polygon[0].outer,
            "GPolygon Outer ring bounding error on parsing"
        )
        self.assertEqualTree(
            et.fromstring(text_xml),
            geo_coverage.to_element(),
            "Error on to element"
        )

    def test_parse_reference(self):
        text_xml = """
<geographicCoverage scope="system">
    <references system="http://gbif.org">1</references>
</geographicCoverage>
        """
        geo_coverage = GeographicCoverage.from_string(text_xml)
        self.assertEqual(
            "",
            geo_coverage.description,
            "Geographic description from nowhere"
        )
        self.assertTrue(
            math.isnan(geo_coverage.west_bounding),
            "West bounding from nowhere"
        )
        self.assertTrue(
            math.isnan(geo_coverage.east_bounding),
            "East bounding from nowhere"
        )
        self.assertTrue(
            math.isnan(geo_coverage.north_bounding),
            "North bounding from nowhere"
        )
        self.assertTrue(
            math.isnan(geo_coverage.south_bounding),
            "South bounding from nowhere"
        )
        self.assertIsNone(
            geo_coverage.max_altitude_bounding,
            "Altitude maximum bounding from nowhere"
        )
        self.assertIsNone(
            geo_coverage.min_altitude_bounding,
            "Altitude minimum bounding from nowhere"
        )
        self.assertIsNone(
            geo_coverage.altitude_units_bounding,
            "Altitude units bounding from nowhere"
        )
        self.assertEqual(
            0,
            len(geo_coverage.g_polygon),
            "GPolygon Outer ring bounding from nowhere"
        )
        self.assertTrue(
            geo_coverage.referencing,
            "Not referencing"
        )
        self.assertEqual(
            "1",
            geo_coverage.references,
            "Error on references"
        )
        self.assertEqual(
            "http://gbif.org",
            geo_coverage.references.system,
            "Error on references system"
        )
        self.assertEqual(
            "1",
            geo_coverage.id,
            "Error on id"
        )
        self.assertEqualTree(
            et.fromstring(text_xml),
            geo_coverage.to_element(),
            "Error on to element"
        )

    def test_parse_alternative(self):
        text_xml = """
<geographicCoverage id="" scope="document" system="">
    <geographicDescription>Manistee River watershed</geographicDescription>
    <boundingCoordinates>
        <westBoundingCoordinate>-118.25</westBoundingCoordinate>
        <eastBoundingCoordinate>-118.25</eastBoundingCoordinate>
        <northBoundingCoordinate>-18.25</northBoundingCoordinate>
        <southBoundingCoordinate>-118.25</southBoundingCoordinate>
    </boundingCoordinates>
    <datasetGPolygon>
        <datasetGPolygonOuterGRing>
            <gRingPoint>
                <gRingLatitude>34.123</gRingLatitude>
                <gRingLongitude>-118.25</gRingLongitude>
            </gRingPoint>
            <gRingPoint>
                <gRingLatitude>-18.25</gRingLatitude>
                <gRingLongitude>+25</gRingLongitude>
            </gRingPoint>
            <gRingPoint>
                <gRingLatitude>+78.25</gRingLatitude>
                <gRingLongitude>45.24755</gRingLongitude>
            </gRingPoint>
        </datasetGPolygonOuterGRing>
    </datasetGPolygon>
</geographicCoverage>
        """
        geo_coverage = GeographicCoverage.from_string(text_xml)
        self.assertEqual(
            "Manistee River watershed",
            geo_coverage.description,
            "Geographic description error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.west_bounding,
            "West bounding error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.east_bounding,
            "East bounding error on parsing"
        )
        self.assertEqual(
            -18.25,
            geo_coverage.north_bounding,
            "North bounding error on parsing"
        )
        self.assertEqual(
            -118.25,
            geo_coverage.south_bounding,
            "South bounding error on parsing"
        )
        self.assertIsNone(
            geo_coverage.max_altitude_bounding,
            "Altitude maximum bounding error on parsing"
        )
        self.assertIsNone(
            geo_coverage.min_altitude_bounding,
            "Altitude minimum bounding error on parsing"
        )
        self.assertIsNone(
            geo_coverage.altitude_units_bounding,
            "Altitude units bounding error on parsing"
        )
        self.assertEqual(
            [(34.123, -118.25), (-18.25, 25), (78.25, 45.24755)],
            geo_coverage.g_polygon[0].outer,
            "GPolygon Outer ring bounding error on parsing"
        )
        text_xml = text_xml.replace("""<gRingPoint>
                <gRingLatitude>34.123</gRingLatitude>
                <gRingLongitude>-118.25</gRingLongitude>
            </gRingPoint>
            <gRingPoint>
                <gRingLatitude>-18.25</gRingLatitude>
                <gRingLongitude>+25</gRingLongitude>
            </gRingPoint>
            <gRingPoint>
                <gRingLatitude>+78.25</gRingLatitude>
                <gRingLongitude>45.24755</gRingLongitude>
            </gRingPoint>""", """
<gRing>34.123, -118.25 -18.25, 25 78.25, 45.24755</gRing>
            """)
        self.assertEqualTree(
            et.fromstring(text_xml),
            geo_coverage.to_element(),
            "Error on to element"
        )

    def test_xml_to_polygon_with_points(self):
        xml = """
<datasetGPolygon>
    <datasetGPolygonOuterGRing>
        <gRingPoint>
            <gRingLatitude>34.123</gRingLatitude>
            <gRingLongitude>-118.25</gRingLongitude>
        </gRingPoint>
        <gRingPoint>
            <gRingLatitude>-18.25</gRingLatitude>
            <gRingLongitude>+25</gRingLongitude>
        </gRingPoint>
        <gRingPoint>
            <gRingLatitude>+78.25</gRingLatitude>
            <gRingLongitude>+78.25</gRingLongitude>
        </gRingPoint>
    </datasetGPolygonOuterGRing>
</datasetGPolygon>
        """
        element = et.fromstring(xml)
        polygon = GeographicCoverage.xml_to_polygon(element, {})
        self.assertEqual(
            [(34.123, -118.25), (-18.25, 25), (78.25, 78.25)],
            polygon.outer,
            "Error on parsing to polygon"
        )

    def test_xml_to_polygon_with_ring(self):
        xml = """
<datasetGPolygon>
    <datasetGPolygonOuterGRing>
        <gRing>12, 2.0987 12, -7.5555 34.345,10.40</gRing>
    </datasetGPolygonOuterGRing>
    <datasetGPolygonExclusionGRing>
        <gRing>13, 2.0987 12, -7.5555 34.345, 100</gRing>
    </datasetGPolygonExclusionGRing>
    <datasetGPolygonExclusionGRing>
        <gRing>15, 2.0987 12, -7.5555 34.345, 40</gRing>
    </datasetGPolygonExclusionGRing>
</datasetGPolygon>
        """
        element = et.fromstring(xml)
        polygon = GeographicCoverage.xml_to_polygon(element, {})
        self.assertEqual(
            [(12, 2.0987), (12, -7.5555), (34.345, 10.40)],
            polygon.outer,
            "Error on parsing to polygon (outer)"
        )
        self.assertEqual(
            GRing((13, 2.0987), (12, -7.5555), (34.345, 100)),
            polygon.exclusion[0],
            "Error on parsing to polygon (first exclusion)"
        )
        self.assertEqual(
            [(15, 2.0987), (12, -7.5555), (34.345, 40)],
            polygon.exclusion[1],
            "Error on parsing to polygon (second exclusion)"
        )
        self.assertNotEqual(
            ((15, 2.0987), (12, -7.5555), (34.345, 40)),
            polygon.exclusion[1],
            "Error on equals implementation"
        )

    def test_polygon_to_xml(self):
        xml = """
<datasetGPolygon>
    <datasetGPolygonOuterGRing>
        <gRing>12, 2.0987 12, -7.5555 34.345, 10.40</gRing>
    </datasetGPolygonOuterGRing>
    <datasetGPolygonExclusionGRing>
        <gRing>12, 2.0987 12, -7.5555 34.345, 10.40</gRing>
    </datasetGPolygonExclusionGRing>
    <datasetGPolygonExclusionGRing>
        <gRing>12, 2.0987 12, -7.5555 34.345, 10.40</gRing>
    </datasetGPolygonExclusionGRing>
</datasetGPolygon>
        """
        polygon = GPolygon(
            outer=GRing((12, 2.0987), (12, -7.5555), (34.345, 10.40)),
            exclusion=[
                GRing((12, 2.0987), (12, -7.5555), (34.345, 10.40)),
                GRing((12, 2.0987), (12, -7.5555), (34.345, 10.40)),
            ],
        )
        element = GeographicCoverage.polygon_to_xml(polygon)
        self.assertEqualTree(
            et.fromstring(xml),
            element,
            "Error on generate element from polygon"
        )


if __name__ == '__main__':
    unittest.main()
