from __future__ import annotations

from typing import List, Union, Dict

from lxml import etree as et

from dwca.classes import DataFile, DataFileType
from dwca.terms import Field


class OutsideClass(DataFile):
    """
    Classes defined outside the Darwin Core specifications.

    Parameters
    ----------
    _id : int
        Unique identifier for the core entity.
    uri : str
        URI of the term.
    files : str
        File location, in the archive, this is inside the `zip` file.
    data_file_type: DataFileType
        The Data File Type in the Darwin Core Archive.
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
    ignore_header_lines : int, optional
        Ignore headers at the start of document, can be one line or a list of them, default 0 (first line).
    """
    def __init__(
            self, _id: int, uri: str,
            files: str,
            fields: List[Field],
            data_file_type: DataFileType = DataFileType.CORE,
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: int = 0,
    ) -> None:
        super().__init__(
            _id, files, fields, data_file_type, encoding,
            lines_terminated_by, fields_terminated_by,
            fields_enclosed_by, ignore_header_lines,
        )
        self.URI = uri
        return

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> OutsideClass | None:
        """
        Parse an `lxml.etree.Element` into an OutsideClass object.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        OutsideClass
            An instance of OutsideClass.
        """
        if element is None:
            return None
        kwargs = cls.parse_kwargs(element, nmap)
        kwargs["uri"] = element.get("rowType")
        outside = OutsideClass(**kwargs)
        outside.__namespace__ = nmap
        return outside
