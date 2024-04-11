import os.path
import sys
import unittest

import pandas as pd
from lxml import etree as et

from dwca.classes import Taxon
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestTaxon(TestXML):
    def setUp(self) -> None:
        with open(os.path.join(PATH, os.pardir, "example_data", "meta.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        self.taxon_xml = base_file.find("core", namespaces=base_file.nsmap)
        self.text = et.tostring(self.taxon_xml, pretty_print=True).decode("utf-8")
        self.taxon = None
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

    def test_filter_kingdom_exception(self):
        taxon = Taxon(0, "file.txt", [])
        self.assertRaisesRegex(
            AssertionError,
            "Kingdom must be in fields",
            taxon.filter_by_kingdom,
            []
        )

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
        two_synonyms = self.taxon.all_synonyms(["urn:lsid:example.org:taxname:10000", "urn:lsid:example.org:taxname:100005"])
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

    def test_filter_phylum_exception(self):
        taxon = Taxon(0, "file.txt", [])
        self.assertRaisesRegex(
            AssertionError,
            "Phylum must be in fields",
            taxon.filter_by_phylum,
            []
        )

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

    def test_none(self):
        self.assertIsNone(Taxon.parse(None, {}), "Object parsed from nothing")

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


if __name__ == '__main__':
    unittest.main()
