import unittest

from lxml import etree as et

from eml.resources.distribution import EMLOffline
from test_xml.test_xml import TestXML


class TestOffline(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
    }

    def test_parse_none(self):
        self.assertIsNone(EMLOffline.parse(None, {}), "EMLOffline from nowhere")

    def test_parse_invalid(self):
        text_xml = """
<offline>
    <mediumDensity>High Density (HD)</mediumDensity>
    <mediumDensityUnits>B/cm</mediumDensityUnits>
    <mediumVolume>650 MB</mediumVolume>
    <mediumFormat>NTFS</mediumFormat>
    <mediumNote>any additional pertinent information about the media</mediumNote>
</offline>
        """
        self.assertRaises(
            AttributeError,
            EMLOffline.from_string,
            text_xml
        )

    def test_parse_minimum(self):
        text_xml = """
<offline>
    <mediumName>Tape, 3.5 inch Floppy Disk, hardcopy</mediumName>
</offline>
        """
        offline = EMLOffline.from_string(text_xml)
        self.assertEqual("Tape, 3.5 inch Floppy Disk, hardcopy", offline.medium_name,
                         "Incorrect parsed of medium name")
        self.assertIsNone(offline.medium_density, "Incorrect parsed of medium density")
        self.assertIsNone(offline.medium_density_units, "Incorrect parsed of medium density units")
        self.assertIsNone(offline.medium_volume, "Incorrect parsed of medium volume")
        self.assertEqual(0, len(offline.medium_format), "Incorrect parsed of medium format")
        self.assertIsNone(offline.medium_note, "Incorrect parsed of medium note")
        self.assertEqualTree(et.fromstring(text_xml), offline.to_element(), "Error on to element")

    def test_parse_complete(self):
        text_xml = """
<offline>
    <mediumName>Tape, 3.5 inch Floppy Disk, hardcopy</mediumName>
    <mediumDensity>High Density (HD)</mediumDensity>
    <mediumDensityUnits>B/cm</mediumDensityUnits>
    <mediumVolume>650 MB</mediumVolume>
    <mediumFormat>NTFS</mediumFormat>
    <mediumNote>any additional pertinent information about the media</mediumNote>
</offline>
        """
        offline = EMLOffline.from_string(text_xml)
        self.assertEqual("Tape, 3.5 inch Floppy Disk, hardcopy", offline.medium_name,
                         "Incorrect parsed of medium name")
        self.assertEqual("High Density (HD)", offline.medium_density, "Incorrect parsed of medium density")
        self.assertEqual("B/cm", offline.medium_density_units, "Incorrect parsed of medium density units")
        self.assertEqual("650 MB", offline.medium_volume, "Incorrect parsed of medium volume")
        self.assertEqual(1, len(offline.medium_format), "Incorrect parsed of medium format")
        self.assertEqual("NTFS", offline.medium_format[0], "Incorrect parsed of medium format")
        self.assertEqual(
            "any additional pertinent information about the media",
            offline.medium_note,
            "Incorrect parsed of medium note"
        )
        self.assertEqualTree(et.fromstring(text_xml), offline.to_element(), "Error on to element")

    def test_parse_more_formats(self):
        text_xml = """
<offline>
    <mediumName>Tape, 3.5 inch Floppy Disk, hardcopy</mediumName>
    <mediumDensity>High Density (HD)</mediumDensity>
    <mediumDensityUnits>B/cm</mediumDensityUnits>
    <mediumVolume>650 MB</mediumVolume>
    <mediumFormat>NTFS</mediumFormat>
    <mediumFormat>FAT32</mediumFormat>
    <mediumFormat>EXT2</mediumFormat>
    <mediumFormat>QIK80</mediumFormat>
    <mediumNote>any additional pertinent information about the media</mediumNote>
</offline>
        """
        offline = EMLOffline.from_string(text_xml)
        self.assertEqual("Tape, 3.5 inch Floppy Disk, hardcopy", offline.medium_name,
                         "Incorrect parsed of medium name")
        self.assertEqual("High Density (HD)", offline.medium_density, "Incorrect parsed of medium density")
        self.assertEqual("B/cm", offline.medium_density_units, "Incorrect parsed of medium density units")
        self.assertEqual("650 MB", offline.medium_volume, "Incorrect parsed of medium volume")
        self.assertEqual(4, len(offline.medium_format), "Incorrect parsed of medium format")
        self.assertEqual(
            "NTFS, FAT32, EXT2, QIK80".split(", "),
            offline.medium_format,
            "Incorrect parsed of medium format"
        )
        self.assertEqual(
            "any additional pertinent information about the media",
            offline.medium_note,
            "Incorrect parsed of medium note"
        )
        self.assertEqualTree(et.fromstring(text_xml), offline.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
