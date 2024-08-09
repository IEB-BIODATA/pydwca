import os
import tempfile
import unittest
import zipfile

from dwca.base import DarwinCoreArchive
from eml import EML
from eml.resources import EMLResource
from eml.types import ResponsibleParty, IndividualName
from test_xml.test_xml import TestXML
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCACommon(TestXML):
    def setUp(self) -> None:
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        return

    def __test_attributes__(self):
        self.assertIsNotNone(self.object.metadata, "Doesn't have metadata")
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
        self.assertEqual(Language.ENG, self.object.language, "Wrong language")

    def __test_merge__(self):
        dataset1 = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "dataset_1.zip")
        )
        dataset2 = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "dataset_2.zip")
        )
        expected = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "merged_dataset.zip")
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
        actual = DarwinCoreArchive.merge(
            dataset1, dataset2, eml=metadata
        )
        self.assertEqualTree(
            actual.metadata.to_element(),
            expected.metadata.to_element(),
            "Incorrect EML set"
        )
        self.assertEqual(
            len(expected.core), len(actual.core), f"Wrong number of values on core"
        )
        self.assertEqual(len(expected.extensions), len(actual.extensions), "Not the same extensions")
        for exp_ext, act_ext in zip(expected.extensions, actual.extensions):
            self.assertEqual(
                len(exp_ext), len(act_ext), f"Wrong number of values on extension: {act_ext}"
            )
        self.assertDictEqual(
            expected.dataset_metadata,
            actual.dataset_metadata,
            "Different metadata of datasets"
        )


if __name__ == '__main__':
    unittest.main()
