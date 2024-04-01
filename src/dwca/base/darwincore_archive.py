from __future__ import annotations

import io
import zipfile
from typing import List, Dict, Type
from warnings import warn

from lxml import etree as et

from dwca.base import DarwinCore
from dwca.classes import DataFile, Occurrence, Organism, MaterialEntity, MaterialSample, Event, Location, \
    GeologicalContext, Identification, Taxon, ResourceRelationship, MeasurementOrFact, ChronometricAge, OutsideClass
from xml_common.utils import Language
from xml_common import XMLObject
from eml import EML
from eml.resources import EMLResource


class DarwinCoreArchive(DarwinCore):
    """
    Represent a Darwin Core Archive file with all its elements.

    Parameters
    ----------
    _id : str, optional
        A unique id for this Darwin Core Archive.
    """
    class Metadata(XMLObject):
        """
        Metadata class of the Darwin Core Archive storing the file name of the archive elements.

        Parameters
        ----------
        metadata : str, optional
            Name of the metadata file (e.g.: eml.xml)
        """
        PRINCIPAL_TAG = "archive"
        """str : Require tag of the metadata"""
        __classes__ = [
            Occurrence, Organism, MaterialEntity, MaterialSample,
            Event, Location, GeologicalContext, Identification,
            Taxon, ResourceRelationship, MeasurementOrFact,
            ChronometricAge,
        ]

        def __init__(self, metadata: str = None) -> None:
            super().__init__()
            self.__metadata__ = metadata
            self.__core__ = None
            self.__extensions__: List[DataFile] = list()
            return

        @classmethod
        def get_dwc_class(cls, element: et.Element) -> Type[DataFile]:
            """
            Extract the row type from an XML element instance.

            Parameters
            ----------
            element : lxml.etree.Element
                XML element instance.

            Returns
            -------
            Type[DataFile]
                The Python ``class`` representing the class term.
            """
            for dwc_class in cls.__classes__:
                if element.get("rowType") == dwc_class.URI:
                    return dwc_class
            warn(f"{element.get('rowType')} not in expected namespace. "
                 f"Some functionalities may not be available.")
            return OutsideClass

        @property
        def core(self) -> DataFile:
            """
            DataFile: Core object representing the data entity upon which records are based on.
            """
            return self.__core__

        @property
        def extensions(self) -> List[DataFile]:
            """
            List[DataFile]: A list of Extension objects representing the entities directly related to the core
            """
            return self.__extensions__

        @property
        def metadata_filename(self) -> str:
            """
            str: Name of the metadata file (e.g.: eml.xml)
            """
            return self.__metadata__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> DarwinCoreArchive.Metadata:
            """
            Parses an `lxml.etree.Element` in a Metadata instance.

            Parameters
            ----------
            element : `lxml.etree.Element`
                XML element to be parsed.
            nmap : Dict
                Namespace prefix:uri.

            Returns
            -------
            Metadata
                New Metadata instance with the data from the element.
            """
            metadata = element.get("metadata", None)
            core_element = element.find(f"{{{nmap[None]}}}core")
            assert core_element.find("id", nmap).get("index") is not None, "Core must have an id"
            core = cls.get_dwc_class(core_element).parse(core_element, nmap=nmap)
            meta = DarwinCoreArchive.Metadata(metadata)
            meta.__core__ = core
            for extension_elem in element.findall(f"{{{nmap[None]}}}extension"):
                assert extension_elem.find("coreid", nmap).get("index") is not None, "Extension must have a coreid"
                extension = cls.get_dwc_class(extension_elem).parse(extension_elem, nmap)
                meta.__extensions__.append(extension)
            meta.__namespace__ = nmap
            return meta

        def to_element(self) -> et.Element:
            """
            Generate an element from a Metadata instance.

            Returns
            -------
            lxml.etree.Element
                XML element from Metadata instance
            """
            element = super().to_element()
            if self.__metadata__ is not None:
                element.set("metadata", self.__metadata__)
            if self.core is not None:
                element.append(self.core.to_element())
            for extension in self.extensions:
                element.append(extension.to_element())
            return element

    def __init__(self, _id: str = None) -> None:
        super().__init__()
        self.__id__ = _id
        self.__meta__ = DarwinCoreArchive.Metadata()
        self.__metadata__ = None
        return

    @property
    def id(self) -> str:
        """str: A unique identifier for this DarwinCoreArchive."""
        return self.__id__

    @property
    def core(self) -> DataFile:
        """DataFile: The file with the core of the archive."""
        return self.__meta__.__core__

    @core.setter
    def core(self, core: DataFile) -> None:
        self.__meta__.__core__ = core
        try:
            df = self.__meta__.__core__.pandas
            for extension in self.extensions:
                ext_df = extension.pandas
                mask = ext_df.iloc[:, extension.id].isin(df.iloc[:, core.id])
                ext_df = ext_df.loc[ext_df[mask].index, :]
                extension.pandas = ext_df
        except ImportError:
            pass
        return

    @property
    def extensions(self) -> List[DataFile]:
        """
        List[DataFile]: A list with the extension of the archive.
        """
        return self.__meta__.__extensions__

    @property
    def metadata(self) -> EML:
        """
        EML: Metadata instance, currently supported EML.
        """
        return self.__metadata__

    @property
    def language(self) -> Language:
        """Language: Language of the Darwin Core Archive register on metadata."""
        return self.metadata.language

    def generate_eml(self, filename: str = "eml.xml") -> None:
        """
        Generate an EML file on the archive

        Parameters
        ----------
        filename : str
            Filename for the EML file to be generated

        Returns
        -------
        None
            Generate an EML object on the archive
        """
        self.__meta__.__metadata__ = filename
        self.__metadata__ = EML(self.id, system="http://gbif.org", resource_type=EMLResource.DATASET)
        return

    @classmethod
    def from_file(cls, path_to_archive: str) -> DarwinCoreArchive:
        """
        Generate a Darwin Core Archive instance from an archive file (`.zip`).

        Parameters
        ----------
        path_to_archive : str
            Path of the archive file.

        Returns
        -------
        DarwinCoreArchive
            Instance of the Darwin Core Archive.
        """
        archive = zipfile.ZipFile(path_to_archive, "r")
        index_file = archive.read("meta.xml")
        metadata = DarwinCoreArchive.Metadata.from_string(index_file.decode(encoding="utf-8"))
        if metadata.metadata_filename is not None:
            metadata_content = archive.read(metadata.metadata_filename)
            try:
                eml = EML.from_string(metadata_content.decode(encoding="utf-8"))
            except ValueError:
                eml = EML.from_string(metadata_content)
            darwin_core = DarwinCoreArchive(_id=eml.package_id)
        else:
            darwin_core = DarwinCoreArchive()
        darwin_core.__meta__ = metadata
        darwin_core.__metadata__ = eml
        core_file = archive.read(darwin_core.core.filename)
        darwin_core.__meta__.__core__.read_file(core_file.decode(encoding=metadata.__core__.__encoding__))
        darwin_core.__meta__.__core__._register_darwin_core_(0, darwin_core)
        for i, extension in enumerate(darwin_core.extensions):
            extension_file = archive.read(extension.filename)
            darwin_core.__meta__.__extensions__[i].read_file(extension_file.decode())
        archive.close()
        return darwin_core

    def to_file(self, path_to_archive: str, encoding: str = "utf-8") -> None:
        """
        Generate a Darwin Core Archive file (`.zip` file) using the information of this instance.

        Parameters
        ----------
        path_to_archive : str
            Path of the archive to generate.
        encoding : str, optional
            Encoding of the corresponding files. Default `"utf-8"`.

        Returns
        -------
        None
            Writes file.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
            zip_file.writestr("meta.xml", self.__metadata__.to_xml().encode(encoding))
        with open(path_to_archive, 'wb') as output_file:
            output_file.write(zip_buffer.getvalue())
        zip_buffer.close()
        return

    def __repr__(self) -> str:
        return f"<Darwin Core Archive ({self})>"

    def __str__(self) -> str:
        return f"{self.id} [Core: {self.core.uri}, Entries: {len(self.core)}]"
