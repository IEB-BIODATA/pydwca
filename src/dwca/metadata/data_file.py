from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, List, Dict

from lxml import etree as et

from dwca.metadata import Field
from dwca.xml import XMLObject


class DataFile(XMLObject, ABC):
    """
    Abstract Class representing a data entity

    Parameters
    ----------
    row_type : str
        Type of the on the Darwin Core Standard
    files : str
        File location, in the archive, this is inside the `zip` file
    fields : List[Field]
        A list of the Field (columns) in the Core data entity
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
    def __init__(
            self,
            row_type: str,
            files: str,
            fields: List[Field],
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: Union[List[Union[int, str]], int, str] = 0
    ) -> None:
        super().__init__()
        self.__row_type_url__ = row_type
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
        return

    @property
    def filename(self) -> str:
        """str: Filename of the Data File entity"""
        return self.__files__

    def to_element(self) -> et.Element:
        """
        Generate a XML `Element` instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` instance
        """
        element = super().to_element()
        element.set("rowType", self.__row_type_url__)
        element.set("encoding", self.__encoding__)
        element.set("linesTerminatedBy", self.__lines_end__)
        element.set("fieldsTerminatedBy", self.__fields_end__)
        element.set("fieldsEnclosedBy", self.__fields_enclosed__)
        element.set("ignoreHeaderLines", ",".join([str(ignore) for ignore in self.__ignore_header__]))
        files = self.object_to_element("files")
        location = self.object_to_element("location")
        files.append(location)
        element.append(files)
        for field in self.__fields__:
            field_element = field.to_element()
            element.append(field_element)
        return element
