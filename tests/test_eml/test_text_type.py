import unittest
from lxml import etree as et

from dwca.utils import Language
from eml.types import EMLTextType, EMLSection
from test_xml.test_xml import TestXML


class TestAbstract(TestXML):
    PARAGRAPH = ("Lorem ipsum dolor sit amet, consectetur "
                 "adipiscing elit. Sed euismod urna sit amet "
                 "pulvinar porttitor. Ut aliquet lectus sit amet.")
    ENG_PARAGRAPH = ("The company's marketing team will be "
                     "added to the company's budget. At a "
                     "price tag, it's now a real estate company, "
                     "at times.")
    ESP_PARAGRAPH = ("El equipo de marketing de la empresa se "
                     "agregará al presupuesto de la empresa. Por "
                     "un precio, ahora es una empresa de bienes "
                     "raíces, a veces.")
    MARKDOWN = ("*Lorem ipsum* dolor sit amet, _consectetur_ "
                "adipiscing elit. Sed euismod urna sit amet "
                "pulvinar porttitor. Ut aliquet lectus sit amet. "
                "Generated using [Lorem ipsum generator](https://www.lipsum.com/)")
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
    }

    def test_parse_simple(self):
        text_xml = f"""
<abstract>
    <para>{self.PARAGRAPH}</para>
</abstract>
        """
        abstract = EMLTextType.from_string(text_xml)
        self.assertEqual(0, len(abstract.sections), "Section generated from nowhere")
        self.assertEqual(self.PARAGRAPH, abstract.paragraphs[0], "Paragraph parsed incorrectly")
        self.assertEqual(0, len(abstract.markdowns), "Markdown generated from nowhere")
        self.assertEqual(Language.ENG, abstract.language, "Language parsed incorrectly")
        self.assertRaises(
            RuntimeError,
            abstract.to_element
        )
        abstract.set_tag("abstract")
        self.assertEqualTree(et.fromstring(text_xml), abstract.to_element(), "To element incorrect")

    def test_parse_empty(self):
        text_xml = "<abstract></abstract>"
        abstract = EMLTextType.from_string(text_xml)
        self.assertEqual(0, len(abstract.sections), "Section generated from nowhere")
        self.assertEqual(0, len(abstract.paragraphs), "Paragraph generated from nowhere")
        self.assertEqual(0, len(abstract.markdowns), "Markdown generated from nowhere")
        self.assertRaises(
            RuntimeError,
            abstract.to_element
        )
        abstract.set_tag("abstract")
        self.assertEqualTree(et.fromstring(text_xml), abstract.to_element(), "To element incorrect")

    def test_parse_complete(self):
        text_xml = f"""
<abstract>
    <section>
        <para>A small section</para>
    </section>
    <para>{self.PARAGRAPH}</para>
    <markdown>{self.MARKDOWN}</markdown>
</abstract>
        """
        abstract = EMLTextType.from_string(text_xml)
        self.assertEqual(
            EMLSection(paragraph="A small section"),
            abstract.sections[0],
            "Section parsed incorrectly"
        )
        self.assertEqual(self.PARAGRAPH, abstract.paragraphs[0], "Paragraph parsed incorrectly")
        self.assertEqual(self.MARKDOWN, abstract.markdowns[0], "Markdown parsed incorrectly")
        self.assertRaises(
            RuntimeError,
            abstract.to_element
        )
        abstract.set_tag("abstract")
        self.assertEqualTree(et.fromstring(text_xml), abstract.to_element(), "To element incorrect")

    def test_parse_none(self):
        self.assertIsNone(EMLTextType.parse(None, {}), "Error on parse None")

    def test_multilanguage(self):
        text_xml = f"""
<abstract>
    <para xml:lang="eng">{self.ENG_PARAGRAPH}</para>
    <para xml:lang="esp">{self.ESP_PARAGRAPH}</para>
    <markdown>{self.MARKDOWN}</markdown>
</abstract>
        """
        abstract = EMLTextType.from_string(text_xml)
        self.assertEqual(0, len(abstract.sections), "Section generated from nowhere")
        self.assertEqual(self.ENG_PARAGRAPH, abstract.paragraphs[0], "English Paragraph parsed incorrectly")
        self.assertEqual(Language.ENG, abstract.paragraphs[0].language, "English Paragraph wrong language")
        self.assertEqual(self.ESP_PARAGRAPH, abstract.paragraphs[1], "Spanish Paragraph parsed incorrectly")
        self.assertEqual(Language.ESP, abstract.paragraphs[1].language, "Spanish Paragraph wrong language")
        self.assertRaises(
            RuntimeError,
            abstract.to_element
        )
        abstract.set_tag("abstract")
        self.assertEqualTree(et.fromstring(text_xml), abstract.to_element(), "To element incorrect")


if __name__ == '__main__':
    unittest.main()
