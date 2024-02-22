from __future__ import annotations

from typing import List, Union

from dwca.classes import DataFile
from dwca.terms import Field, OccurrenceID, CatalogNumber, RecordNumber, RecordedBy, RecordedByID, IndividualCount, \
    OrganismQuantity, OrganismQuantityType, OccurrenceSex, LifeStage, ReproductiveCondition, Caste, Behavior, \
    Vitality, DWCEstablishmentMeans, DWCDegreeOfEstablishment, Pathway, GeoreferenceVerificationStatus, \
    OccurrenceStatus, AssociatedMedia, AssociatedOccurrences, AssociatedReferences, AssociatedTaxa, \
    OtherCatalogNumbers, OccurrenceRemarks


class Occurrence(DataFile):
    """
    An existence of an organism at a particular place at a particular time.

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
    URI = DataFile.URI + "Occurrence"
    __field_class__ = DataFile.__field_class__ + [
        OccurrenceID, CatalogNumber, RecordNumber, RecordedBy,
        RecordedByID, IndividualCount, OrganismQuantity,
        OrganismQuantityType, OccurrenceSex, LifeStage,
        ReproductiveCondition, Caste, Behavior, Vitality,
        DWCEstablishmentMeans, DWCDegreeOfEstablishment,
        Pathway, GeoreferenceVerificationStatus, OccurrenceStatus,
        AssociatedMedia, AssociatedOccurrences, AssociatedReferences,
        AssociatedTaxa, OtherCatalogNumbers, OccurrenceRemarks
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
