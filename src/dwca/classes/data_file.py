from __future__ import annotations

from abc import ABC
from typing import List, Union, Dict, Type
from warnings import warn

from lxml import etree as et

from dwca.terms import Field, DWCType, DWCModified, DWCLanguage, DWCLicense, DWCRightsHolder, DWCAccessRights, \
    DWCBibliographicCitation, DWCReferences, DWCInstitution, DWCCollection, DWCDataset, DWCInstitutionCode, \
    DWCCollectionCode, DWCDatasetName, DWCOwnerInstitutionCode, DWCBasisOfRecord, DWCInformationWithheld, \
    DWCDataGeneralizations, DWCDynamicProperties, OutsideTerm
from dwca.xml import XMLObject


class DataFile(XMLObject, ABC):
    """
    Abstract class representing the class of data represented by each row in a data entity.

    Parameters
    ----------
    _id : int
        Unique identifier for the core entity.
    files : str
        File location, in the archive, this is inside the `zip` file.
    fields : List[Field]
        A list of the Field (columns) in the Core data entity.
    encoding : str, optional
        Encoding of the file location (`files` parameter), default is "utf-8".
    lines_terminated_by : str, optional
        Delimiter of lines on the file, default `"\\\\n"`.
    fields_terminated_by : str, optional
        Delimiter of the file (cells) on the file, default `","`.
    fields_enclosed_by : str, optional
        Specifies the character used to enclose (mark the start and end of) each field, default empty `""`.
    ignore_header_lines : List[int|str] | int | str, optional
        Ignore headers at the start of document, can be one line or a list of them, default 0 (first line).
    """
    URI = "http://rs.tdwg.org/dwc/terms/"
    """str: Unified Resource Identifier (URI) for the term identifying the class of data."""
    __field_class__ = [
        DWCType, DWCModified, DWCLanguage, DWCLicense, DWCRightsHolder,
        DWCAccessRights, DWCBibliographicCitation, DWCReferences,
        DWCInstitution, DWCCollection, DWCDataset, DWCInstitutionCode,
        DWCCollectionCode, DWCDatasetName, DWCOwnerInstitutionCode,
        DWCBasisOfRecord, DWCInformationWithheld, DWCDataGeneralizations,
        DWCDynamicProperties,
    ]

    def __init__(
            self, _id: int, files: str,
            fields: List[Field],
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: Union[List[Union[int, str]], int, str] = 0,
            _principal_tag: str = "core",
    ) -> None:
        super().__init__()
        self.__id__ = _id
        self.__files__ = files
        self.__fields__ = fields
        self.__encoding__ = encoding
        self.__lines_end__ = lines_terminated_by
        self.__fields_end__ = fields_terminated_by
        self.__fields_enclosed__ = fields_enclosed_by
        if isinstance(ignore_header_lines, List):
            self.__ignore_header_lines__ = [int(i) for i in ignore_header_lines]
        else:
            self.__ignore_header__ = [int(ignore_header_lines)]
        self.PRINCIPAL_TAG = _principal_tag
        return

    @property
    def id(self) -> int:
        """int: Column to be identified as primary key"""
        return self.__id__

    @property
    def uri(self) -> str:
        """str: Unified Resource Identifier (URI) for the term."""
        return self.URI

    @property
    def filename(self) -> str:
        """str: Filename of the Data File entity"""
        return self.__files__

    def set_tag(self, tag: str) -> None:
        """
        Set tag for the XML element to generate.

        Parameters
        ----------
        tag : str
            The principal tag of the XML.

        Returns
        -------
        None
        """
        self.PRINCIPAL_TAG = tag
        return

    @classmethod
    def get_term_class(cls, element: et.Element) -> Type[Field]:
        """
        Extract the Python ``class`` term from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element instance.

        Returns
        -------
        Type[Field]
            The Python ``class`` representing the term name.
        """
        for field_class in cls.__field_class__:
            if element.get("term") == field_class.URI:
                return field_class
        warn(f"{element.get('term')} not in expected namespace. "
             f"Some functionalities may not be available.")
        return OutsideTerm

    @classmethod
    def parse_kwargs(cls, element: et.Element, nmap: Dict) -> Dict:
        """
        Parse an `lxml.etree.Element` into the DataFile parameters.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        Dict
            The Parameters of any DataFile.
        """
        fields = list()
        for field_tree in element.findall("field", namespaces=nmap):
            fields.append(cls.get_term_class(field_tree).parse(field_tree, nmap))
        assert len(fields) >= 1, "A Data File must contain at least one field"
        element_id = element.find("id", nmap)
        try:
            _id = int(element_id.get("index"))
        except AttributeError:
            element_id = element.find("coreid", nmap)
            _id = int(element_id.get("index"))
        return {
            "_id": _id,
            "files": element.find("files", namespaces=nmap).find("location", namespaces=nmap).text,
            "fields": fields,
            "encoding": element.get("encoding", "utf-8"),
            "lines_terminated_by": element.get("linesTerminatedBy", "\n"),
            "fields_terminated_by": element.get("fieldsTerminatedBy", ","),
            "fields_enclosed_by": element.get("fieldsEnclosedBy", ""),
            "ignore_header_lines": element.get("ignoreHeaderLines", 0),
        }

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> DataFile | None:
        """
        Parse an `lxml.etree.Element` into a concrete DataFile object.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        DataFile
            An instance of a concrete DataFile class.
        """
        if element is None:
            return None
        kwargs = cls.parse_kwargs(element, nmap)
        data_file = cls(**kwargs)
        data_file.__namespace__ = nmap
        return data_file

    def to_element(self) -> et.Element:
        """
        Generate a XML `Element` instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` instance
        """
        element = super().to_element()
        element.set("rowType", self.uri)
        element.set("encoding", self.__encoding__)
        element.set("linesTerminatedBy", self.__lines_end__)
        element.set("fieldsTerminatedBy", self.__fields_end__)
        element.set("fieldsEnclosedBy", self.__fields_enclosed__)
        element.set("ignoreHeaderLines", ",".join([str(ignore) for ignore in self.__ignore_header__]))
        if self.PRINCIPAL_TAG == "core":
            element_id = self.object_to_element("id")
        else:  # self.PRINCIPAL_TAG == "extension"
            element_id = self.object_to_element("coreid")
        element_id.set("index", str(self.id))
        element.append(element_id)
        files = self.object_to_element("files")
        location = self.object_to_element("location")
        files.append(location)
        element.append(files)
        for field in self.__fields__:
            field_element = field.to_element()
            element.append(field_element)
        return element

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Overwrite due to different possible tags.

        Parameters
        ----------
        tag : str
            Actual tag.
        nmap : Dict
            Namespace.

        Returns
        -------
        None
        """
        pass
