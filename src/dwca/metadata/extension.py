from __future__ import annotations

from typing import Dict, List, Union

from lxml import etree as et

from dwca.metadata import DataFile, Field
from dwca.xml import XMLObject


class Extension(DataFile):
    """
    Class representing an individual extension entity directly related to the core

    Parameters
    ----------
    row_type : str
        Type of the on the Darwin Core Standard
    files : str
        File location, in the archive, this is inside the `zip` file
    fields : List[Field]
        A list of the Field (columns) in the Core data entity
    core_id : str | int
        Column to be reference to the Core file
    encoding : str, optional
        Encoding of the file location (`files` parameter), default is "utf-8"
    lines_terminated_by : str, optional
        Delimiter of lines on the file, default `"\\\\n"`
    fields_terminated_by : str, optional
        Delimiter of the file (cells) on the file, default `","`
    fields_enclosed_by : str, optional
        Specifies the character used to enclose (mark the start and end of) each field, default empty `""`
    ignore_header_lines : List[int|str] | int | str, optional
        Ignore headers at the start of document, can be one line or a list of them, default 0 (first line)
    """
    PRINCIPAL_TAG = "extension"
    """str: Principal tag `extension`"""

    def __init__(
            self,
            row_type: str,
            files: str,
            fields: List[Field],
            core_id: str | int = None,
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: Union[List[Union[int, str]], int, str] = 0
    ) -> None:
        super().__init__(
            row_type, files, fields,
            encoding, lines_terminated_by,
            fields_terminated_by, fields_enclosed_by,
            ignore_header_lines
        )
        self.__core_id__ = int(core_id)
        return

    @property
    def core_id(self) -> int:
        """int: Column that reference the id of the Core file"""
        return self.__core_id__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> Extension | None:
        """
        Parse an `lxml.etree.Element` into an Extension instance.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        Extension
            A data entity Extension instance.
        """
        if element is None:
            return None
        fields = list()
        for field in element.findall("field", namespaces=nmap):
            fields.append(Field.parse(field, nsmap=nmap))
        assert len(fields) >= 1, "Extension must contain at least one field"
        extension = Extension(
            element.get("rowType"),
            element.find("files", namespaces=nmap).find("location", namespaces=nmap).text,
            fields,
            element.find("coreid", namespaces=nmap).get("index", None),
            element.get("encoding", "utf-8"),
            element.get("linesTerminatedBy", "\n"),
            element.get("fieldsTerminatedBy", ","),
            element.get("fieldsEnclosedBy", ""),
            element.get("ignoreHeaderLines", 0)
        )
        extension.__namespace__ = nmap
        return extension

    def to_element(self) -> et.Element:
        """
        Generate a XML `Element` instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` instance
        """
        element = super().to_element()
        core_elem = self.object_to_element("coreid")
        core_elem.set("index", str(self.core_id))
        element.append(core_elem)
        return element
