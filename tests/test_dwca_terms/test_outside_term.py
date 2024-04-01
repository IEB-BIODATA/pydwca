import unittest
from typing import Callable

from lxml import etree as et

from dwca.terms import OutsideTerm
from test_xml.test_xml import TestXML


class TestOutsideTerm(TestXML):
    def test_simple_term(self):
        term_xml = """
<field index="0" term="http://example.org/terms/example"/>
        """
        term = OutsideTerm.from_string(term_xml)
        self.assertEqual(0, term.index, "Index wrongly parsed")
        self.assertIsNone(term.default, "Default value from nowhere")
        self.assertIsNone(term.vocabulary, "Vocabulary from nowhere")
        self.assertEqual("http://example.org/terms/example", term.uri, "URI wrongly parsed")
        self.assertEqualTree(et.fromstring(term_xml), term.to_element(), "Error on to element")

    def test_complete_term(self):
        term_xml = """
<field
    index="0"
    term="http://example.org/terms/example"
    default="Default value"
    vocabulary="http://example.org/vocabulary/example"
/>
        """
        term = OutsideTerm.from_string(term_xml)
        self.assertEqual(0, term.index, "Index wrongly parsed")
        self.assertEqual("Default value", term.default, "Default wrongly parsed")
        self.assertEqual("http://example.org/vocabulary/example", term.vocabulary, "Vocabulary wrongly parsed")
        self.assertEqual("http://example.org/terms/example", term.uri, "URI wrongly parsed")
        self.assertEqualTree(et.fromstring(term_xml), term.to_element(), "Error on to element")

    def test_repr(self):
        term_xml = """
        <field index="0" term="http://example.org/terms/example"/>
                """
        term = OutsideTerm.from_string(term_xml)
        self.assertEqual(
            "<Field [term=http://example.org/terms/example]>",
            repr(term),
            "Term wrongly parsed"
        )

    def test_parse_none(self):
        self.assertIsNone(
            OutsideTerm.parse(None, {}),
            "Parse term from nowhere"
        )

    def test_no_index(self):
        self.assertRaises(
            TypeError,
            OutsideTerm.from_string,
            """
<field index="0"/>
            """
        )

    def test_invalid_format(self):
        term = OutsideTerm(3, "http://example.org/terms/example")

        class A:
            pass

        term.TYPE = A
        self.assertRaisesRegex(
            TypeError, "automatic conversion",
            term.format, "a"
        )
        term.TYPE = Callable
        self.assertRaisesRegex(
            TypeError, "automatic conversion",
            term.format, "a"
        )


if __name__ == '__main__':
    unittest.main()
