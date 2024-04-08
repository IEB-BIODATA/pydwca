import os
import sys
import unittest

from dwca.base import DarwinCoreArchive
from xml_common.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCA(unittest.TestCase):
    def setUp(self) -> None:
        sys.modules['pandas'] = None
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        return

    def tearDown(self) -> None:
        del sys.modules['pandas']
        return

    def test_set_core(self):
        core = self.object.core
        self.assertEqual(163460, len(core), "Wrong number of entries")
        core.__entries__ = core.__entries__[0:100]
        self.assertEqual(100, len(core), "Core has not been shorted to 100 entries")
        self.object.core = core
        self.assertEqual(100, len(self.object.core), "Core has not been shorted on DwC-A object")
        for extension in self.object.extensions:
            self.assertGreaterEqual(100, len(extension), f"Extension {extension.uri} has not been shorted")

    def test_attributes(self):
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


if __name__ == '__main__':
    unittest.main()
