import unittest

from eml.base import EML
from eml.types import SemanticAnnotation
from test_xml.test_xml import TestXML


class TestAnnotation(TestXML):
    def setUp(self) -> None:
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
        self.semantic_annotation = SemanticAnnotation.from_string(text_xml)
        return

    def test_equal(self):
        first_annotation = EML.Annotation(self.semantic_annotation, "example")
        self.assertIn(
            self.semantic_annotation,
            (first_annotation, ),
            "Semantic annotation not the same"
        )
        self.assertEqual(
            first_annotation,
            first_annotation,
            "Same annotation not equal"
        )
        second_annotation = EML.Annotation(self.semantic_annotation, "example")
        self.assertEqual(
            first_annotation,
            second_annotation,
            "Equal annotation not equal"
        )
        self.assertNotEqual(1, first_annotation, "Annotation equal to an int")

    def test_annotation(self):
        annotation = EML.Annotation(self.semantic_annotation, "example")
        self.assertEqual(
            self.semantic_annotation,
            annotation.annotation,
            "Annotation incorrectly got"
        )

    def test_reference(self):
        annotation = EML.Annotation(self.semantic_annotation, "example")
        self.assertEqual(
            "example",
            annotation.references,
            "References incorrectly got"
        )


if __name__ == '__main__':
    unittest.main()
