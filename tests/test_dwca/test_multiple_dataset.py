import os
import unittest

from dwca import DarwinCoreArchive
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


if __name__ == '__main__':
    unittest.main()
