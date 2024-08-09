import os.path
import sys
import unittest

from lxml import etree as et

from dwca.classes import Taxon
from test_dwca_classes.test_taxon_common import TestTaxonCommon

PATH = os.path.abspath(os.path.dirname(__file__))


class TestTaxon(TestTaxonCommon):
    def setUp(self) -> None:
        sys.modules['pandas'] = None
        self.nmap, self.taxon_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        self.taxon = None
        return

    def tearDown(self) -> None:
        del sys.modules['pandas']
        return

    def test_add_field(self):
        super().__test_add_field__()

    def test_add_field_incorrect_index(self):
        super().__test_add_field_incorrect_index__()

    def test_parse(self):
        super().__test_parse__()

    def test_filter_kingdom_exception(self):
        super().__test_filter_kingdom_exception__()

    def test_get_parents(self):
        super().__test_get_parents__()

    def test_get_incorrect_parent(self):
        self.__test_get_incorrect_parent__()

    def test_get_synonyms(self):
        self.__test_get_synonyms__()

    def test_get_synonyms_names(self):
        super().__test_get_synonyms_names__()

    def test_get_incorrect_synonyms(self):
        self.__test_get_incorrect_synonyms__()

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
        super().__test_none__()

    def test_merge(self):
        super().__test_merge__()

    def test_no_pandas(self):
        self.read_pandas()
        with self.assertRaisesRegex(ImportError, "Install pandas to use this feature"):
            var = self.taxon.pandas


if __name__ == '__main__':
    unittest.main()
