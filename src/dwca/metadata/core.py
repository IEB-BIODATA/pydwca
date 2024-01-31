from __future__ import annotations

from typing import List, Union, Dict

from lxml import etree as et

from dwca.metadata import DataFile, Field


class Core(DataFile):
    """
    Class representing the data entity upon which records are based

    Parameters
    ----------
    row_type : str
        Type of the on the Darwin Core Standard
    files : str
        File location, in the archive, this is inside the `zip` file
    fields : List[Field]
        A list of the Field (columns) in the Core data entity
    _id : str, int
        Unique identifier for the core entity
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
    PRINCIPAL_TAG = "core"
    """str : Principal tag `"core"`"""

    def __init__(
            self,
            row_type: str,
            files: str,
            fields: List[Field],
            _id: str | int = None,
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
        self.__id__ = int(_id)
        return

    @property
    def id(self) -> int:
        """int: Column to be identified as primary key"""
        return self.__id__

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> Core | None:
        """
        Parse an `lxml.etree.Element` into a Core instance.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nsmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        Core
            A data entity Core instance.
        """
        if element is None:
            return None
        fields = list()
        for field_tree in element.findall("field", namespaces=nsmap):
            field = Field.parse(field_tree, nsmap=nsmap)
            field.__namespace__ = nsmap
            fields.append(field)
        assert len(fields) >= 1, "Core must contain at least one field"
        core = Core(
            element.get("rowType"),
            element.find("files", namespaces=nsmap).find("location", namespaces=nsmap).text,
            fields,
            element.find("id", namespaces=nsmap).get("index", None),
            element.get("encoding", "utf-8"),
            element.get("linesTerminatedBy", "\n"),
            element.get("fieldsTerminatedBy", ","),
            element.get("fieldsEnclosedBy", ""),
            element.get("ignoreHeaderLines", 0)
        )
        core.__namespace__ = nsmap
        return core

    def to_element(self) -> et.Element:
        """
        Generate a XML `Element` instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` instance
        """
        element = super().to_element()
        id_element = self.object_to_element("id")
        id_element.set("index", str(self.__id__))
        element.append(id_element)
        return element
