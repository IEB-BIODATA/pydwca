import os
import unittest
from lxml import etree as et

from eml.base import EML, EMLVersion
from dwca.utils import Language
from eml.resources import EMLResource
from eml.types import Scope
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestEML(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "phonetype": "voice",
    }

    def setUp(self) -> None:
        eml_path = os.path.join(PATH, os.pardir, "example_data", "eml.xml")
        self.eml = EML.from_xml(eml_path)
        with open(eml_path, "r", encoding="utf-8") as file:
            self.text_eml = file.read()
        self.element_eml = et.fromstring(self.text_eml)
        return

    def test_parse(self):
        self.assertEqual("Example Package", self.eml.package_id, "Error on package id read")
        self.assertEqual("http://gbif.org", self.eml.system, "Error on system")
        self.assertEqual(Scope.SYSTEM, self.eml.scope, "Error on Scope")
        self.assertEqual(Language.ENG, self.eml.language, "Wrong language")
        self.assertEqual(EMLResource.DATASET, self.eml.resource_type, "Wrong resource type found")
        self.assertIsNone(self.eml.access, "Access from nothing")
        self.assertEqual(0, len(self.eml.annotations), "Annotations from nothing")
        self.assertEqual(1, len(self.eml.additional_metadata), "Additional metadata not found")
        self.assertEqualTree(self.element_eml, self.eml.to_element(), "Error on generated element")

    def test_eml_version(self):
        self.assertEqual(EMLVersion.LATEST, EMLVersion.get_version(None), "Wrong default")
        self.assertRaises(
            NotImplementedError,
            EMLVersion.get_version,
            "any_url another_url"
        )
        wrong_version = EMLVersion.LATEST
        wrong_version._value_ = "wrong value"
        self.assertRaises(
            NotImplementedError,
            wrong_version.schema_location
        )


if __name__ == '__main__':
    unittest.main()
