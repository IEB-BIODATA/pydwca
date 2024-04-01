import os
import unittest
from lxml import etree as et

from dwca.base import DarwinCoreArchive
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestMeta(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        self.metadata = et.fromstring(content)
        self.text = et.tostring(self.metadata, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        meta = DarwinCoreArchive.Metadata.from_string(self.text)
        self.assertEqual("eml.xml", meta.metadata_filename,"Metadata not found in file")
        self.assertEqual(0, meta.core.id, "Core not found")
        self.assertEqual(3, len(meta.extensions), "Extensions not found")
        self.assertEqual(0, meta.extensions[0].id, "First extension not found")
        self.assertEqual(0, meta.extensions[1].id, "Second extension not found")
        self.assertEqual(0, meta.extensions[2].id, "Third extension not found")
        self.assertEqualTree(self.metadata, meta.to_element(), "Not same tree generated")


if __name__ == '__main__':
    unittest.main()
