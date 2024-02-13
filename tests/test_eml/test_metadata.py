import os
import unittest

from lxml import etree as et

from eml.base import EMLAdditionalMetadata, EMLMetadata
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestMetadata(TestXML):
    def test_none(self):
        self.assertIsNone(EMLAdditionalMetadata.parse(None, {}), "Additional Metadata from nowhere")
        self.assertIsNone(EMLMetadata.parse(None, {}), "Metadata from nowhere")

    def test_parse(self):
        eml_path = os.path.join(PATH, os.pardir, "example_data", "eml.xml")
        with open(eml_path, "r", encoding="utf-8") as file:
            xml_tree = et.fromstring(file.read()).find("additionalMetadata")
        add_metadata = EMLAdditionalMetadata.from_string(et.tostring(xml_tree))
        metadata_tree = xml_tree.find("metadata")
        metadata = EMLMetadata.from_string(et.tostring(metadata_tree))
        self.assertEqualTree(metadata_tree, metadata.to_element(), "Error on metadata")
        self.assertEqualTree(xml_tree, add_metadata.to_element(), "Error on additional metadata")

    def test_complete(self):
        text_xml = """
<additionalMetadata id="A unique ID">
    <metadata>
        <example>Example</example>
        <anotherExample>Different Example</anotherExample>
    </metadata>
    <describes>Section 1</describes>
    <describes>Dataset 3</describes>
</additionalMetadata>
        """
        add_metadata = EMLAdditionalMetadata.from_string(text_xml)
        self.assertEqualTree(et.fromstring(text_xml), add_metadata.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
