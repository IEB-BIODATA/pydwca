import os
import unittest
import lxml.etree as et

from dwca.metadata import Metadata
from test_xml.test_xml import TestXML


class MyTestCase(TestXML):
    def setUp(self) -> None:
        with open(os.path.join("example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        self.metadata = et.fromstring(content)
        self.text = et.tostring(self.metadata, pretty_print=True).decode("utf-8")
        return

    def test_parse(self):
        meta = Metadata.from_string(self.text)
        self.assertEqual("eml.xml", meta.metadata_filename,"Metadata not found in file")
        self.assertEqual(0, meta.core.id, "Core not found")
        self.assertEqual(3, len(meta.extensions), "Extensions not found")
        self.assertEqual(0, meta.extensions[0].core_id, "First extension not found")
        self.assertEqual(0, meta.extensions[1].core_id, "Second extension not found")
        self.assertEqual(0, meta.extensions[2].core_id, "Third extension not found")
        self.assertEqualTree(self.metadata, meta.to_element(), "Not same tree generated")


if __name__ == '__main__':
    unittest.main()
