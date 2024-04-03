import os.path
import sys
import unittest

from lxml import etree as et

from dwca.classes import Taxon
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestTaxon(TestXML):
    def setUp(self) -> None:
        sys.modules['pandas'] = None
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.taxon_xml = base_file.find("core", namespaces=base_file.nsmap)
        self.text = et.tostring(self.taxon_xml, pretty_print=True).decode("utf-8")
        self.taxon = None
        return

    def tearDown(self) -> None:
        del sys.modules['pandas']
        return

    def read_pandas(self):
        self.taxon = Taxon.from_string(self.text)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon.txt"), "r", encoding="utf-8") as file:
            self.taxon.read_file(file.read())
        return

    def test_parse(self):
        taxon = Taxon.from_string(self.text)
        self.assertEqual("taxon.txt", taxon.filename, "Files parse incorrectly")
        self.assertEqual(0, taxon.id, "Files parse incorrectly")
        self.assertEqual("UTF-8", taxon.__encoding__, "Encoding parse incorrectly")
        self.assertEqual("\n", taxon.__lines_end__, "Lines end parse incorrectly")
        self.assertEqual("\t", taxon.__fields_end__, "Field end parse incorrectly")
        self.assertEqual("", taxon.__fields_enclosed__, "Field enclosed parse incorrectly")
        self.assertEqual(1, taxon.__ignore_header_lines__, "Ignore header parse incorrectly")
        self.assertEqual(Taxon.URI, taxon.uri, "Row type parse incorrectly")
        self.assertEqual(47, len(taxon.__fields__), "Fields parse incorrectly")
        self.assertEqualTree(self.taxon_xml, taxon.to_element(), "Error on element conversion")

    def test_get_parents(self):
        self.read_pandas()
        parents_set = self.taxon.get_parents("urn:lsid:example.org:taxname:360")
        self.assertEqual(11, len(parents_set), "Incorrect number of parents.")
        parents_set = self.taxon.get_parents("urn:lsid:example.org:taxname:366")
        self.assertEqual(14, len(parents_set), "Incorrect number of parents.")

    def test_get_incorrect_parent(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        self.assertRaisesRegex(
            ValueError, taxa_id, self.taxon.get_parents, taxa_id
        )

    def test_get_synonyms(self):
        self.read_pandas()
        first_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:10000")
        self.assertEqual(2, len(first_synonyms), "Incorrect number of synonyms.")
        second_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:10001")
        self.assertEqual(2, len(second_synonyms), "Incorrect number of synonyms.")
        self.assertCountEqual(
            first_synonyms, second_synonyms, "Synonyms do not match"
        )
        no_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:100005")
        self.assertEqual(1, len(no_synonyms), "Incorrect number of synonym with a taxa with no synonymous.")
        self.assertEqual("urn:lsid:example.org:taxname:100005", no_synonyms[0], "Incorrect same synonym")

    def test_get_synonyms_names(self):
        self.read_pandas()
        first_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:10000", get_names=True)
        self.assertEqual(2, len(first_synonyms), "Incorrect number of synonyms.")
        second_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:10001", get_names=True)
        self.assertEqual(2, len(second_synonyms), "Incorrect number of synonyms.")
        self.assertCountEqual(
            first_synonyms, second_synonyms, "Synonyms do not match"
        )
        no_synonyms = self.taxon.all_synonyms("urn:lsid:example.org:taxname:100005", get_names=True)
        self.assertEqual(1, len(no_synonyms), "Incorrect number of synonym with a taxa with no synonymous.")
        self.assertEqual(
            "Wxjncmbdqbd Jdhbtbju oojmaovly var. ushibyxcfc Whhngbhiq",
            no_synonyms[0], "Incorrect same synonym"
        )

    def test_get_incorrect_synonyms(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        self.assertRaisesRegex(
            ValueError, taxa_id, self.taxon.all_synonyms, taxa_id
        )

    def test_filter_kingdom(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_kingdom(["Ydhxpqku", "Zcmmvusczo"])
        self.assertEqual(length, len(self.taxon), "Filter by all kingdoms.")
        self.taxon.filter_by_kingdom(["Ydhxpqku"])
        self.assertEqual(159490, len(self.taxon), "Filter by first kingdom.")

    def test_filter_phylum(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_phylum(["Ajiwcqftc", "Xpqnzcij", "Gdhevlcsj", "Xtgktcts"])
        self.assertEqual(length, len(self.taxon), "Filter by all phylum.")
        self.taxon.filter_by_phylum(["Ajiwcqftc"])
        self.assertEqual(
            79772,
            len(self.taxon),
            "Incorrect filter by Ajiwcqftc."
        )

    def test_filter_class(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_class([
            "Rwqpdxtmzf", "Wturcymgs", "Yichyzkbff",
            "Mrtuudeumnwn", "Yoadtafayw", "Vicipbwnr",
            "Qipttfiyorbt", "Pvopxyxw",  "Uzskxjpkntg"
        ])
        self.assertEqual(length, len(self.taxon), "Filter by all classes.")
        self.taxon.filter_by_class(["Yichyzkbff"])
        self.assertEqual(
            1 + 39941 + 1 + 1,
            len(self.taxon),
            "Incorrect filter by Yichyzkbff."
        )

    def test_none(self):
        self.assertIsNone(Taxon.parse(None, {}), "Object parsed from nothing")

    def test_no_pandas(self):
        self.read_pandas()
        with self.assertRaisesRegex(ImportError, "Install pandas to use this feature"):
            var = self.taxon.pandas


if __name__ == '__main__':
    unittest.main()
