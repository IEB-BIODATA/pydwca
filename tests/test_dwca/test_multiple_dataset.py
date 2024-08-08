import os
import tempfile
import unittest
import zipfile

from dwca import DarwinCoreArchive
from eml import EML
from eml.resources import EMLResource
from eml.types import ResponsibleParty, IndividualName
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestMultipleDataset(TestXML):

    def test_unique_dataset(self):
        dwc = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        self.assertEqual(1, len(dwc.dataset_metadata), "Incorrect number of metadata for unique dataset.")
        self.assertEqual(
            dwc.metadata.to_xml(),
            dwc.dataset_metadata["metadata"].to_xml(),
            "Difference between the main metadata and metadata of datasets."
        )

    def test_multiple_dataset(self):
        dwc = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "merged_dataset.zip")
        )
        self.assertEqual(3, len(dwc.dataset_metadata), "Incorrect number of metadata.")
        self.assertEqual(
            dwc.metadata.to_xml(),
            dwc.dataset_metadata["metadata"].to_xml(),
            "Difference between the main metadata and metadata of datasets."
        )
        self.assertEqual(
            "dataset_1", dwc.dataset_metadata["dataset_1"].package_id,
            "Incorrect `dataset_1` package_id"
        )
        self.assertEqual(
            "Example for Darwin Core Archive 1", dwc.dataset_metadata["dataset_1"].resource.title,
            "Incorrect `dataset_1` title"
        )
        self.assertEqual(
            "dataset_2", dwc.dataset_metadata["dataset_2"].package_id,
            "Incorrect `dataset_2` package_id"
        )
        self.assertEqual(
            "Example for Darwin Core Archive 2", dwc.dataset_metadata["dataset_2"].resource.title,
            "Incorrect `dataset_2` title"
        )

    def test_write_multiple_dataset(self):
        dwc = DarwinCoreArchive("test")
        dwc.generate_eml("eml.xml")
        dwc.metadata.initialize_resource(
            "A Multiple Dataset Test",
            ResponsibleParty(individual_name=IndividualName("Doe", "Example")),
            contact=[ResponsibleParty(individual_name=IndividualName(
                "Doe", "Jane"
            ))]
        )
        dwc.dataset_metadata["dataset_1"] = EML(
            "another_dataset", "http://gbif.org", EMLResource.DATASET
        )
        dwc.dataset_metadata["dataset_1"].initialize_resource(
            "First extra dataset",
            ResponsibleParty(individual_name=IndividualName("Doe", "Example")),
            contact=[ResponsibleParty(individual_name=IndividualName(
                "Doe", "Jane"
            ))]
        )
        dwc.dataset_metadata["dataset_2"] = EML(
            "one_more_dataset", "http://gbif.org", EMLResource.DATASET
        )
        dwc.dataset_metadata["dataset_2"].initialize_resource(
            "Second extra dataset",
            ResponsibleParty(individual_name=IndividualName("Doe", "Example")),
            contact=[ResponsibleParty(individual_name=IndividualName(
                "Doe", "Jane"
            ))]
        )
        with tempfile.NamedTemporaryFile("wb") as file:
            dwc.to_file(file.name)
            with zipfile.ZipFile(file.name, "r") as zipped_file:
                presented_files = zipped_file.namelist()
                self.assertEqual(4, len(presented_files), "Wrong number of files on dataset")
                self.assertCountEqual(
                    ["dataset/dataset_1.xml", "dataset/dataset_2.xml"],
                    list(filter(lambda x: "dataset/" in x, presented_files)),
                    f"Expected datasets not present: {presented_files}"
                )
                dataset1 = EML.from_string(zipped_file.read("dataset/dataset_1.xml").decode())
                self.assertEqualTree(dwc.dataset_metadata["dataset_1"].to_element(), dataset1.to_element(), "Wrong parsed dataset 1")
                dataset2 = EML.from_string(zipped_file.read("dataset/dataset_2.xml").decode())
                self.assertEqualTree(dwc.dataset_metadata["dataset_2"].to_element(), dataset2.to_element(), "Wrong parsed dataset 2")


if __name__ == '__main__':
    unittest.main()
