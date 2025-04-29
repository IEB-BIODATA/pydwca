import os
import tempfile
import unittest
import zipfile

from dwca.base import DarwinCoreArchive
from eml import EML
from eml.resources import EMLResource
from eml.types import ResponsibleParty, IndividualName
from test_dwca.test_dwca_common import TestDWCACommon

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCA(TestDWCACommon):
    def test_minimal(self):
        super().__test_minimal__()

    def test_attributes(self):
        super().__test_attributes__()

    def test_merge(self):
        super().__test_merge__()

    def test_read_lazy(self):
        lazy_dwca = DarwinCoreArchive.from_file(os.path.join(PATH, os.pardir, "example_data", "example_archive.zip"), lazy=True, _no_interaction=True)
        self.assertEqual(
            0, len(lazy_dwca.core.__entries__), "Entries populated in core."
        )
        self.assertNotEqual(
            0, len(lazy_dwca.core), "Laziness do not load length in core."
        )
        for extension in lazy_dwca.extensions:
            self.assertEqual(
                0, len(extension.__entries__), f"Entries populated in extension {extension.uri}."
            )
            self.assertNotEqual(
                0, len(extension), f"Laziness do not load length in extension {extension.uri}."
            )

    def test_as_pandas(self):
        df = self.object.core.as_pandas(_no_interaction=True)
        self.assertEqual(163460, len(df), "Wrong number of rows")
        self.assertEqual(len(self.object.core.__fields__), len(df.columns), "Wrong number of fields")
        for extension, rows in zip(self.object.extensions, [153621, 98518, 7617]):
            df = extension.as_pandas(_no_interaction=True)
            self.assertEqual(rows, len(df), f"Wrong number of rows at {extension.__class__.__name__}")
            self.assertEqual(len(extension.__fields__), len(df.columns), "Wrong number of fields")

    def test_set_pandas_core(self):
        df = self.object.core.as_pandas(_no_interaction=True)
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

    def test_set_eml_new(self):
        new_dwca = DarwinCoreArchive("Empty Darwin Core")
        self.assertIsNone(
            new_dwca.metadata,
            "Wrong metadata generated",
        )
        new_dwca.set_eml(EML("test_id", "example.org", EMLResource.DATASET))
        eml = new_dwca.metadata
        self.assertIsInstance(
            eml, EML, "Wrong metadata generated"
        )
        self.assertEqual(
            "test_id", eml.package_id, "Wrong EML id"
        )

    def test_set_eml_replace(self):
        self.assertIsNotNone(
            self.object.metadata,
            "Wrong metadata generated",
        )
        self.object.set_eml(EML("test_id", "example.org", EMLResource.DATASET))
        eml = self.object.metadata
        self.assertIsInstance(
            eml, EML, "Wrong metadata generated"
        )
        self.assertEqual(
            "test_id", eml.package_id, "Wrong EML id"
        )

    def test_to_file(self):
        with tempfile.NamedTemporaryFile("wb") as file:
            self.object.to_file(file.name, _no_interaction=True)
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
            empty_dwca.to_file(file.name, _no_interaction=True)
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
            meta_dwca.to_file(file.name, _no_interaction=True)
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
