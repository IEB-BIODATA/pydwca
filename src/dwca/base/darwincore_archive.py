from __future__ import annotations

import io
import zipfile
from typing import List, Dict

from lxml import etree as et

from dwca.base import DarwinCore
from dwca.classes import DataFile, get_dwc_class
from dwca.xml import XMLObject
from eml.base import EML
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
        def __init__(self, metadata: str = None) -> None:
            super().__init__()
            self.__metadata__ = metadata
            self.__core__ = None
            self.__extensions__: List[DataFile] = list()
            return

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
            core = get_dwc_class(core_element).parse(core_element, nmap=nmap)
            core.set_tag("core")
            meta = DarwinCoreArchive.Metadata(metadata)
            meta.__core__ = core
            for extension_elem in element.findall(f"{{{nmap[None]}}}extension"):
                assert extension_elem.find("coreid", nmap).get("index") is not None, "Extension must have a coreid"
                extension = get_dwc_class(extension_elem).parse(extension_elem, nmap)
                extension.set_tag("extension")
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
        if metadata.metadata_file is not None:
            eml = EML.from_string(archive.read(metadata.metadata_filename).decode(encoding="utf-8"))
            darwin_core = DarwinCoreArchive(_id=eml.package_id)
        else:
            darwin_core = DarwinCoreArchive()
        darwin_core.__meta__ = metadata
        darwin_core.__metadata__ = eml
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
        return f"{self.id} [Core: {self.core}]"
