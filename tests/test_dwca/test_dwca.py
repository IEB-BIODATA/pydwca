import os
import tempfile
import unittest
import zipfile

from dwca.base import DarwinCoreArchive
from eml import EML
from eml.types import ResponsibleParty, IndividualName
from xml_common.utils import Language

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

    def test_as_pandas(self):
        df = self.object.core.as_pandas()
        self.assertEqual(163460, len(df), "Wrong number of rows")
        self.assertEqual(len(self.object.core.__fields__), len(df.columns), "Wrong number of fields")
        for extension, rows in zip(self.object.extensions, [153621, 98518, 7617]):
            df = extension.as_pandas()
            self.assertEqual(rows, len(df), f"Wrong number of rows at {extension.__class__.__name__}")
            self.assertEqual(len(extension.__fields__), len(df.columns), "Wrong number of fields")

    def test_set_pandas_core(self):
        df = self.object.core.as_pandas()
        self.assertEqual(163460, len(df), "Wrong number of rows")
        df = df[0:100]
        self.assertEqual(100, len(df), "Wrong number of rows set")
        self.object.core.pandas = df
        self.assertEqual(100, len(self.object.core), "Wrong number of rows set")
        for extension in self.object.extensions:
            self.assertGreaterEqual(100, len(extension), f"Wrong number of rows set at {extension.__class__.__name__}")

    def test_generate_eml(self):
        new_dwca = DarwinCoreArchive("Empty Darwin Core")
        new_dwca.generate_eml()
        eml = new_dwca.metadata
        self.assertIsInstance(
            eml, EML, "Wrong metadata generated"
        )
        self.assertEqual(
            "Empty Darwin Core", eml.package_id, "Wrong EML id"
        )

    def test_to_file(self):
        with tempfile.NamedTemporaryFile("wb") as file:
            self.object.to_file(file.name)
            with zipfile.ZipFile(file.name, "r") as zip_file:
                self.assertEqual(6, len(zip_file.namelist()), "Error writing DwC-A file.")
                self.assertCountEqual(
                    ["meta.xml", "taxon.txt", "identification.txt",
                     "reference.txt", "speciesprofile.txt", "eml.xml"],
                    zip_file.namelist(),
                    "Incorrect file saved"
                )
        empty_dwca = DarwinCoreArchive("Empty One")
        with tempfile.NamedTemporaryFile("wb") as file:
            empty_dwca.to_file(file.name)
            with zipfile.ZipFile(file.name, "r") as zip_file:
                self.assertEqual(1, len(zip_file.namelist()), "Error writing empty DwC-A file.")
                self.assertCountEqual(
                    ["meta.xml"],
                    zip_file.namelist(),
                    "Incorrect file saved"
                )
        meta_dwca = DarwinCoreArchive("With EML")
        meta_dwca.generate_eml()
        meta_dwca.metadata.initialize_resource(
            "Example for Darwin Core Archive",
            ResponsibleParty(
                _id="1",
                individual_name=IndividualName(
                    last_name="Doe",
                    first_name="Jane",
                    salutation="Ms"
                )
            ),
            contact=[ResponsibleParty(_id="1", referencing=True)]
        )
        with tempfile.NamedTemporaryFile("wb") as file:
            meta_dwca.to_file(file.name)
            with zipfile.ZipFile(file.name, "r") as zip_file:
                self.assertEqual(2, len(zip_file.namelist()), "Error writing DwC-A file with metadata.")
                self.assertCountEqual(
                    ["meta.xml", "eml.xml"],
                    zip_file.namelist(),
                    "Incorrect file saved"
                )

    def test_str(self):
        self.assertEqual(
            "Example Package [Core: http://rs.tdwg.org/dwc/terms/Taxon, Entries: 163460]",
            str(self.object),
            "Error on DwCA string."
        )

    def test_repr(self):
        self.assertEqual(
            "<Darwin Core Archive (Example Package [Core: http://rs.tdwg.org/dwc/terms/Taxon, Entries: 163460])>",
            repr(self.object),
            "Error on DwCA string representation."
        )


if __name__ == '__main__':
    unittest.main()
