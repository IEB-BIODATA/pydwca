import unittest

import lxml.etree as et
from dwca.metadata import Field


class TestField(unittest.TestCase):
    def test_parse(self):
        field = Field.from_string('<field index="1" term="http://rs.tdwg.org/dwc/terms/scientificNameID"/>')
        self.assertEqual(1, field.__index__, "Wrong parse index")
        self.assertEqual("http://rs.tdwg.org/dwc/terms/scientificNameID", field.__term__, "Wrong parse term")
        self.assertIsNone(field.__default__, "Wrong parse default value")
        self.assertIsNone(field.__vocabulary__, "Wrong parse vocabulary value")

    def test_parse_invalid(self):
        self.assertRaises(
            ValueError,
            Field.from_string,
            '<field index="OK" term="http://rs.tdwg.org/dwc/terms/scientificNameID"/>'
        )
        self.assertRaises(
            AssertionError,
            Field.from_string,
            '<archive index="0" term="Valid Term"/>'
        )
        self.assertRaises(
            TypeError,
            Field.from_string,
            '<field index="2"/>'
        )

    def test_xml(self):
        field = Field("http://rs.tdwg.org/dwc/terms/scientificNameID", index=1)
        expected = et.Element("field")
        expected.set("term", "http://rs.tdwg.org/dwc/terms/scientificNameID")
        expected.set("index", "1")
        actual = et.fromstring(field.to_xml())
        self.assertEqual(et.tostring(expected), et.tostring(actual), "Wrong xml generated")


if __name__ == '__main__':
    unittest.main()
