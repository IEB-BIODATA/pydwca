import unittest
from lxml import etree as et

from eml.types import EMLPhone
from test_xml.test_xml import TestXML


class TestEMLPhone(TestXML):
    EXAMPLE_XML = """
<phone phonetype="voice">805-555-2500</phone>
    """

    def test_parse(self):
        eml_phone = EMLPhone.from_string(self.EXAMPLE_XML)
        self.assertEqual("805-555-2500", eml_phone, "Phone set incorrectly")
        self.assertEqual("voice", eml_phone.phone_type, "Phonetype set incorrectly")
        self.assertEqualTree(et.fromstring(self.EXAMPLE_XML), eml_phone.to_element(), "Incorrect generated element")
        return

    def test_equal(self):
        variable = EMLPhone("805-555-2500")
        self.assertEqual(EMLPhone("805-555-2500"), variable, "Phones not equal")
        self.assertNotEqual(8055552500, variable, "Phones equal to other type")
        self.assertNotEqual(EMLPhone("8055552500"), variable, "Phones equal to different phone")


if __name__ == '__main__':
    unittest.main()
