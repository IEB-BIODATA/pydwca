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
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:360"])
        self.assertEqual(11, len(parents_set), "Incorrect number of parents.")
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:366"])
        self.assertEqual(14, len(parents_set), "Incorrect number of parents.")
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:360", "urn:lsid:example.org:taxname:366"])
        self.assertEqual(14, len(parents_set), "Incorrect number of parents.")

    def test_get_incorrect_parent(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        with self.assertWarnsRegex(UserWarning, taxa_id):
            missing = self.taxon.get_parents([taxa_id])
            self.assertEqual(0, len(missing), "Parent found of invalid taxon id")

    def test_get_synonyms(self):
        self.read_pandas()
        first_synonyms = self.taxon.all_synonyms(["urn:lsid:example.org:taxname:10000"])
        self.assertEqual(2, len(first_synonyms), "Incorrect number of synonyms.")
        second_synonyms = self.taxon.all_synonyms(["urn:lsid:example.org:taxname:10001"])
        self.assertEqual(2, len(second_synonyms), "Incorrect number of synonyms.")
        self.assertCountEqual(
            first_synonyms, second_synonyms, "Synonyms do not match"
        )
        two_synonyms = self.taxon.all_synonyms(
            ["urn:lsid:example.org:taxname:10000", "urn:lsid:example.org:taxname:100005"])
        self.assertEqual(3, len(two_synonyms), "Incorrect number of synonym with a taxa with no synonymous.")
        self.assertTrue("urn:lsid:example.org:taxname:100005" in two_synonyms, "Incorrect same synonym")

    def test_get_synonyms_names(self):
        self.read_pandas()
        first_synonyms = self.taxon.all_synonyms(["urn:lsid:example.org:taxname:10000"], get_names=True)
        self.assertEqual(2, len(first_synonyms), "Incorrect number of synonyms.")
        second_synonyms = self.taxon.all_synonyms(["urn:lsid:example.org:taxname:10001"], get_names=True)
        self.assertEqual(2, len(second_synonyms), "Incorrect number of synonyms.")
        self.assertCountEqual(
            first_synonyms, second_synonyms, "Synonyms do not match"
        )
        two_synonyms = self.taxon.all_synonyms([
            "urn:lsid:example.org:taxname:10000", "urn:lsid:example.org:taxname:100005"
        ], get_names=True)
        self.assertEqual(3, len(two_synonyms), "Incorrect number of synonym with a taxa with no synonymous.")
        self.assertTrue(
            "Wxjncmbdqbd (Jdhbtbju) oojmaovly var. ushibyxcfc Whhngbhiq" in two_synonyms,
            "Incorrect same synonym"
        )

    def test_get_incorrect_synonyms(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        with self.assertWarnsRegex(UserWarning, "urn:lsid:example.org:taxname:300000"):
            synonyms = self.taxon.all_synonyms([taxa_id])
            self.assertEqual(0, len(synonyms), "Found something of false taxon id.")

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

    def test_filter_order(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_order([
            "Emicapsmvx", "Qyztmnpzz", "Udfewrqmk", "Ffknrbypsk", "Tqmvrbmttmo", "Xhngcistiqri", "Iwxoydtagzew",
            "Civppxeuqtes", "Xmvvualtokh", "Rbaliuycliu", "Xlhofowltm", "Jqgigdqsvqtw", "Mrvmytfgxyb", "Krwyqoqmeih",
            "Zcucwtks", "Lphobkhmtio", "Gwmtzgbm", "Wryqyvfr", "Koblytwog", "Oqqwmlsoycmg", "Mrplaoqwi"
        ])
        self.assertEqual(length, len(self.taxon), "Filter by all orders.")
        self.taxon.filter_by_order(["Rbaliuycliu", "Xlhofowltm"])
        self.assertEqual(39834 + 4, len(self.taxon), "Incorrect filter.")

    def test_filter_family(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_family([
            "Yzpkpquxs", "Aagnljgrt", "Kdahroigttef", "Wbeobsbx", "Uzajhqjglr", "Qmsjwosehsjg", "Jcvvsouvb", "Geitphvl",
            "Szlglzepeoj", "Tuguotkggz", "Csmeldytb", "Yvnmmueju", "Wykuuqdtfh", "Dxojfzqb", "Nwzoybkyquv",
            "Xvflpivgwtw", "Hbznvnpvdlll", "Nytpapprh", "Cdaukfqnbild", "Dvfwfnrosp", "Vowctemwht", "Yhfsclavzwz",
            "Dcohvbddjk", "Rtuitsplmqrw", "Kxwbhmfxwmah", "Abaxaenj", "Cscukzira", "Dxaougdpy", "Kvtgqwfmy",
            "Hoskerxymj", "Bmtbnvhlsn", "Jaksslqkhna", "Gvwkrzuzcsm", "Qejrpechiokg", "Ldbjloyw", "Acxcalcjb",
            "Exudmuohg", "Jisevptt", "Dmlkwsbankpr", "Ebxkmrllsmhb", "Fhhnxbgsj", "Blvgjqyf", "Ofrmsymysbj",
            "Iegtwpmzsn", "Uxlbjpgytrr", "Yppvqkvpyg", "Ufeoonfwvbwj", "Wxnibhsng", "Gzhzmloknffb", "Yqzeqqieric",
            "Bwysxkndbdo", "Aujqbritahm", "Nnjnmwvudn", "Pnpuqusvjmoh", "Qubplgsfgbf", "Aatwuzftuuh", "Mieccdvk",
            "Dakljsno", "Jqvrvbesgygm", "Iuzgldlop", "Xiuuksnsmk", "Cvbllcbq", "Hfwzlwzsmin", "Rqbbjpso", "Ipfvwairk",
            "Nbtktczp", "Jodyeaftwmzy", "Xuejrpuqj", "Xbezapgssp", "Iqrmrnbiovqz", "Wkttduowlm", "Xnxaxfml",
            "Bzivoaubjpig"
        ])
        self.assertEqual(length, len(self.taxon), "Filter by all families.")
        self.taxon.filter_by_family(["Dxaougdpy", "Kvtgqwfmy"])
        self.assertEqual(9969 + 5, len(self.taxon), "Incorrect filter.")

    def test_filter_genus(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_genus(["Hbqrtfopjuh", "Vbpjkmfqd"])
        self.assertEqual(624 + 11, len(self.taxon), "Incorrect filter.")

    def test_filter_species(self):
        self.read_pandas()
        length = len(self.taxon)
        self.assertEqual(length, len(self.taxon), "Original length of dataframe.")
        species_synonym = "Hqmjhacvb (Azvoxtzhwueu) gupfjmnf"
        variety = "Rtfkiaicpdng obzninluz var. cebwyzcqoy Glhnskwn"
        cultivar = "Rtfkiaicpdng (Abifwvxqn) gurqtwpof f. prczacpvtdtu 'xzhgezqpaorp'"
        self.taxon.filter_by_species([species_synonym, variety, cultivar])
        self.assertEqual(24, len(self.taxon), "Filter by all genera.")

    def test_none(self):
        self.assertIsNone(Taxon.parse(None, {}), "Object parsed from nothing")

    def test_no_pandas(self):
        self.read_pandas()
        with self.assertRaisesRegex(ImportError, "Install pandas to use this feature"):
            var = self.taxon.pandas


if __name__ == '__main__':
    unittest.main()
