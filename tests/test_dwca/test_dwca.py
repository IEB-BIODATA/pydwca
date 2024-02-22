import os
import tempfile
import unittest
import zipfile

from dwca.base import DarwinCoreArchive
from dwca.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCA(unittest.TestCase):
    def setUp(self) -> None:
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        return

    def test_attributes(self):
        self.assertIsNotNone(self.object.metadata, "Doesn't have metadata")
        self.assertEqual(3, len(self.object.extensions), "Missing or wrong number of extensions")
        self.assertEqual("taxon.txt", self.object.core.filename, "Wrong filename in Core")
        print([(type(field), field) for field in self.object.core.__fields__])
        self.assertCountEqual(
            ["speciesprofile.txt", "reference.txt", "identifier.txt"],
            [extension.filename for extension in self.object.extensions],
            "Extension not read"
        )
        self.assertEqual(Language.ENG, self.object.language, "Wrong language")

    def no_test_new_simple(self):
        darwin_core = DarwinCoreArchive("Example", language="eng")
        with tempfile.NamedTemporaryFile("w") as archive_file:
            darwin_core.to_file(archive_file.name)
            archive_zip = zipfile.ZipFile(archive_file.name, "r")
            self.assertEqual(1, len(archive_zip.filelist), "Wrong number of files written")
            self.assertEqual("meta.xml", archive_zip.filelist[0].filename, "Wrong number of files written")
            self.assertFalse(darwin_core.has_metadata(), "Metadata from nothing")
            archive_zip.close()

    def no_test_new_eml(self):
        darwin_core = DarwinCoreArchive("Example", language="eng")
        darwin_core.generate_eml("example_eml.xml")
        with tempfile.NamedTemporaryFile("w") as archive_file:
            darwin_core.to_file(archive_file.name)
            archive_zip = zipfile.ZipFile(archive_file.name, "r")
            self.assertEqual(1, len(archive_zip.filelist), "Wrong number of files written")
            self.assertEqual("meta.xml", archive_zip.filelist[0].filename, "Wrong number of files written")
            self.assertTrue(darwin_core.has_metadata(), "Metadata not generated")
            archive_zip.close()


if __name__ == '__main__':
    unittest.main()
