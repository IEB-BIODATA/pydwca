import os
import unittest

from dwca.classes import OutsideClass, Taxon
from test_dwca_classes.test_outside_class_common import TestOutsideCommon
from test_dwca_classes.test_taxon_common import TestTaxonCommon
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDataFile(TestXML):
    def test_assertion(self):
        _, xml_file_1, text_1 = TestTaxonCommon.read_xml(os.path.join(
            PATH, os.pardir, "example_data", "dataset1_meta.xml"
        ))
        xml_file_2, text_2 = TestOutsideCommon.read_xml(os.path.join(
            PATH, os.pardir, "example_data", "dataset1_meta.xml"
        ))
        taxon1 = Taxon.from_string(text_1)
        with open(os.path.join(PATH, os.pardir, "example_data", "taxon1.txt"), "r", encoding="utf-8") as taxa_file:
            taxon1.read_file(taxa_file.read(), _no_interaction=True)
        extension = OutsideClass.from_string(text_2)
        with open(
                os.path.join(PATH, os.pardir, "example_data", "extension_example1.txt"),
                "r", encoding="utf-8"
        ) as file:
            extension.read_file(file.read(), _no_interaction=True)
        self.assertRaises(AssertionError, taxon1.merge, extension)
        self.assertRaises(AssertionError, extension.merge, taxon1)


if __name__ == '__main__':
    unittest.main()
