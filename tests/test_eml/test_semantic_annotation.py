import unittest

from lxml import etree as et

from eml.types import SemanticAnnotation
from test_xml.test_xml import TestXML


class TestSemanticAnnotation(TestXML):
    DEFAULT_TAGS = {
        "scope": "document"
    }

    def setUp(self) -> None:
        self.text_xml = """
        <annotation id="Annotation">
            <propertyURI 
                label="has characteristic"
            >http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic</propertyURI>
            <valueURI
                label="Mass"
            >http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass</valueURI>
        </annotation>
                """
        self.annotation = SemanticAnnotation.from_string(self.text_xml)

    def test_parse(self):
        self.assertEqual(
            "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#ofCharacteristic",
            self.annotation.property_uri,
            "Error on parsing property URI"
        )
        self.assertEqual(
            "has characteristic",
            self.annotation.property_uri.label,
            "Error on parsing property URI label"
        )
        self.assertEqual(
            "http://ecoinformatics.org/oboe/oboe.1.2/oboe-characteristics.owl#Mass",
            self.annotation.value_uri,
            "Error on parsing value URI"
        )
        self.assertEqual(
            "Mass",
            self.annotation.value_uri.label,
            "Error on parsing value URI label"
        )
        self.assertRaises(
            RuntimeError,
            self.annotation.to_element
        )
        self.annotation.set_tag("annotation")
        self.assertEqualTree(et.fromstring(self.text_xml), self.annotation.to_element(), "Error on to element")

    def test_referencing(self):
        text_xml = """
<annotation>
    <references>Invalid</references>
</annotation>
        """
        self.assertRaises(
            ValueError, SemanticAnnotation.from_string, text_xml
        )

    def test_equal(self):
        annotation = SemanticAnnotation.from_string(self.text_xml)
        self.assertEqual(
            self.annotation,
            annotation,
            "Annotation not equal"
        )
        self.assertNotEqual(
            1,
            annotation,
            "Annotation equal to an integer"
        )



if __name__ == '__main__':
    unittest.main()
