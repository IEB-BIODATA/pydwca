from typing import List, Union

from dwca.classes import DataFile
from dwca.terms import MaterialSampleID, Field


class MaterialSample(DataFile):
    """
    A material entity that represents an entity of interest in whole or in part.
    """
    URI = DataFile.URI + 'MaterialSample'
    __field_class__ = DataFile.__field_class__ + [
        MaterialSampleID,
    ]

    def __init__(
            self, _id: int, files: str,
            fields: List[Field],
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: Union[List[Union[int, str]], int, str] = 0,
            _principal_tag: str = "core"
    ) -> None:
        super().__init__(
            _id, files, fields, encoding, lines_terminated_by,
            fields_terminated_by, fields_enclosed_by,
            ignore_header_lines, _principal_tag
        )
        return
