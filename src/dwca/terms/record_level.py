from typing import Any, Dict
import datetime as dt

from dwca.terms import Field
from dwca.utils import Language


class DWCType(Field):
    """
    The nature or genre of the resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/elements/1.1/type"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCModified(Field):
    """
    The most recent date-time on which the resource was changed.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "	http://purl.org/dc/terms/modified"
    TYPE = dt.datetime

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCLanguage(Field):
    """
    A language of the resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/elements/1.1/language"
    TYPE = Language

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCLicense(Field):
    """
    A legal document giving official permission to do something with the resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/terms/license"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCRightsHolder(Field):
    """
    A person or organization owning or managing rights over the resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/terms/rightsHolder"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCAccessRights(Field):
    """
    Information about who can access the resource or an indication of its security status.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/terms/accessRights"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCBibliographicCitation(Field):
    """
    A bibliographic reference for the resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/terms/bibliographicCitation"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCReferences(Field):
    """
    A related resource that is referenced, cited, or otherwise pointed to by the described resource.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://purl.org/dc/terms/references"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCInstitution(Field):
    """
    An identifier for the institution having custody of the object(s) or information referred to in the record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/institutionID"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCCollection(Field):
    """
    An identifier for the collection or dataset from which the record was derived.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/collectionID"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCDataset(Field):
    """
    An identifier for the set of data.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/datasetID"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCInstitutionCode(Field):
    """
    The name (or acronym) in use by the institution having custody of the information referred to in the record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/institutionCode"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCCollectionCode(Field):
    """
    The name, acronym, coden, or initialism identifying the collection or data set from which the record was derived.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/collectionCode"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCDatasetName(Field):
    """
    The name identifying the data set from which the record was derived.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/datasetName"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCOwnerInstitutionCode(Field):
    """
    The name (or acronym) in use by the institution having ownership of the object(s) or information referred to in the record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/ownerInstitutionCode"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCBasisOfRecord(Field):
    """
    The specific nature of the data record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/basisOfRecord"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCInformationWithheld(Field):
    """
    Additional information that exists, but that has not been shared in the given record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/informationWithheld"
    TYPE = str

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCDataGeneralizations(Field):
    """
    Actions taken to make the shared data less specific or complete than in its original form.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/dataGeneralizations"
    TYPE = Any

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class DWCDynamicProperties(Field):
    """
    A list of additional measurements, facts, characteristics, or assertions about the record.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/dynamicProperties"
    TYPE = Dict[str, Any]

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return