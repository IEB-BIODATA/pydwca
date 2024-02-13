import unittest
from lxml import etree as et

from dwca.utils import Language
from eml.types import EMLSection
from test_xml.test_xml import TestXML


class TestSection(TestXML):
    PARAGRAPH = ("Lorem ipsum dolor sit amet, consectetur "
                 "adipiscing elit. Sed euismod urna sit amet "
                 "pulvinar porttitor. Ut aliquet lectus sit amet.")
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
    }

    def test_parse_simple(self):
        text_xml = f"""
<section>
    <title>A simple section</title>
    <para>{self.PARAGRAPH}</para>
</section>
        """
        section = EMLSection.from_string(text_xml)
        self.assertEqual("A simple section", section.title, "Title parsed incorrectly")
        self.assertEqual(Language.ENG, section.title.language, "Title language parsed incorrectly")
        self.assertEqual(self.PARAGRAPH, section.paragraph, "Paragraph parsed incorrectly")
        self.assertIsNone(section.section, "Section generated from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), section.to_element(), "To element incorrect")

    def test_parse_empty(self):
        text_xml = "<section></section>"
        self.assertRaises(ValueError, EMLSection.from_string, text_xml)

    def test_parse_none(self):
        self.assertIsNone(EMLSection.parse(None, {}), "Error on parse None")

    def test_equal(self):
        section = EMLSection(
            title="A simple section",
            paragraph="A simple paragraph"
        )
        section_esp = EMLSection(
            title="A simple section",
            paragraph="A simple paragraph",
            language=Language.ESP
        )
        self.assertEqual(section, section_esp, "Compare language")
        self.assertNotEqual(3, section_esp, "Error on equal implementation")

    def test_parse_no_title(self):
        text_xml = f"""
<section>
    <para>{self.PARAGRAPH}</para>
</section>
        """
        section = EMLSection.from_string(text_xml)
        self.assertIsNone(section.title, "Title generated from nowhere")
        self.assertEqual(self.PARAGRAPH, section.paragraph, "Paragraph parsed incorrectly")
        self.assertIsNone(section.section, "Section generated from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), section.to_element(), "To element incorrect")

    def test_parse_complete(self):
        text_xml = f"""
<section>
    <title>A simple section</title>
    <section>
        <para>{self.PARAGRAPH}</para>
    </section>
</section>
        """
        section = EMLSection.from_string(text_xml)
        self.assertEqual("A simple section", section.title, "Title parsed incorrectly")
        self.assertEqual(Language.ENG, section.title.language, "Title language parsed incorrectly")
        self.assertEqual(EMLSection(paragraph=self.PARAGRAPH), section.section, "Error on equal implementation")
        self.assertEqualTree(et.fromstring(text_xml), section.to_element(), "To element incorrect")

    def test_parse_recursive(self):
        text_xml = f"""
<section>
    <title>A simple section</title>
    <section>
        <title>One level section</title>
        <section xml:lang="esp">
            <title xml:lang="esp">Segundo nivel de recursión</title>
            <section>
                <title>Third level</title>
                <para>{self.PARAGRAPH}</para>
            </section>
        </section>
    </section>
</section>
        """
        section = EMLSection.from_string(text_xml)
        self.assertEqual("A simple section", section.title, "Title parsed incorrectly")
        self.assertEqual(Language.ENG, section.title.language, "Title language parsed incorrectly")
        self.assertEqual(Language.ENG, section.language, "Language parsed incorrectly")
        self.assertEqual("One level section", section.section.title, "Error on first recursion")
        self.assertEqual(Language.ENG, section.section.title.language, "Error on language on first recursion")
        self.assertEqual("Segundo nivel de recursión", section.section.section.title, "Error on second recursion")
        self.assertEqual(
            Language.ESP,
            section.section.section.title.language,
            "Error on language (title) on second recursion"
        )
        self.assertEqual(Language.ESP, section.section.section.language, "Error on language on second recursion")
        self.assertEqual("Third level", section.section.section.section.title, "Error on third recursion")
        self.assertEqual(
            Language.ENG,
            section.section.section.section.title.language,
            "Error on language on third recursion"
        )
        self.assertEqual(
            self.PARAGRAPH,
            section.section.section.section.paragraph,
            "Error on paragraph on third recursion"
        )


if __name__ == '__main__':
    unittest.main()
