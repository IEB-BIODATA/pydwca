import logging
import os.path
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from lxml import etree as et

from dwca.classes import Taxon
from dwca.terms import DWCLanguage, TaxonID
from test_dwca_classes.test_taxon_common import TestTaxonCommon
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))

orig_import = __import__


def import_mock_fuzzy(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'rapidfuzz':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


class TestTaxon(TestTaxonCommon):
    def setUp(self) -> None:
        self.nmap, self.taxon_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        self.taxon = None
        return

    def tearDown(self) -> None:
        if self.taxon is not None and self.taxon.is_lazy():
            self.taxon.close()

    def test_name(self):
        taxon = Taxon.from_string(self.text)
        self.assertEqual("Taxon", taxon.name, "Name parsed incorrectly.")

    def test_add_field(self):
        super().__test_add_field__()

    def test_add_field_incorrect_index(self):
        super().__test_add_field_incorrect_index__()

    def test_add_field_data(self):
        self.read_pandas()
        df = self.taxon.polars
        self.assertEqual(47, len(df.columns), "Wrong number of initial columns")
        self.assertRaisesRegex(
            AttributeError, "language",
            getattr,
            self.taxon.__entries__[0],
            "language"
        )
        self.taxon.add_field(DWCLanguage(index=47, default=Language.ENG))
        self.assertEqual(
            Language.ENG,
            self.taxon.__entries__[0].language,
            "Language not write on all entries"
        )
        df = self.taxon.polars
        self.assertEqual(48, len(df.columns), "Wrong number of columns after set")
        self.assertEqual(48, len(self.taxon.fields), "Fields not set")
        self.text = self.text.replace(
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>""",
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>
    <field index="47" default="eng" term="http://purl.org/dc/elements/1.1/language"/>""")
        self.assertEqual(Language.ENG, self.taxon.polars.item(7, "language"), "Wrong set default on polars.")
        self.assertEqual(Language.ENG, self.taxon.__entries__[7].language, "Wrong set default on entries.")
        self.assertEqualTree(et.fromstring(self.text), self.taxon.to_element(), "Error on element conversion with new field")

    def test_add_field_lazy(self):
        self.read_pandas(lazy=True)
        self.assertNotIn(
            DWCLanguage(0).uri,
            self.taxon.fields,
            "Language in fields"
        )
        self.assertIn(
            TaxonID(0).uri,
            self.taxon.fields,
            "TaxonID not in fields"
        )
        df = self.taxon.polars
        self.assertEqual(47, len(df.columns), "Wrong number of initial columns")
        self.read_pandas(lazy=True)
        self.taxon.add_field(DWCLanguage(index=47, default=Language.ENG))
        df = self.taxon.polars
        self.assertEqual(48, len(df.columns), "Wrong number of columns after set")
        self.assertEqual(48, len(self.taxon.fields), "Fields not set")
        self.text = self.text.replace(
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>""",
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>
    <field index="47" default="eng" term="http://purl.org/dc/elements/1.1/language"/>""")
        self.assertEqual(Language.ENG.value, self.taxon.polars.item(7, "language"), "Wrong set default on polars.")
        self.assertEqualTree(et.fromstring(self.text), self.taxon.to_element(),
                             "Error on element conversion with new field")


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
        df = self.taxon.pandas
        length_df = len(df)
        kingdom_summary = df.groupby("kingdom").size().to_dict()
        print(f"Kingdom Summary: {kingdom_summary}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_kingdom(kingdom_summary.keys())
        self.assertEqual(length_df, len(self.taxon), "Filter by all kingdoms.")
        first_kingdom = list(kingdom_summary.keys())[0]
        self.taxon.filter_by_kingdom([first_kingdom])
        self.assertEqual(kingdom_summary[first_kingdom], len(self.taxon), "Filter by first kingdom.")

    def test_filter_phylum(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        phylum_summary = df.groupby(["kingdom", "phylum"]).size().to_dict()
        kingdom_list = list()
        phylum_list = list()
        for candid in phylum_summary.keys():
            if candid[1] != "":
                phylum_list.append(candid[1])
            else:
                kingdom_list.append(candid[0])
        print(f"Phylum Summary: {phylum_summary}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_phylum(phylum_list)
        self.assertEqual(length_df, len(self.taxon), "Filter by all phylum.")
        self.taxon.filter_by_phylum([phylum_list[0]])
        self.assertEqual(
            phylum_summary[(kingdom_list[0], "")] + phylum_summary[(kingdom_list[0], phylum_list[0])],
            len(self.taxon),
            f"Incorrect filter by {phylum_list[0]}."
        )

    def test_filter_phylum_no_threshold(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        phylum_summary = df.groupby(["kingdom", "phylum"]).size().to_dict()
        kingdom_list = list()
        phylum_list = list()
        for candid in phylum_summary.keys():
            if candid[1] != "":
                phylum_list.append(candid[1])
            else:
                kingdom_list.append(candid[0])
        print(f"Phylum Summary: {phylum_summary}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        # Modified phylum 0
        # Change 2 letter
        phylum_as_list = list(phylum_list[0])
        phylum_as_list[4] = "Y"
        phylum_as_list.pop(3)
        phylum_list[0] = ''.join(phylum_as_list)
        self.taxon.filter_by_phylum(phylum_list, fuzzy_threshold=100)
        self.assertGreater(length_df, len(self.taxon), "Filter by all phylum with no threshold.")

    def test_filter_phylum_threshold(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        phylum_summary = df.groupby(["kingdom", "phylum"]).size().to_dict()
        kingdom_list = list()
        phylum_list = list()
        for candid in phylum_summary.keys():
            if candid[1] != "":
                phylum_list.append(candid[1])
            else:
                kingdom_list.append(candid[0])
        print(f"Phylum Summary: {phylum_summary}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        # Modified phylum 0
        # Change 2 letter
        phylum_as_list = list(phylum_list[0])
        phylum_as_list[4] = "Y"
        phylum_as_list.pop(3)
        phylum_list[0] = ''.join(phylum_as_list)
        self.taxon.filter_by_phylum(phylum_list, fuzzy_threshold=50)
        self.assertEqual(length_df, len(self.taxon), "Filter by all phylum with enough threshold.")
        self.taxon.filter_by_phylum(phylum_list, fuzzy_threshold=90)
        self.assertGreater(length_df, len(self.taxon), "Filter by all phylum with not enough threshold.")

    def test_filter_class(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        class_summary = df.groupby(["kingdom", "phylum", "class"]).size().to_dict()
        kingdom_list = list()
        phylum_list = list()
        class_list = list()
        for candid in class_summary.keys():
            if candid[2] != "":
                class_list.append(candid[2])
            else:
                if candid[1] != "":
                    phylum_list.append(candid[1])
                else:
                    kingdom_list.append(candid[0])
        print(f"Class Summary: {class_summary}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_class(class_list)
        self.assertEqual(length_df, len(self.taxon), "Filter by all classes.")
        self.taxon.filter_by_class([class_list[2]])
        self.assertEqual(
            class_summary[(kingdom_list[0], "", "")] +
            class_summary[(kingdom_list[0], phylum_list[0], "")] +
            class_summary[(kingdom_list[0], phylum_list[0], class_list[1])] +
            class_summary[(kingdom_list[0], phylum_list[0], class_list[2])],
            len(self.taxon),
            f"Incorrect filter by {class_list[2]}."
        )

    def test_filter_order(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        orders = list(filter(lambda x: x != "", pd.unique(df["order"])))
        order_names = ", ".join([f'"{order}"' for order in orders])
        print(f"Orders found: {order_names}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_order(orders)
        self.assertEqual(length_df, len(self.taxon), "Filter by all orders.")
        accepted = df[df["scientificName"] == "Rbaliuycliu"]["acceptedNameUsage"].iloc[0]
        with_order = sum(df["order"].isin(["Rbaliuycliu", "Xlhofowltm", accepted]))
        taxa_id = df[df["scientificName"].isin(["Rbaliuycliu", "Xlhofowltm", accepted])]["taxonID"]
        parents = self.taxon.get_parents(taxa_id)
        parents.update(self.taxon.all_synonyms(parents))
        parents = sum(df["taxonID"].isin(parents))
        print("Filtering by orders: Rbaliuycliu, Xlhofowltm", file=sys.stderr)
        print(f"Accepted orders: Rbaliuycliu, {accepted}", file=sys.stderr)
        self.taxon.filter_by_order(["Rbaliuycliu", "Xlhofowltm"])
        print(f"Expected: with order {with_order} and parents {parents}", file=sys.stderr)
        self.assertEqual(with_order + parents, len(self.taxon), "Incorrect filter.")

    def test_filter_family(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        families = list(filter(lambda x: x != "", pd.unique(df["family"])))
        family_names = ", ".join([f'"{family}"' for family in families])
        print(f"Families found: {family_names}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_family(families)
        self.assertEqual(length_df, len(self.taxon), "Filter by all families.")
        accepted = df[df["scientificName"] == "Dxaougdpy"]["acceptedNameUsage"].iloc[0]
        with_family = sum(df["family"].isin(["Dxaougdpy", "Kvtgqwfmy", accepted]))
        taxa_id = df[df["scientificName"].isin(["Dxaougdpy", "Kvtgqwfmy", accepted])]["taxonID"]
        parents = self.taxon.get_parents(taxa_id)
        parents.update(self.taxon.all_synonyms(parents))
        parents = sum(df["taxonID"].isin(parents))
        print("Filtering by family: Dxaougdpy, Kvtgqwfmy", file=sys.stderr)
        print(f"Accepted families: Kvtgqwfmy, {accepted}", file=sys.stderr)
        self.taxon.filter_by_family(["Dxaougdpy", "Kvtgqwfmy"])
        print(f"Expected: with family {with_family} and parents {parents}", file=sys.stderr)
        self.assertEqual(with_family + parents, len(self.taxon), "Incorrect filter.")

    def test_filter_genus(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        genera = list(filter(lambda x: x != "", pd.unique(df["genus"])))
        genus_names = ", ".join([f'"{genus}"' for genus in genera])
        print(f"Genera found: {genus_names}", file=sys.stderr)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        self.taxon.filter_by_genus(genera)
        self.assertEqual(length_df, len(self.taxon), "Filter by all genera.")
        accepted = df[df["scientificName"] == "Hbqrtfopjuh"]["acceptedNameUsage"].iloc[0]
        with_genus = sum(df["genus"].isin(["Hbqrtfopjuh", "Vbpjkmfqd", accepted]))
        taxa_id = df[df["scientificName"].isin(["Hbqrtfopjuh", "Vbpjkmfqd", accepted])]["taxonID"]
        parents = self.taxon.get_parents(taxa_id)
        parents.update(self.taxon.all_synonyms(parents))
        parents = sum(df["taxonID"].isin(parents))
        print("Filtering by genus: Hbqrtfopjuh, Vbpjkmfqd", file=sys.stderr)
        print(f"Accepted genera: Vbpjkmfqd, {accepted}", file=sys.stderr)
        self.taxon.filter_by_genus(["Hbqrtfopjuh", "Vbpjkmfqd"])
        print(f"Expected: with genus {with_genus} and parents {parents}", file=sys.stderr)
        self.assertEqual(with_genus + parents, len(self.taxon), "Incorrect filter.")

    def test_filter_species(self):
        self.read_pandas()
        df = self.taxon.pandas
        length_df = len(df)
        self.assertEqual(length_df, len(self.taxon), "Original length of dataframe.")
        species_synonym = "Hqmjhacvb (Azvoxtzhwueu) gupfjmnf"
        variety = "Rtfkiaicpdng obzninluz var. cebwyzcqoy Glhnskwn"
        cultivar = "Rtfkiaicpdng (Abifwvxqn) gurqtwpof f. prczacpvtdtu 'xzhgezqpaorp'"
        synonyms = set()
        species_row = df[df["scientificName"] == species_synonym].iloc[0]
        accepted = species_row["acceptedNameUsageID"]
        synonyms.add(accepted)
        synonyms.add(species_row["taxonID"])
        first_parents = self.taxon.get_parents([accepted])
        print(f"For {species_synonym} expected {len(first_parents)} parents, accepted and synonym", file=sys.stderr)
        variety_id = df[df["scientificName"] == variety]["taxonID"].iloc[0]
        second_parents = self.taxon.get_parents([variety_id])
        synonyms.add(variety_id)
        print(f"For {variety} expected {len(second_parents)} parents and self", file=sys.stderr)
        cultivar_id = df[df["scientificName"] == cultivar]["taxonID"].iloc[0]
        third_parents = self.taxon.get_parents([cultivar_id])
        synonyms.add(cultivar_id)
        print(f"For {cultivar} expected {len(third_parents)} parents", file=sys.stderr)
        synonyms.update(self.taxon.all_synonyms(
            list(synonyms.copy()) +
            list(first_parents) +
            list(second_parents) +
            list(third_parents)
        ))
        other_synonyms = synonyms.difference({species_synonym, variety, cultivar})
        other_synonyms = other_synonyms.difference(set(first_parents))
        other_synonyms = other_synonyms.difference(set(second_parents))
        other_synonyms = other_synonyms.difference(set(third_parents))
        print(f"Synonyms found: {len(other_synonyms)}", file=sys.stderr)
        print(f"Total {len(synonyms)}", file=sys.stderr)
        self.taxon.filter_by_species([species_synonym, variety, cultivar])
        self.assertEqual(
            len(synonyms),
            len(self.taxon),
            "Filter by all genera."
        )

    def test_filter_phylum_exception(self):
        super().__test_filter_phylum_exception__()

    def test_none(self):
        super().__test_none__()

    def test_merge(self):
        super().__test_merge__()

    def test_missing_field(self):
        self.assertRaises(
            AssertionError,
            Taxon.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
</core>
            """
        )

    def test_field_twice(self):
        self.assertRaises(
            AssertionError,
            Taxon.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
    <field index="2" term=""/>
    <field index="3" term=""/>
    <field index="4" term=""/>
</core>
            """
        )

    def test_parse_invalid(self):
        self.assertRaises(
            AssertionError,
            Taxon.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            Taxon.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )

    def test_set_pandas(self):
        self.read_pandas()
        df = self.taxon.pandas
        self.assertEqual(163460, len(self.taxon), "Data incorrectly read.")
        self.assertEqual(163460, len(df), "DataFrame incorrectly read.")
        df = df[0:100]
        self.taxon.pandas = df
        self.assertEqual(100, len(df), "DataFrame incorrectly set.")
        self.assertEqual(100, len(self.taxon), "Data incorrectly set.")

    def test_write_file(self):
        self.read_pandas()
        plain_text = self.taxon.write_file()
        self.maxDiff = None
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon.txt"), "r", encoding="utf-8") as file:
            for expected, actual in zip(file.read().split("\n"), plain_text.split("\n")):
                self.assertEqual(
                    expected,
                    actual,
                    "File written incorrectly."
                )

    def test_read_lazy(self):
        self.read_pandas(lazy=True)
        # Difference between local and GitHub Action, it appears to be polar related
        self.assertLessEqual(
            163459, len(self.taxon), "Data incorrectly read."
        )

    def test_close(self):
        with tempfile.NamedTemporaryFile(delete=True) as file:
            temp_folder = os.path.dirname(file.name)
            temp_files = os.listdir(temp_folder)
            temp_files.remove(os.path.basename(file.name))
        self.read_pandas(lazy=True)
        self.assertTrue(self.taxon.is_lazy(), "`lazy` did not set.")
        self.taxon.close()
        self.assertCountEqual(temp_files, os.listdir(temp_folder), "File was not deleted.")

    def test_set_core_field(self):
        self.__test_set_core_field__()

    def test_set_primary_key(self):
        self.__test_set_primary_key__()

    def test_sql_table(self):
        self.__test_sql_table__()

    @patch('builtins.__import__', side_effect=import_mock_fuzzy)
    def test_fuzzy_exception(self, mock_import):
        self.__test_fuzzy_exception__()


if __name__ == '__main__':
    unittest.main()
