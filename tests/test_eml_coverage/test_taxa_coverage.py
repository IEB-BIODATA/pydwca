import unittest

from lxml import etree as et

from eml.resources.coverage import TaxonomicCoverage
from test_xml.test_xml import TestXML


class MyTestCase(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        '{http://www.w3.org/XML/1998/namespace}lang': 'eng',
    }

    def test_parse(self):
        general_taxonomic_coverage = ("All vascular plants were identified "
                                      "to family or species, mosses and "
                                      "lichens were identified as moss or "
                                      "lichen.")
        text_xml = f"""
<taxonomicCoverage id="" scope="document" system="">
    <taxonomicSystem>
        <classificationSystem>
            <classificationSystemCitation>
                <references>class-system</references>
            </classificationSystemCitation>
        </classificationSystem>
        <identifierName>
            <organizationName>Identifier Organization</organizationName>
        </identifierName>
        <taxonomicProcedures>specimen processing</taxonomicProcedures>
    </taxonomicSystem>
    <generalTaxonomicCoverage>{general_taxonomic_coverage}</generalTaxonomicCoverage>
    <taxonomicClassification>
        <taxonRankName>Kingdom</taxonRankName>
        <taxonRankValue>Viridiplantae</taxonRankValue>
        <commonName>Green Plants</commonName>
        <taxonId provider="https://www.ncbi.nlm.nih.gov/taxonomy">33090</taxonId>
    </taxonomicClassification>
</taxonomicCoverage>
        """
        coverage = TaxonomicCoverage.from_string(text_xml)
        self.assertEqual(
            1, len(coverage.taxonomic_system.classification_system),
            "Error on parsing classification system"
        )
        self.assertEqual(
            "class-system", coverage.taxonomic_system.classification_system[0].citation.id,
            "Error on parse classification system citation"
        )
        self.assertIsNone(
            coverage.taxonomic_system.classification_system[0].modifications,
            "Error on parse classification system modifications"
        )
        self.assertEqual(
            0, len(coverage.taxonomic_system.identification_reference),
            "Identification reference from nowhere"
        )
        self.assertEqual(
            1, len(coverage.taxonomic_system.identifier_name),
            "Error on parsing identifier name"
        )
        self.assertEqual(
            "Identifier Organization", coverage.taxonomic_system.identifier_name[0].organization_name,
            "Error on parsing identifier name (organization name)"
        )
        self.assertEqual(
            "specimen processing", coverage.taxonomic_system.procedures,
            "Error on parsing taxonomic procedures"
        )
        self.assertEqual(
            general_taxonomic_coverage,
            coverage.general_coverage,
            "Error on parsing general taxonomic coverage"
        )
        self.assertEqual(
            1, len(coverage.classification),
            "Error on parsing classification system"
        )
        self.assertEqual("Kingdom", coverage.classification[0].rank_name, "Error on parsing taxonomic rank name")
        self.assertEqual("Viridiplantae", coverage.classification[0].rank_value, "Error on parsing taxonomic rank value")
        self.assertEqual(1, len(coverage.classification[0].common_name), "Error on parsing common name")
        self.assertEqual("Green Plants", coverage.classification[0].common_name[0], "Error on parsing common name")
        self.assertEqual(1, len(coverage.classification[0].taxon_id), "Error on parsing taxon id")
        self.assertEqual(
            33090,
            coverage.classification[0].taxon_id[0],
            "Error on parsing taxon id"
        )
        self.assertEqual(
            "https://www.ncbi.nlm.nih.gov/taxonomy",
            coverage.classification[0].taxon_id[0].provider,
            "Error on parsing taxon id"
        )
        self.assertEqual(
            0, len(coverage.classification[0].classification),
            "Taxonomic classification from nowhere"
        )
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_taxonomic_system(self):
        text_xml = """
<taxonomicSystem>
    <classificationSystem>
        <classificationSystemCitation>
            <references>class-system</references>
        </classificationSystemCitation>
        <classificationSystemModifications>Description of any modifications or exceptions.</classificationSystemModifications>
    </classificationSystem>
    <identificationReference>
        <references>knb.45.3</references>
    </identificationReference>
    <identifierName>
        <organizationName>Identifier Organization</organizationName>
    </identifierName>
    <taxonomicProcedures>specimen processing</taxonomicProcedures>
    <taxonomicCompleteness>materials sent to experts</taxonomicCompleteness>
    <vouchers>
        <specimen>herbarium specimens</specimen>
        <repository>
            <originator>
                <organizationName>Repository Organization</organizationName>
            </originator>
        </repository>
    </vouchers>
</taxonomicSystem>
        """
        taxonomic_system = TaxonomicCoverage.TaxonomicSystem.from_string(text_xml)
        self.assertEqual(
            1, len(taxonomic_system.classification_system),
            "Error on parsing classification system"
        )
        self.assertEqual(
            "class-system", taxonomic_system.classification_system[0].citation.id,
            "Error on parse classification system citation"
        )
        self.assertEqual(
            "Description of any modifications or exceptions.",
            taxonomic_system.classification_system[0].modifications,
            "Error on parse classification system modifications"
        )
        self.assertEqual(
            1, len(taxonomic_system.identification_reference),
            "Error on parsing identification reference"
        )
        self.assertEqual(
            "knb.45.3", taxonomic_system.identification_reference[0].id,
            "Error on parse identification reference"
        )
        self.assertEqual(
            1, len(taxonomic_system.identifier_name),
            "Error on parsing identifier name"
        )
        self.assertEqual(
            "Identifier Organization", taxonomic_system.identifier_name[0].organization_name,
            "Error on parsing identifier name (organization name)"
        )
        self.assertEqual(
            "specimen processing", taxonomic_system.procedures,
            "Error on parsing taxonomic procedures"
        )
        self.assertEqual(
            "materials sent to experts", taxonomic_system.completeness,
            "Error on parsing taxonomic completeness"
        )
        self.assertEqual(
            1, len(taxonomic_system.vouchers),
            "Error on parsing vouchers"
        )
        self.assertEqual(
            "herbarium specimens", taxonomic_system.vouchers[0].specimen,
            "Error on parsing vouchers specimen"
        )
        self.assertEqual(
            1, len(taxonomic_system.vouchers[0].repository),
            "Error on parsing vouchers repository"
        )
        self.assertEqual(
            "Repository Organization", taxonomic_system.vouchers[0].repository[0].organization_name,
            "Error on parsing vouchers repository"
        )
        self.assertEqualTree(et.fromstring(text_xml), taxonomic_system.to_element(), "Error on to element")

    def test_parse_taxonomic_system_invalid(self):
        self.assertRaises(
            ValueError, TaxonomicCoverage.TaxonomicSystem.from_string,
            """
<taxonomicSystem>
    <identificationReference>
        <references>knb.45.3</references>
    </identificationReference>
    <identifierName>
        <organizationName>Identifier Organization</organizationName>
    </identifierName>
    <taxonomicProcedures>specimen processing</taxonomicProcedures>
    <taxonomicCompleteness>materials sent to experts</taxonomicCompleteness>
    <vouchers>
        <specimen>herbarium specimens</specimen>
        <repository>
            <originator>
                <organizationName>Repository Organization</organizationName>
            </originator>
        </repository>
    </vouchers>
</taxonomicSystem>
            """
        )
        self.assertRaises(
            ValueError, TaxonomicCoverage.TaxonomicSystem.from_string,
            """
<taxonomicSystem>
    <classificationSystem>
        <classificationSystemCitation>
            <references>class-system</references>
        </classificationSystemCitation>
        <classificationSystemModifications>Description of any modifications or exceptions.</classificationSystemModifications>
    </classificationSystem>
    <identificationReference>
        <references>knb.45.3</references>
    </identificationReference>
    <taxonomicProcedures>specimen processing</taxonomicProcedures>
    <taxonomicCompleteness>materials sent to experts</taxonomicCompleteness>
    <vouchers>
        <specimen>herbarium specimens</specimen>
        <repository>
            <originator>
                <organizationName>Repository Organization</organizationName>
            </originator>
        </repository>
    </vouchers>
</taxonomicSystem>
            """
        )

    def test_parse_taxonomic_system_none(self):
        self.assertIsNone(TaxonomicCoverage.TaxonomicSystem.parse(None, {}), "Taxonomic System from nowhere")

    def test_parse_taxonomic_classification(self):
        text_xml = """
<taxonomicClassification id="">
    <taxonRankName>Kingdom</taxonRankName>
    <taxonRankValue>Viridiplantae</taxonRankValue>
    <commonName>Green Plants</commonName>
    <taxonId provider="https://www.ncbi.nlm.nih.gov/taxonomy">33090</taxonId>
    <taxonomicClassification>
        <taxonRankName>Phylum</taxonRankName>
        <taxonRankValue>Chlorophyta</taxonRankValue>
        <commonName>Green Algae</commonName>
        <taxonId provider="https://www.ncbi.nlm.nih.gov/taxonomy">3041</taxonId>
    </taxonomicClassification>
</taxonomicClassification>
        """
        taxonomic_classification = TaxonomicCoverage.TaxonomicClassification.from_string(text_xml)
        self.assertEqual("Kingdom", taxonomic_classification.rank_name, "Error on parsing taxonomic rank name")
        self.assertEqual("Viridiplantae", taxonomic_classification.rank_value, "Error on parsing taxonomic rank value")
        self.assertEqual(1, len(taxonomic_classification.common_name), "Error on parsing common name")
        self.assertEqual("Green Plants", taxonomic_classification.common_name[0], "Error on parsing common name")
        self.assertEqual(1, len(taxonomic_classification.taxon_id), "Error on parsing taxon id")
        self.assertEqual(
            33090,
            taxonomic_classification.taxon_id[0],
            "Error on parsing taxon id"
        )
        self.assertEqual(
            "https://www.ncbi.nlm.nih.gov/taxonomy",
            taxonomic_classification.taxon_id[0].provider,
            "Error on parsing taxon id"
        )
        self.assertEqual(
            1, len(taxonomic_classification.classification),
            "Error on parsing taxonomic classification"
        )
        self.assertEqual(
            "Phylum", taxonomic_classification.classification[0].rank_name,
            "Error on parsing taxonomic rank name"
        )
        self.assertEqual(
            "Chlorophyta",
            taxonomic_classification.classification[0].rank_value,
            "Error on parsing taxonomic rank value"
        )
        self.assertEqual(1, len(taxonomic_classification.classification[0].common_name), "Error on parsing common name")
        self.assertEqual("Green Algae", taxonomic_classification.classification[0].common_name[0], "Error on parsing common name")
        self.assertEqual(1, len(taxonomic_classification.classification[0].taxon_id), "Error on parsing taxon id")
        self.assertEqual(
            3041,
            taxonomic_classification.classification[0].taxon_id[0],
            "Error on parsing taxon id"
        )
        self.assertEqual(
            "https://www.ncbi.nlm.nih.gov/taxonomy",
            taxonomic_classification.classification[0].taxon_id[0].provider,
            "Error on parsing taxon id"
        )
        self.assertEqual(
            0, len(taxonomic_classification.classification[0].classification),
            "Taxonomic classification from nowhere"
        )
        self.assertEqualTree(et.fromstring(text_xml), taxonomic_classification.to_element(), "Error on to element")

    def test_parse_taxonomic_classification_none(self):
        self.assertIsNone(
            TaxonomicCoverage.TaxonomicClassification.parse(None, {}),
            "Taxonomic classification from nowhere"
        )

    def test_equal_taxon_id(self):
        example = TaxonomicCoverage.TaxonID(1, "http://gbif.org")
        self.assertEqual(1, example, "Not compare to int")
        same_example = TaxonomicCoverage.TaxonID(1, "http://gbif.org")
        self.assertEqual(example, same_example, "Same dato, not equals")
        other_example = TaxonomicCoverage.TaxonID(1, "http://gbif_alternative.org")
        self.assertNotEqual(example, other_example, "Equal different provider")
        self.assertNotEqual("1", example, "Error on equal implementation")

    def test_parse_invalid(self):
        general_taxonomic_coverage = ("All vascular plants were identified "
                                      "to family or species, mosses and "
                                      "lichens were identified as moss or "
                                      "lichen.")
        text_xml = f"""
<taxonomicCoverage id="" scope="document" system="">
    <taxonomicSystem>
        <classificationSystem>
            <classificationSystemCitation>
                <references>class-system</references>
            </classificationSystemCitation>
        </classificationSystem>
        <identifierName>
            <organizationName>Identifier Organization</organizationName>
        </identifierName>
        <taxonomicProcedures>specimen processing</taxonomicProcedures>
    </taxonomicSystem>
    <generalTaxonomicCoverage>{general_taxonomic_coverage}</generalTaxonomicCoverage>
</taxonomicCoverage>
        """
        self.assertRaises(ValueError, TaxonomicCoverage.from_string, text_xml)

    def test_parse_none(self):
        self.assertIsNone(TaxonomicCoverage.parse(None, {}), "Taxonomic Coverage from nowhere")

    def test_parse_minimum(self):
        text_xml = """
<taxonomicCoverage>
    <taxonomicClassification>
        <taxonRankName>Kingdom</taxonRankName>
        <taxonRankValue>Viridiplantae</taxonRankValue>
        <commonName>Green Plants</commonName>
        <taxonId provider="https://www.ncbi.nlm.nih.gov/taxonomy">33090</taxonId>
    </taxonomicClassification>
</taxonomicCoverage>
        """
        coverage = TaxonomicCoverage.from_string(text_xml)
        self.assertIsNone(coverage.id, "Identifier from nowhere")
        self.assertFalse(coverage.referencing, "Error on parse referencing")
        self.assertIsNone(coverage.taxonomic_system, "Taxonomic System from nowhere")
        self.assertIsNone(coverage.general_coverage, "General coverage from nowhere")
        self.assertEqual(1, len(coverage.classification), "Error on parsing classification")
        self.assertEqual("Kingdom", coverage.classification[0].rank_name, "Error on parsing taxonomic rank name")
        self.assertEqual("Viridiplantae", coverage.classification[0].rank_value, "Error on parsing taxonomic rank value")
        self.assertEqual(1, len(coverage.classification[0].common_name), "Error on parsing common name")
        self.assertEqual("Green Plants", coverage.classification[0].common_name[0], "Error on parsing common name")
        self.assertEqual(1, len(coverage.classification[0].taxon_id), "Error on parsing taxon id")
        self.assertEqual(
            33090,
            coverage.classification[0].taxon_id[0],
            "Error on parsing taxon id"
        )
        self.assertEqual(
            "https://www.ncbi.nlm.nih.gov/taxonomy",
            coverage.classification[0].taxon_id[0].provider,
            "Error on parsing taxon id"
        )
        self.assertEqual(
            0, len(coverage.classification[0].classification),
            "Taxonomic classification from nowhere"
        )
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_referencing(self):
        text_xml = """
<taxonomicCoverage scope="system">
    <references system="http://gbif.org">56</references>
</taxonomicCoverage>
        """
        coverage = TaxonomicCoverage.from_string(text_xml)
        self.assertEqual("56", coverage.id, "Error on parsing id")
        self.assertEqual("http://gbif.org", coverage.references.system, "Error on parsing system of references")
        self.assertTrue(coverage.referencing, "Error on parse referencing")
        self.assertIsNone(coverage.taxonomic_system, "Taxonomic System from nowhere")
        self.assertIsNone(coverage.general_coverage, "General coverage from nowhere")
        self.assertEqual(0, len(coverage.classification), "Classification from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")


if __name__ == '__main__':
    unittest.main()
