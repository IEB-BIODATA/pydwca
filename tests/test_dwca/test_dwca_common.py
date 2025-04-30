import os
import tempfile
import unittest
import zipfile

from dwca.base import DarwinCoreArchive
from dwca.classes import OutsideClass
from dwca.terms import OutsideTerm
from eml import EML
from eml.resources import EMLResource
from eml.types import ResponsibleParty, IndividualName
from test_xml.test_xml import TestXML
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCACommon(TestXML):
    def setUp(self) -> None:
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip"), _no_interaction=True
        )
        return

    def __test_minimal__(self):
        minimal_dwca = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "minimal.zip")
        )
        self.assertIsNone(minimal_dwca.metadata, "Metadata file generated from nowhere.")
        self.assertIsNone(minimal_dwca.metadata_filename, "Metadata file (name) generated from nowhere.")
        self.assertEqual(0, len(minimal_dwca.extensions), "Extension from nowhere.")
        self.assertEqual("minimal_core.txt", minimal_dwca.core.filename, "Wrong filename in core.")
        minimal_dwca.core = OutsideClass(0, "http://www.example.org/minimalCore", "minimal_core.txt", [
            OutsideTerm(0, "http://www.example.org/minimalTerm")
        ])

    def __test_attributes__(self):
        self.assertIsNotNone(self.object.metadata, "Doesn't have metadata")
        self.assertEqual("eml.xml", self.object.metadata_filename, "Wrong file name of metadata")
        self.assertEqual(3, len(self.object.extensions), "Missing or wrong number of extensions")
        self.assertEqual("taxon.txt", self.object.core.filename, "Wrong filename in Core")
        self.assertEqual("Core:"
                         "\n\tclass: http://rs.tdwg.org/dwc/terms/Taxon"
                         "\n\tfilename: taxon.txt"
                         "\n\tcontent: 163460 entries", str(self.object.core), "Wrong string of core")
        self.assertCountEqual(
            ["speciesprofile.txt", "reference.txt", "identification.txt"],
            [extension.filename for extension in self.object.extensions],
            "Extension not read"
        )
        self.assertEqual("Extension:"
                         "\n\tclass: http://rs.gbif.org/terms/1.0/SpeciesProfile"
                         "\n\tfilename: speciesprofile.txt"
                         "\n\tcontent: 153621 entries", str(self.object.extensions[0]),
                         "Wrong string of extension (species profile)")
        self.assertEqual("Extension:"
                         "\n\tclass: http://rs.gbif.org/terms/1.0/Reference"
                         "\n\tfilename: reference.txt"
                         "\n\tcontent: 98518 entries", str(self.object.extensions[1]),
                         "Wrong string of extension (reference)")
        self.assertEqual("Extension:"
                         "\n\tclass: http://rs.tdwg.org/dwc/terms/Identification"
                         "\n\tfilename: identification.txt"
                         "\n\tcontent: 7617 entries", str(self.object.extensions[2]),
                         "Wrong string of extension (identification)")
        for ext in self.object.extensions:
            self.assertEqual(
                "http://rs.tdwg.org/dwc/terms/taxonID",
                ext.fields[0],
                f"Core id not set in extension {ext.uri}"
            )
        self.assertEqual(Language.ENG, self.object.language, "Wrong language")

    def __test_merge__(self):
        dataset1 = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "dataset_1.zip"), _no_interaction=True
        )
        dataset2 = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "dataset_2.zip"), _no_interaction=True
        )
        original_expected = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "merged_dataset.zip"), _no_interaction=True
        )
        metadata = EML(
            package_id="merge_data",
            system="http://gbif.org",
            resource_type=EMLResource.DATASET
        )
        metadata.initialize_resource(
            "Merged Dataset",
            ResponsibleParty(
                individual_name=IndividualName("Doe", "John")
            ),
            contact=[ResponsibleParty(
                individual_name=IndividualName("Doe", "Jane")
            )],
        )
        actual_12 = DarwinCoreArchive.merge(
            dataset1, dataset2, eml=metadata
        )
        actual_21 = DarwinCoreArchive.merge(
            dataset2, dataset1, eml=metadata
        )
        actual_121 = DarwinCoreArchive.merge(
            actual_12, dataset1, eml=metadata
        )
        actual_112 = DarwinCoreArchive.merge(
            dataset1, actual_12, eml=metadata
        )
        new_expected = DarwinCoreArchive.merge(
            original_expected, dataset1, eml=metadata
        )
        for actual, expected, name in [
            (actual_12, original_expected, "1 + 2"),
            (actual_21, original_expected, "2 + 1"),
            (actual_121, new_expected, "1 + 2 + 1"),
            (actual_112, new_expected, "1 + 1 + 2"),
        ]:
            self.assertEqualTree(
                actual.metadata.to_element(),
                expected.metadata.to_element(),
                f"Incorrect EML set ({name})"
            )
            self.assertEqual(
                len(expected.core), len(actual.core), f"Wrong number of values on core ({name})"
            )
            self.assertEqual(len(expected.extensions), len(actual.extensions), f"Not the same extensions ({name})")
            for exp_ext, act_ext in zip(expected.extensions, actual.extensions):
                self.assertEqual(
                    len(exp_ext), len(act_ext), f"Wrong number of values on extension: {act_ext} ({name})"
                )
            self.assertDictEqual(
                expected.dataset_metadata,
                actual.dataset_metadata,
                f"Different metadata of datasets ({name})"
            )
            with tempfile.NamedTemporaryFile("wb") as file:
                actual.to_file(file.name)
                with zipfile.ZipFile(file.name, "r") as zip_file:
                    self.assertEqual(5 + len(actual.dataset_metadata), len(zip_file.namelist()), "Error writing DwC-A file with metadata.")
                    datasets = ["eml.xml"]
                    for dataset in actual.dataset_metadata.keys():
                        if dataset != "metadata":
                            datasets.append("dataset/" + dataset + ".xml")
                    self.assertCountEqual(
                        ['meta.xml', 'taxon.txt', 'reference.txt', 'extension1.txt', 'extension2.txt'] + datasets,
                        zip_file.namelist(),
                        "Incorrect file saved"
                    )


if __name__ == '__main__':
    unittest.main()
