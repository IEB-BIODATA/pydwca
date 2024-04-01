from typing import List, Union

from dwca.classes import DataFile, DataFileType
from dwca.terms import ResourceRelationshipID, ResourceID, RelationshipOfResourceID, RelatedResourceID, \
    RelationshipOfResource, RelationshipAccordingTo, RelationshipEstablishedDate, RelationshipRemarks, Field


class ResourceRelationship(DataFile):
    """
    A relationship of one Resource to another.

    Parameters
    ----------
    _id : int
        Unique identifier for the core entity.
    files : str
        File location, in the archive, this is inside the `zip` file.
    fields : List[Field]
        A list of the Field (columns) in the Core data entity.
    data_file_type: DataFileType
        The Data File Type in the Darwin Core Archive.
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
    URI = DataFile.URI + "ResourceRelationship"
    __field_class__ = DataFile.__field_class__ + [
        ResourceRelationshipID, ResourceID,
        RelationshipOfResourceID, RelatedResourceID,
        RelationshipOfResource, RelationshipAccordingTo,
        RelationshipEstablishedDate, RelationshipRemarks,
    ]

    def __init__(
            self, _id: int, files: str,
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
        return
