import unittest
from lxml import etree as et
from dwca.utils import Language
from eml.resources import EMLKeywordSet, KeywordType
from test_xml.test_xml import TestXML


class TestKeyword(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng"
    }

    def test_parse_simple(self):
        text_xml = """
<keywordSet>
    <keyword>taxonomic</keyword>
    <keyword>database</keyword>
    <keyword>online</keyword>
    <keyword>species</keyword>
    <keywordThesaurus/>
</keywordSet>
        """
        keyword = EMLKeywordSet.from_string(text_xml)
        self.assertEqual(4, len(keyword.keywords), "Error on parsing keywords")
        self.assertEqual("", keyword.thesaurus, "Error on parsing thesaurus")
        self.assertEqual(4, len(keyword.keywords_type), "Error on parsing keywords")
        self.assertEqual([KeywordType.NULL] * 4, keyword.keywords_type, "Error on type of keywords")
        self.assertEqualTree(et.fromstring(text_xml), keyword.to_element(), "Error on to element")

    def test_parse_complete(self):
        text_xml = """
<keywordSet>
    <keyword keywordType="place" xml:lang="esp">Concepción</keyword>
    <keyword>database</keyword>
    <keyword>online</keyword>
    <keyword>species</keyword>
    <keyword xml:lang="esp">especies</keyword>
    <keyword keywordType="taxonomic">plantae</keyword>
    <keywordThesaurus>IRIS keyword thesaurus</keywordThesaurus>
</keywordSet>
        """
        keyword = EMLKeywordSet.from_string(text_xml)
        self.assertEqual(6, len(keyword.keywords), "Error on parsing keywords")
        self.assertEqual("IRIS keyword thesaurus", keyword.thesaurus, "Error on parsing thesaurus")
        self.assertEqual(6, len(keyword.keywords_type), "Error on parsing keywords")
        self.assertEqual(
            [
                KeywordType.PLACE,
                KeywordType.NULL,
                KeywordType.NULL,
                KeywordType.NULL,
                KeywordType.NULL,
                KeywordType.TAXONOMIC,
            ], keyword.keywords_type,
            "Error on type of keywords"
        )
        self.assertEqual(Language.ESP, keyword.keywords[4].language, "Error on keyword language")
        self.assertEqualTree(et.fromstring(text_xml), keyword.to_element(), "Error on to element")

    def test_keyword_type_default(self):
        keyword = EMLKeywordSet(["species", "database", "online", "taxonomic"])
        self.assertEqual(4, len(keyword.keywords_type), "Error on default types")
        self.assertEqual([KeywordType.NULL] * 4, keyword.keywords_type, "Error on default types specific")

    def test_keyword_language_default(self):
        keyword = EMLKeywordSet(["species", "database", "online", "taxonomic"])
        self.assertEqual(4, len(keyword.keywords), "Error on keywords")
        self.assertEqual([Language.ENG] * 4, [k.language for k in keyword.keywords], "Error on default languages")

    def test_keyword_invalid(self):
        self.assertRaises(
            ValueError,
            EMLKeywordSet,
            []
        )

    def test_keyword_invalid_parse(self):
        text_xml = """
<keywordSet>
</keywordSet>
        """
        self.assertRaises(
            ValueError,
            EMLKeywordSet.from_string,
            text_xml,
        )
        text_xml = """
<keywordSet>
    <keywordThesaurus>Example Thesaurus</keywordThesaurus>
</keywordSet>
        """
        self.assertRaises(
            ValueError,
            EMLKeywordSet.from_string,
            text_xml,
        )

    def test_keyword_type(self):
        keyword = EMLKeywordSet(
            ["conservation", "database", "online", "taxonomic"],
            keywords_type=[KeywordType.THEME]
        )
        self.assertEqual(4, len(keyword.keywords_type), "Error on default types")
        self.assertEqual([
            KeywordType.THEME,
            KeywordType.NULL,
            KeywordType.NULL,
            KeywordType.NULL,
        ], keyword.keywords_type,
            "Error on default types specific"
        )

    def test_parse_none(self):
        self.assertIsNone(EMLKeywordSet.parse(None, {}), "Parse from nowhere")

    def test_parse_invalid_type(self):
        text_xml = """
<keywordSet>
    <keyword keywordType="place" xml:lang="esp">Concepción</keyword>
    <keyword>database</keyword>
    <keyword>online</keyword>
    <keyword keywordType="species">species</keyword>
    <keyword keywordType="taxonomic">plantae</keyword>
    <keywordThesaurus>IRIS keyword thesaurus</keywordThesaurus>
</keywordSet>
        """
        keyword = EMLKeywordSet.from_string(text_xml)
        self.assertEqual(5, len(keyword.keywords), "Error on parsing keywords")
        self.assertEqual("IRIS keyword thesaurus", keyword.thesaurus, "Error on parsing thesaurus")
        self.assertEqual(5, len(keyword.keywords_type), "Error on parsing keywords")
        self.assertEqual(
            [
                KeywordType.PLACE,
                KeywordType.NULL,
                KeywordType.NULL,
                KeywordType.NULL,
                KeywordType.TAXONOMIC,
            ], keyword.keywords_type,
            "Error on type of keywords"
        )


if __name__ == '__main__':
    unittest.main()
