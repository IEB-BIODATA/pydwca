import datetime as dt
from typing import Union

from datetime_interval import Interval

from dwca.terms import Field


class ResourceRelationshipID(Field):
    """
    An identifier for an instance of relationship between one resource (the subject) and another (the object).
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/resourceRelationshipID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ResourceID(Field):
    """
    An identifier for the resource that is the subject of the relationship.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/resourceID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RelationshipOfResourceID(Field):
    """
    An identifier for the relationship type.

    An identifier for the relationship type
    (predicate) that connects the subject
    identified by Resource ID to its object
    identified by Related Resource ID.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relationshipOfResourceID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class RelatedResourceID(Field):
    """
    An identifier for a related resource.

    The object, rather than the subject of the relationship.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relatedResourceID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RelationshipOfResource(Field):
    """
    The relationship of the subject to the object.

    The subject identified by ``Resource ID``. The object
    identified by ``Related Resource ID``.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relationshipOfResource"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class RelationshipAccordingTo(Field):
    """
    The source establishing the relationship between the two resources.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relationshipAccordingTo"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RelationshipEstablishedDate(Field):
    """
    The date-time on which the relationship between the two resources was established.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate"
    TYPE = Union[dt.datetime, Interval]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class RelationshipRemarks(Field):
    """
    Comments or notes about the relationship between the two resources.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/relationshipRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
