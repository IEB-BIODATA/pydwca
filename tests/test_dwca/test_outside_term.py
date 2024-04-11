import unittest

from lxml import etree as et
from dwca.terms import OutsideTerm


class TestField(unittest.TestCase):
    def test_parse(self):
        field = OutsideTerm.from_string('<field index="1" term="http://rs.tdwg.org/dwc/terms/scientificNameID"/>')
        self.assertEqual(1, field.index, "Wrong parse index")
        self.assertEqual("http://rs.tdwg.org/dwc/terms/scientificNameID", field.uri, "Wrong parse term")
        self.assertIsNone(field.default, "Wrong parse default value")
        self.assertIsNone(field.vocabulary, "Wrong parse vocabulary value")

    def test_parse_invalid(self):
        self.assertRaises(
            ValueError,
            OutsideTerm.from_string,
            '<field index="OK" term="http://rs.tdwg.org/dwc/terms/scientificNameID"/>'
        )
        self.assertRaises(
            AssertionError,
            OutsideTerm.from_string,
            '<archive index="0" term="Valid Term"/>'
        )
        self.assertRaises(
            TypeError,
            OutsideTerm.from_string,
            '<field index="2"/>'
        )

    def test_xml(self):
        field = OutsideTerm(index=1, uri="http://rs.tdwg.org/dwc/terms/scientificNameID")
        expected = et.Element("field")
        expected.set("term", "http://rs.tdwg.org/dwc/terms/scientificNameID")
        expected.set("index", "1")
        actual = et.fromstring(field.to_xml())
        self.assertEqual(et.tostring(expected), et.tostring(actual), "Wrong xml generated")


if __name__ == '__main__':
    unittest.main()
