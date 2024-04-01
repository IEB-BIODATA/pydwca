import unittest

from lxml import etree as et

from dwca.terms import OrganismQuantity
from test_xml.test_xml import TestXML


class TestUnionField(TestXML):
    def test_parse(self):
        organism_quantity_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/organismQuantity"/>"""
        organism_quantity = OrganismQuantity.from_string(organism_quantity_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/organismQuantity",
            organism_quantity.uri,
            "Wrong URI"
        )
        self.assertEqual(3, organism_quantity.index, "Wrong index")
        self.assertEqualTree(
            et.fromstring(organism_quantity_xml),
            organism_quantity.to_element(),
            "Wrong generated element."
        )
        pass

    def test_format(self):
        organism_quantity = OrganismQuantity(3)
        value = "many"
        self.assertEqual(
            value, organism_quantity.format(value), "Error formatting union (string)"
        )
        value = "14.8"
        self.assertGreaterEqual(
            1e-10, abs(organism_quantity.format(value) - 14.8), "Error formatting union (float)"
        )
        value = "3"
        self.assertEqual(
            3, organism_quantity.format(value), "Error formatting union (int)"
        )


if __name__ == '__main__':
    unittest.main()
