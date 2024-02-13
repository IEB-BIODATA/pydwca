from __future__ import annotations

import io
import zipfile
from typing import List

from dwca.metadata import Metadata, Core, Extension
from dwca.utils import Language
from eml.base import EML


class DarwinCoreArchive:
    """
    Base class of this package. Represent a Darwin Core Archive file with all its elements.

    Parameters
    ----------
    title : str
        Title of the database in the Darwin Core Archive.
    language : str, optional
        Short name of language, default `"eng"`.
    """
    def __init__(self, title: str = "", language: str = "eng", __eml__: EML = None) -> None:
        super().__init__()
        self.__title__ = title
        self.__metadata__ = Metadata()
        for lang in Language:
            if lang.name.lower() == language.lower():
                self.__lang__ = lang
        self.__eml__ = __eml__
        return

    @property
    def title(self) -> str:
        """str: The title of the Darwin Core Archive, equivalent to the title of the dataset in the EML metadata."""
        return self.__title__

    @property
    def language(self) -> Language:
        """Language: Language of the Darwin Core."""
        return self.__lang__

    @property
    def core(self) -> Core:
        """Core: The file with the core of the archive."""
        return self.__metadata__.__core__

    @property
    def extensions(self) -> List[Extension]:
        """
        List[Extension] : A list with the extension of the archive.
        """
        return self.__metadata__.__extensions__

    def has_metadata(self) -> bool:
        """
        If the archive has a metadata file (eml.xml).

        Returns
        -------
        bool
            True if the archive has metadata, False otherwise.
        """
        return self.__metadata__.metadata_filename is not None

    def generate_eml(self, filename: str) -> None:
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
        self.__metadata__.__metadata__ = filename
        self.__eml__ = EML("example", self.title, self.language.name)
        return

    @classmethod
    def from_archive(cls, path_to_archive: str) -> DarwinCoreArchive:
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
        metadata = Metadata.from_string(index_file.decode(encoding="utf-8"))
        if metadata.metadata_filename is not None:
            eml = EML.from_string(archive.read(metadata.metadata_filename).decode(encoding="utf-8"))
            darwin_core = DarwinCoreArchive(eml.title, eml.language.name, __eml__=eml)
        else:
            darwin_core = DarwinCoreArchive("")
        darwin_core.__metadata__ = metadata
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
        return f"<Darwin Core Archive ({self.__title__} [{self.__lang__.name.lower()}])>"

    def __str__(self) -> str:
        return f"{self.__title__} [{self.__lang__.name.lower()}]"
