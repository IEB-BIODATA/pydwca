import os.path
import unittest
from typing import Tuple, Dict

from lxml import etree as et

from dwca.classes import Taxon
from dwca.terms import DWCLanguage, TaxonID
from test_dwca.test_dwca_no_pandas import orig_import
from test_xml.test_xml import TestXML
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestTaxonCommon(TestXML):
    @staticmethod
    def read_xml(path: str) -> Tuple[Dict, str, str]:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        base_file = et.fromstring(content)
        nmap = base_file.nsmap
        xml_file = base_file.find("core", namespaces=base_file.nsmap)
        text = et.tostring(xml_file, pretty_print=True).decode("utf-8")
        return nmap, xml_file, text

    def setUp(self) -> None:
        self.nmap, self.taxon_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        self.taxon = None
        return

    def read_pandas(self, lazy: bool = False):
        self.taxon = Taxon.from_string(self.text)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon.txt"), "rb") as file:
            if lazy:
                self.taxon.read_file("", source_file=file, lazy=lazy, _no_interaction=True)
            else:
                self.taxon.read_file(file.read().decode(encoding="utf-8"), _no_interaction=True)
        return

    def __test_add_field__(self):
        taxon = Taxon.from_string(self.text)
        taxon.add_field(DWCLanguage(index=47, default=Language.ENG))
        self.assertEqual(48, len(taxon.__fields__), "Fields not set")
        self.text = self.text.replace(
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>""",
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>
    <field index="47" default="eng" term="http://purl.org/dc/elements/1.1/language"/>""")
        self.assertEqualTree(et.fromstring(self.text), taxon.to_element(), "Error on element conversion with new field")

    def __test_add_field_incorrect_index__(self):
        taxon = Taxon.from_string(self.text)
        with self.assertWarnsRegex(UserWarning, "index"):
            taxon.add_field(DWCLanguage(index=3, default=Language.ENG))
        self.assertEqual(48, len(taxon.__fields__), "Fields not set")
        self.text = self.text.replace(
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>""",
            """<field index="46" default="EXAMPLE" term="http://rs.tdwg.org/dwc/terms/institutionCode"/>
    <field index="47" default="eng" term="http://purl.org/dc/elements/1.1/language"/>""")
        self.assertEqualTree(et.fromstring(self.text), taxon.to_element(), "Error on element conversion with new field")

    def __test_parse__(self):
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

    def __test_filter_kingdom_exception__(self):
        taxon = Taxon(0, "file.txt", [])
        self.assertRaisesRegex(
            AssertionError,
            "Kingdom must be in fields",
            taxon.filter_by_kingdom,
            []
        )

    def __test_get_parents__(self):
        self.read_pandas()
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:360"])
        self.assertEqual(11, len(parents_set), "Incorrect number of parents.")
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:366"])
        self.assertEqual(14, len(parents_set), "Incorrect number of parents.")
        parents_set = self.taxon.get_parents(["urn:lsid:example.org:taxname:360", "urn:lsid:example.org:taxname:366"])
        self.assertEqual(14, len(parents_set), "Incorrect number of parents.")

    def __test_get_incorrect_parent__(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        with self.assertWarnsRegex(RuntimeWarning, taxa_id):
            missing = self.taxon.get_parents([taxa_id])
            self.assertEqual(0, len(missing), "Parent found of invalid taxon id")

    def __test_get_synonyms__(self):
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

    def __test_get_synonyms_names__(self):
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

    def __test_get_incorrect_synonyms__(self):
        self.read_pandas()
        taxa_id = "urn:lsid:example.org:taxname:300000"
        with self.assertWarnsRegex(RuntimeWarning, "urn:lsid:example.org:taxname:300000"):
            synonyms = self.taxon.all_synonyms([taxa_id])
            self.assertEqual(0, len(synonyms), "Found something of false taxon id.")

    def __test_filter_phylum_exception__(self):
        taxon = Taxon(0, "file.txt", [])
        self.assertRaisesRegex(
            AssertionError,
            "Phylum must be in fields",
            taxon.filter_by_phylum,
            []
        )

    def __test_fuzzy_exception__(self):
        self.read_pandas()
        self.assertRaisesRegex(
            ImportError,
            "Install rapidfuzz to use this feature.",
            self.taxon.filter_by_species,
            [],
            fuzzy_threshold=90
        )

    def __test_none__(self):
        self.assertIsNone(Taxon.parse(None, {}), "Object parsed from nothing")

    def __test_merge__(self):
        _, xml_file_1, text_1 = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "dataset1_meta.xml"))
        _, xml_file_2, text_2 = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "dataset2_meta.xml"))
        taxon1 = Taxon.from_string(text_1)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon1.txt"), "r", encoding="utf-8") as taxa_file:
            taxon1.read_file(taxa_file.read())
        taxon2 = Taxon.from_string(text_2)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon2.txt"), "r", encoding="utf-8") as taxa_file:
            taxon2.read_file(taxa_file.read())
        merged_taxon = Taxon.merge(taxon1, taxon2)
        self.assertEqual(len(taxon1) + len(taxon2), len(merged_taxon), "Incorrect merged of taxa files.")
        self.assertCountEqual(
            merged_taxon.fields,
            taxon1.fields,
            "Incorrect number of fields"
        )
        self.assertCountEqual(
            merged_taxon.fields,
            taxon2.fields,
            "Incorrect number of fields"
        )

    def __test_set_core_field__(self):
        self.read_pandas()
        self.assertRaisesRegex(
            AttributeError,
            "Core",
            self.taxon.set_core_field,
            TaxonID(0)
        )

    def __test_set_primary_key__(self):
        self.read_pandas()
        self.assertRaisesRegex(
            AttributeError,
            "Core",
            self.taxon.set_primary_key,
            "Taxon"
        )

    def __test_sql_table__(self):
        self.read_pandas()
        self.assertEqual(self.normalize_sql("""
        CREATE TABLE "Taxon" (
            "taxonID" VARCHAR,
            "scientificNameID" VARCHAR,
            "acceptedNameUsageID" VARCHAR,
            "parentNameUsageID" VARCHAR,
            "namePublishedInID" VARCHAR,
            "originalNameUsageID" VARCHAR,
            "nameAccordingToID" VARCHAR,
            "taxonConceptID" VARCHAR,
            "scientificName" VARCHAR,
            "acceptedNameUsage" VARCHAR,
            "parentNameUsage" VARCHAR,
            "namePublishedIn" VARCHAR,
            "originalNameUsage" VARCHAR,
            "nameAccordingTo" VARCHAR,
            "namePublishedInYear" INTEGER,
            "higherClassification" VARCHAR,
            "kingdom" VARCHAR,
            "phylum" VARCHAR,
            "class" VARCHAR,
            "order" VARCHAR,
            "superfamily" VARCHAR,
            "family" VARCHAR,
            "subfamily" VARCHAR,
            "tribe" VARCHAR,
            "subtribe" VARCHAR,
            "genus" VARCHAR,
            "genericName" VARCHAR,
            "subgenus" VARCHAR,
            "infragenericEpithet" VARCHAR,
            "specificEpithet" VARCHAR,
            "infraspecificEpithet" VARCHAR,
            "cultivarEpithet" VARCHAR,
            "taxonRank" VARCHAR,
            "verbatimTaxonRank" VARCHAR,
            "scientificNameAuthorship" VARCHAR,
            "vernacularName" VARCHAR,
            "nomenclaturalCode" VARCHAR,
            "taxonomicStatus" VARCHAR,
            "nomenclaturalStatus" VARCHAR,
            "taxonRemarks" VARCHAR,
            "modified" VARCHAR,
            "bibliographicCitation" VARCHAR,
            "references" VARCHAR,
            "license" VARCHAR,
            "rightsHolder" VARCHAR,
            "datasetName" VARCHAR,
            "institutionCode" VARCHAR,
            PRIMARY KEY ("taxonID")
        );
        """), self.normalize_sql(self.taxon.sql_table), "Wrong SQL table.")


if __name__ == '__main__':
    unittest.main()
