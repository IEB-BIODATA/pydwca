from __future__ import annotations

from enum import Enum
from typing import List, Union, Tuple

from dwca.terms import Field
from xml_common.utils import EstablishmentMeans


class OccurrenceID(Field):
    """
    An identifier for the Occurrence (as opposed to a particular digital record of the Occurrence).

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/occurrenceID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class CatalogNumber(Field):
    """
    An identifier (preferably unique) for the record within the data set or collection.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/catalogNumber"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RecordNumber(Field):
    """
    An identifier given to the Occurrence at the time it was recorded.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/recordNumber"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RecordedBy(Field):
    """
    A list of names of people, groups, or organizations responsible for recording the original Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/recordedBy"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RecordedByID(Field):
    """
    A list of the globally unique identifier for the responsible for recording the original Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/recordedByID"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class IndividualCount(Field):
    """
    The number of individuals present at the time of the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/individualCount"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OrganismQuantity(Field):
    """
    A number or enumeration value for the quantity of Organisms.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/organismQuantity"
    TYPE = Union[int, float, str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OrganismQuantityType(Field):
    """
    The type of quantification system used for the quantity of Organisms.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/organismQuantityType"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OccurrenceSex(Field):
    """
    The sex of the biological individual(s) represented in the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/sex"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class LifeStage(Field):
    """
    The age class or life stage of the Organism(s) at the time the Occurrence was recorded.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/lifeStage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class ReproductiveCondition(Field):
    """
    The reproductive condition of the biological individual(s) represented in the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/reproductiveCondition"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Caste(Field):
    """
    Categorisation of individuals for eusocial species (including some mammals and arthropods).

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/caste"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Behavior(Field):
    """
    The behavior shown by the subject at the time the Occurrence was recorded.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/behavior"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Vitality(Field):
    """
    An indication of whether an Organism was alive or dead at the time of collection or observation.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/vitality"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCEstablishmentMeans(Field):
    """
    Statement about whether an Organism has been introduced through the activity of modern humans.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/establishmentMeans"
    TYPE = EstablishmentMeans

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCDegreeOfEstablishment(Field):
    """
    The degree to which an Organism survives, reproduces, and expands its range at the given place and time.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/degreeOfEstablishment"
    TYPE = str  # TODO: Create DOE Enum following https://dwc.tdwg.org/doe/

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class Pathway(Field):
    """
    The process by which an Organism came to be in a given place at a given time.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/pathway"
    TYPE = str  # TODO: Create DOE Enum following  http://rs.tdwg.org/dwc/doc/pw/.

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class GeoreferenceVerificationStatus(Field):
    """
    A categorical description of which the georeference has been verified for the Location of the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/georeferenceVerificationStatus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class OccurrenceStatus(Field):
    """
    A statement about the presence or absence of a Taxon at a Location.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    class DefaultStatus(Enum):
        PRESENT = 1
        ABSENCE = 0

    URI = "http://rs.tdwg.org/dwc/terms/occurrenceStatus"
    TYPE = DefaultStatus

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return

    def format(self, value: str) -> DefaultStatus:
        """
        Format value to DefaultStatus.

        Parameters
        ----------
        value : str
            Value to be formatted as a DefaultStatus.

        Returns
        -------
        DefaultStatus
            Value as a DefaultStatus Enum object.
        """
        if value.lower() == "present":
            return OccurrenceStatus.DefaultStatus.PRESENT
        elif value.lower() == "absent":
            return OccurrenceStatus.DefaultStatus.ABSENCE
        else:
            raise ValueError("Unknown status: {}".format(value))

    def unformat(self, value: DefaultStatus) -> str:
        """
        Encode value from DefaultStatus to a standard string.

        Parameters
        ----------
        value : DefaultStatus
            An instance of DefaultStatus to be represented as a string.

        Returns
        -------
        str
            String representation of DefaultStatus.
        """
        return value.name.lower()


class AssociatedMedia(Field):
    """
    A list of identifiers (publication, global unique identifier, URI) of media associated with the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/associatedMedia"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class AssociatedOccurrences(Field):
    """
    A list of identifiers of other Occurrence records and their associations to this Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/associatedOccurrences"
    TYPE = List[Tuple[str, str]]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class AssociatedReferences(Field):
    """
    A list of identifiers of literature associated with the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/associatedReferences"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class AssociatedTaxa(Field):
    """
    A list of identifiers or names of Taxon records and the associations of this Occurrence to each of them.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/associatedTaxa"
    TYPE = List[Tuple[str, str]]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OtherCatalogNumbers(Field):
    """
    A list of previous or alternate catalog numbers for the same Occurrence.v

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/otherCatalogNumbers"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OccurrenceRemarks(Field):
    """
    Comments or notes about the Occurrence.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/occurrenceRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
