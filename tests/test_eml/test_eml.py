import os
import unittest
import lxml.etree as et

from eml.base import EML
from dwca.utils import Language
from eml.resources import EMLResource
from test_xml.test_xml import TestXML


class TestEML(TestXML):
    def setUp(self) -> None:
        self.eml = EML.from_xml(os.path.join(os.pardir, "example_data", "eml.xml"))
        with open(os.path.join(os.pardir, "example_data", "eml.xml"), "r", encoding="utf-8") as file:
            self.text_eml = file.read()
        self.element_eml = et.fromstring(self.text_eml)
        return

    def test_parse(self):
        self.assertEqual(self.eml.package_id, "IRMNG_export_2023-05-19", "Error on package id read")
        self.assertEqual(self.eml.system, "http://gbif.org", "Error on system")
        self.assertEqual(self.eml.scope, "system", "Error on Scope")
        self.assertEqual(self.eml.language, Language.ENG, "Wrong language")
        self.assertEqual(self.eml.resource_type, EMLResource.DATASET, "Wrong resource type found")
        self.assertIsNone(self.eml.access, "Access from nothing")
        self.assertIsNone(self.eml.annotations, "Annotations from nothing")
        self.assertEqual(1, len(self.eml.additional), "Additional metadata not found")
        self.assertEqualTree(self.element_eml, self.eml.to_element(), "Error on generated element")


if __name__ == '__main__':
    unittest.main()
