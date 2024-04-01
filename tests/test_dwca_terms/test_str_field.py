import unittest

from lxml import etree as et

from dwca.terms import EventID
from test_xml.test_xml import TestXML


class TestStringField(TestXML):
    def test_parse(self):
        event_id_xml = """<field index="2" term="http://rs.tdwg.org/dwc/terms/eventID"/>"""
        event_id = EventID.from_string(event_id_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/eventID",
            event_id.uri,
            "Wrong URI"
        )
        self.assertEqual(2, event_id.index, "Wrong index")
        self.assertEqualTree(et.fromstring(event_id_xml), event_id.to_element(), "Wrong generated element.")
        pass

    def test_format(self):
        event_id = EventID(2)
        value = "an_example_id"
        self.assertEqual(
            value, event_id.format(value), "Error formatting string"
        )


if __name__ == '__main__':
    unittest.main()
