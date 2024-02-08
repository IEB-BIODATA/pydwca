import unittest

from lxml import etree as et

from eml.types import SemanticAnnotation
from test_xml.test_xml import TestXML


class TestAnnotation(TestXML):
    DEFAULT_TAGS = {
        "scope": "document"
    }

    def test_parse(self):
        text_xml = """
<annotation id="Annotation">
    <propertyURI 
        label="has characteristic"
    >http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic</propertyURI>
    <valueURI
        label="Mass"
    >http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass</valueURI>
</annotation>
        """
        annotation = SemanticAnnotation.from_string(text_xml)
        self.assertEqual(
            "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic",
            annotation.property_uri,
            "Error on parsing property URI"
        )
        self.assertEqual(
            "has characteristic",
            annotation.property_uri.label,
            "Error on parsing property URI label"
        )
        self.assertEqual(
            "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass",
            annotation.value_uri,
            "Error on parsing value URI"
        )
        self.assertEqual(
            "Mass",
            annotation.value_uri.label,
            "Error on parsing value URI label"
        )
        self.assertRaises(
            RuntimeError,
            annotation.to_element
        )
        annotation.set_tag("annotation")
        self.assertEqualTree(et.fromstring(text_xml), annotation.to_element(), "Error on to element")

    def test_referencing(self):
        text_xml = """
<annotation>
    <references>Invalid</references>
</annotation>
        """
        self.assertRaises(
            ValueError, SemanticAnnotation.from_string, text_xml
        )


if __name__ == '__main__':
    unittest.main()
