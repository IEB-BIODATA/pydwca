from __future__ import annotations

import io
import zipfile
from copy import deepcopy
from typing import List, Dict, Type
from warnings import warn

from lxml import etree as et

from dwca.base import DarwinCore
from dwca.classes import DataFile, Occurrence, Organism, MaterialEntity, MaterialSample, Event, Location, \
    GeologicalContext, Identification, Taxon, ResourceRelationship, MeasurementOrFact, ChronometricAge, OutsideClass
from eml import EML
from eml.resources import EMLResource
from xml_common import XMLObject
from xml_common.utils import Language, read_string


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
        xmlns = "http://rs.tdwg.org/dwc/text/"
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
            self.__namespace__[None] = self.xmlns
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
            if self.__core__ is not None:
                element.append(self.__core__.to_element())
            for extension in self.__extensions__:
                element.append(extension.to_element())
            return element

    def __init__(self, _id: str = None) -> None:
        super().__init__()
        self.__id__ = _id
        self.__meta__ = DarwinCoreArchive.Metadata()
        self.__metadata__ = None
        self.__dataset_meta__ = {
            "metadata": self.__metadata__
        }
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
                ext_df = extension.as_pandas(_no_interaction=True)
                mask = ext_df.iloc[:, extension.id].isin(df.iloc[:, core.id])
                ext_df = ext_df.loc[ext_df[mask].index, :]
                extension.pandas = ext_df
        except ImportError:
            core_ids = [getattr(entry, core.__fields__[core.id].name) for entry in self.core.__entries__]
            for extension in self.extensions:
                def criteria(entry: DataFile.Entry) -> bool:
                    entry_id = getattr(entry, extension.__fields__[extension.id].name)
                    return entry_id in core_ids
                extension.__entries__ = list(filter(
                    criteria, extension.__entries__
                ))
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
    def metadata_filename(self) -> str:
        """
        str: The filename of the metadata file.
        """
        return self.__meta__.__metadata__

    @property
    def dataset_metadata(self) -> Dict[str, EML]:
        """
        Dict[str, EML]: Metadata instances for each dataset present on DWC-A.
        """
        return self.__dataset_meta__

    @property
    def language(self) -> Language:
        """Language: Language of the Darwin Core Archive register on metadata."""
        return self.metadata.language

    def generate_eml(self, filename: str = "eml.xml") -> None:
        """
        Generate an EML file on the archive.

        Parameters
        ----------
        filename : str
            Filename for the EML file to be generated. Defaults to "eml.xml".
        """
        self.__meta__.__metadata__ = filename
        self.__metadata__ = EML(self.id, system="http://gbif.org", resource_type=EMLResource.DATASET)
        return

    def set_eml(self, eml: EML, filename: str = "eml.xml") -> None:
        """
        Set an EML file in the archive.

        Parameters
        ----------
        eml : EML
            Metadata instance to set.
        filename : str, optional
            Filename for the EML file. Defaults to "eml.xml".
        """
        self.__meta__.__metadata__ = filename
        self.__metadata__ = eml
        return

    @classmethod
    def from_file(cls, path_to_archive: str, lazy: bool = False, _no_interaction: bool = False) -> DarwinCoreArchive:
        """
        Generate a Darwin Core Archive instance from an archive file (`.zip`).

        Parameters
        ----------
        path_to_archive : str
            Path of the archive file.
        lazy : bool, optional
            Read the archive lazy. Default `False`.
        _no_interaction : bool, optional
            Not to show progress bar if library `tqdm` is installed. Default `False`.

        Returns
        -------
        DarwinCoreArchive
            Instance of the Darwin Core Archive.
        """
        archive = zipfile.ZipFile(path_to_archive, "r")
        index_file = archive.read("meta.xml")
        metadata = DarwinCoreArchive.Metadata.from_string(read_string(index_file))
        if metadata.__metadata__ is not None:
            metadata_content = archive.read(metadata.__metadata__)
            eml = EML.from_string(read_string(metadata_content))
            darwin_core = DarwinCoreArchive(_id=eml.package_id)
            darwin_core.__metadata__ = eml
        else:
            darwin_core = DarwinCoreArchive()
        darwin_core.__meta__ = metadata
        if lazy:
            core_file = archive.open(darwin_core.core.filename)
            darwin_core.__meta__.__core__.read_file("", source_file=core_file, lazy=lazy, _no_interaction=_no_interaction)
            core_file.close()
        else:
            core_file = archive.read(darwin_core.core.filename)
            darwin_core.__meta__.__core__.read_file(core_file.decode(encoding=metadata.__core__.__encoding__), _no_interaction=_no_interaction)
        darwin_core.__meta__.__core__._register_darwin_core_(0, darwin_core)
        for i, extension in enumerate(darwin_core.extensions):
            extension.set_core_field(darwin_core.core.__fields__[darwin_core.core.id])
            extension.set_primary_key(darwin_core.core.name)
            if lazy:
                extension_file = archive.open(extension.filename)
                darwin_core.__meta__.__extensions__[i].read_file("", source_file=extension_file, lazy=lazy, _no_interaction=_no_interaction)
                extension_file.close()
            else:
                extension_file = archive.read(extension.filename)
                darwin_core.__meta__.__extensions__[i].read_file(extension_file.decode(), _no_interaction=_no_interaction)
        darwin_core.__dataset_meta__ = {
            "metadata": darwin_core.__metadata__
        }
        for item in archive.namelist():
            if item.startswith("dataset/"):
                if item == "dataset/":
                    continue
                try:
                    dataset_meta = EML.from_string(read_string(archive.read(item)))
                    darwin_core.__dataset_meta__[dataset_meta.package_id] = dataset_meta
                except Exception as e:
                    warn(f"Could not read {item.replace('dataset/', '')}:\n{e}", category=RuntimeWarning)
        archive.close()
        return darwin_core

    def to_file(
            self, path_to_archive: str,
            encoding: str = "utf-8",
            compression: int = zipfile.ZIP_DEFLATED,
            compression_level: int = 6,
            _no_interaction: bool = False,
    ) -> None:
        """
        Generate a Darwin Core Archive file (`.zip` file) using the information of this instance.

        Parameters
        ----------
        path_to_archive : str
            Path of the archive to generate.
        encoding : str, optional
            Encoding of the corresponding files. Default `"utf-8"`.
        compression : int, optional
            The ZIP compression method to use. Default `zipfile.ZIP_DEFLATED`.
        compression_level : int, optional
            Compression level to use when writing files to the archive. Default `6`.
        _no_interaction : bool, optional
            Not to show progress bar if library `tqdm` is installed. Default `False`.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', compression=compression, compresslevel=compression_level) as zip_file:
            zip_file.writestr("meta.xml", self.__meta__.to_xml().encode(encoding))
            if self.metadata is not None:
                zip_file.writestr(self.__meta__.__metadata__, self.__metadata__.to_xml().encode(encoding))
            if self.core is not None:
                zip_file.writestr(self.core.filename, self.core.write_file(_no_interaction=_no_interaction))
            for extension in self.extensions:
                zip_file.writestr(extension.filename, extension.write_file(_no_interaction=_no_interaction))
            for dataset, metadata in self.dataset_metadata.items():
                if dataset != "metadata":
                    zip_file.writestr(f"dataset/{dataset}.xml", metadata.to_xml().encode(encoding))
        with open(path_to_archive, 'wb') as output_file:
            output_file.write(zip_buffer.getvalue())
        zip_buffer.close()
        return

    @classmethod
    def merge(
            cls, first_archive: DarwinCoreArchive,
            second_archive: DarwinCoreArchive,
            _id: str = None, eml: EML = None,
            eml_filename: str = "eml.xml"
    ) -> DarwinCoreArchive:
        merged_dwca = DarwinCoreArchive(_id=_id)
        if eml is not None:
            merged_dwca.__metadata__ = eml
        new_core = first_archive.core.merge(second_archive.core)
        merged_dwca.core = new_core
        first_extensions = [ext.uri for ext in first_archive.extensions]
        second_extensions = [ext.uri for ext in second_archive.extensions]
        for extension in first_archive.extensions:
            try:
                index = second_extensions.index(extension.uri)
                new_extension = extension.merge(second_archive.extensions[index])
                merged_dwca.extensions.append(deepcopy(new_extension))
                del new_extension
            except ValueError:
                merged_dwca.extensions.append(deepcopy(extension))
        for extension in second_archive.extensions:
            if extension.uri not in first_extensions:
                merged_dwca.extensions.append(deepcopy(extension))
        merged_dwca.__metadata__ = eml
        if eml is not None:
            merged_dwca.__meta__.__metadata__ = eml_filename
            merged_dwca.__dataset_meta__["metadata"] = eml
        if first_archive.metadata is not None:
            merged_dwca.__dataset_meta__[first_archive.metadata.package_id] = first_archive.metadata
        if second_archive.metadata is not None:
            merged_dwca.__dataset_meta__[second_archive.metadata.package_id] = second_archive.metadata
        for name, metadata in first_archive.dataset_metadata.items():
            if name != "metadata":
                merged_dwca.__dataset_meta__[name] = metadata
        for name, metadata in second_archive.dataset_metadata.items():
            if name != "metadata":
                merged_dwca.__dataset_meta__[name] = metadata
        return merged_dwca

    def __repr__(self) -> str:
        return f"<Darwin Core Archive ({self})>"

    def __str__(self) -> str:
        return f"{self.id} [Core: {self.core.uri}, Entries: {len(self.core)}]"
