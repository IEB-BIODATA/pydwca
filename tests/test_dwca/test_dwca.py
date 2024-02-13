import os
import tempfile
import unittest
import zipfile

from dwca import DarwinCoreArchive
from dwca.utils import Language


class TestDWCA(unittest.TestCase):
    def setUp(self) -> None:
        self.object = DarwinCoreArchive.from_archive(os.path.join("example_data", "IRMNG_genera_DwCA.zip"))
        return

    def test_attributes(self):
        self.assertTrue(self.object.has_metadata(), "Doesn't have metadata")
        self.assertEqual(3, len(self.object.extensions), "Missing or wrong number of extensions")
        self.assertEqual("taxon.txt", self.object.core.filename, "Wrong filename in Core")
        self.assertCountEqual(
            ["speciesprofile.txt", "reference.txt", "identifier.txt"],
            [extension.filename for extension in self.object.extensions],
            "Extension not read"
        )
        self.assertEqual(
            "The Interim Register of Marine and Nonmarine Genera", self.object.title, "Wrong title"
        )
        self.assertEqual(
            "The Interim Register of Marine and Nonmarine Genera [eng]",
            str(self.object),
            "Wrong representation"
        )
        self.assertEqual(
            "<Darwin Core Archive (The Interim Register of Marine and Nonmarine Genera [eng])>",
            repr(self.object),
            "Wrong representation"
        )
        self.assertEqual(Language.ENG, self.object.language, "Wrong language")

    def test_new_simple(self):
        darwin_core = DarwinCoreArchive("Example", language="eng")
        with tempfile.NamedTemporaryFile("w") as archive_file:
            darwin_core.to_file(archive_file.name)
            archive_zip = zipfile.ZipFile(archive_file.name, "r")
            self.assertEqual(1, len(archive_zip.filelist), "Wrong number of files written")
            self.assertEqual("meta.xml", archive_zip.filelist[0].filename, "Wrong number of files written")
            self.assertFalse(darwin_core.has_metadata(), "Metadata from nothing")
            archive_zip.close()

    def test_new_eml(self):
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
