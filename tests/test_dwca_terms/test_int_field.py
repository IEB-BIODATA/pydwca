import unittest

from lxml import etree as et

from dwca.terms import IndividualCount
from test_xml.test_xml import TestXML


class TestIntField(TestXML):
    def test_parse(self):
        ind_count_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/individualCount"/>"""
        ind_count = IndividualCount.from_string(ind_count_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/individualCount",
            ind_count.uri,
            "Wrong URI"
        )
        self.assertEqual(3, ind_count.index, "Wrong index")
        self.assertEqualTree(et.fromstring(ind_count_xml), ind_count.to_element(), "Wrong generated element.")
        pass

    def test_format(self):
        ind_count = IndividualCount(3)
        value = "30"
        self.assertEqual(
            30, ind_count.format(value), "Error formatting integer"
        )
        value = "Invalid integer"
        self.assertIsNone(ind_count.format(value), "Error formatting invalid integer")


if __name__ == '__main__':
    unittest.main()
