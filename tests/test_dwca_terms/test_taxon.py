import unittest

from lxml import etree as et

from dwca.terms import OutsideTerm, TaxonID, TaxonRank
from test_xml.test_xml import TestXML


class TestTaxon(TestXML):
    def test_taxon_id(self):
        term_xml = """
<field index="0" term="http://rs.tdwg.org/dwc/terms/taxonID"/>
        """
        term = TaxonID.from_string(term_xml)
        self.assertEqual(0, term.index, "Index wrongly parsed")
        self.assertIsNone(term.default, "Default value from nowhere")
        self.assertIsNone(term.vocabulary, "Vocabulary from nowhere")
        self.assertEqual("http://rs.tdwg.org/dwc/terms/taxonID", term.uri, "URI wrongly parsed")
        self.assertEqualTree(et.fromstring(term_xml), term.to_element(), "Error on to element")

    def test_taxon_rank(self):
        term_xml = """
<field
    index="0"
    term="http://rs.tdwg.org/dwc/terms/taxonRank"
    default="species"
    vocabulary="https://www.iapt-taxon.org/nomen/pages/main/art_3.html"
/>
        """
        term = TaxonRank.from_string(term_xml)
        self.assertEqual(0, term.index, "Index wrongly parsed")
        self.assertEqual("species", term.default, "Default wrongly parsed")
        self.assertEqual("https://www.iapt-taxon.org/nomen/pages/main/art_3.html", term.vocabulary, "Vocabulary wrongly parsed")
        self.assertEqual("http://rs.tdwg.org/dwc/terms/taxonRank", term.uri, "URI wrongly parsed")
        self.assertEqualTree(et.fromstring(term_xml), term.to_element(), "Error on to element")

    def test_repr(self):
        term_xml = """
<field index="0" term="http://rs.tdwg.org/dwc/terms/taxonID"/>
        """
        term = TaxonID.from_string(term_xml)
        self.assertEqual(
            "<Field [term=http://rs.tdwg.org/dwc/terms/taxonID]>",
            repr(term),
            "Taxon ID wrongly parsed"
        )

    def test_parse_none(self):
        self.assertIsNone(
            TaxonID.parse(None, {}),
            "Parse term from nowhere"
        )

    def test_parse_no_field(self):
        self.assertRaises(
            TypeError,
            TaxonID.from_string,
            """
<field index="0"/>
            """
        )


if __name__ == '__main__':
    unittest.main()
