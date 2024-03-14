import datetime as dt
from typing import List

from dwca.terms import Field


class ChronometricAgeID(Field):
    """
    An identifier for the set of information associated with a ChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimChronometricAge(Field):
    """
    The verbatim age for a specimen, whether reported by a dating assay, associated references, or legacy information.

    For example, this could be the radiocarbon age
    as given in an AMS dating report. This could
    also be simply what is reported as the age of
    a specimen in legacy collections data.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/verbatimChronometricAge"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeProtocol(Field):
    """
    A description of or reference to the methods used to determine the chronometric age.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeProtocol"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class UncalibratedChronometricAge(Field):
    """
    The output of a dating assay before it is calibrated into an age using a specific conversion protocol.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/uncalibratedChronometricAge"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeConversionProtocol(Field):
    """
    The method used for converting the UncalibratedChronometricAge into a chronometric age in years.

    As captured in the ``EarliestChronometricAge``, ``EarliestChronometricAgeReferenceSystem``,
    ``LatestChronometricAge``, and ``LatestChronometricAgeReferenceSystem`` fields.
    For example, calibration of conventional radiocarbon age or the
    currently accepted age range of a cultural or geological period.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeConversionProtocol"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestChronometricAge(Field):
    """
    The maximum/earliest/oldest possible age of a specimen as determined by a dating method.

    The expected unit for this field is years. This field, if populated,
    must have an associated ``EarliestChronometricAgeReferenceSystem``.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/earliestChronometricAge"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestChronometricAgeReferenceSystem(Field):
    """
    The reference system associated with the EarliestChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/chrono/terms/earliestChronometricAgeReferenceSystem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class LatestChronometricAge(Field):
    """
    The minimum/latest/youngest possible age of a specimen as determined by a dating method.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/latestChronometricAge"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestChronometricAgeReferenceSystem(Field):
    """
    The reference system associated with the LatestChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/chrono/terms/latestChronometricAgeReferenceSystem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class ChronometricAgeUncertaintyInYears(Field):
    """
    The temporal uncertainty of the EarliestChronometricAge and LatestChronometicAge in years.

    The expected unit for this field is years. The value
    in this field is number of years before and after the
    values given in the earliest and latest chronometric
    age fields within which the actual values are estimated to be.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyInYears"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeUncertaintyMethod(Field):
    """
    The method used to generate the value of ChronometricAgeUncertaintyInYears.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyMethod"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaterialDated(Field):
    """
    A description of the material on which the chronometricAgeProtocol was actually performed, if known.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/materialDated"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaterialDatedID(Field):
    """
    An identifier for the MaterialSample on which the chronometricAgeProtocol was performed, if applicable.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/materialDatedID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class MaterialDatedRelationship(Field):
    """
    The relationship of the MaterialDated to the subject of the ChronometricAge record.

    From which the ChronometricAge of the subject is inferred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/chrono/terms/materialDatedRelationship"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class ChronometricAgeDeterminedBy(Field):
    """
    A list of names of people, groups, or organizations who determined the ChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeDeterminedBy"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeDeterminedDate(Field):
    """
    The date on which the ChronometricAge was determined.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeDeterminedDate"
    TYPE = dt.datetime

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeReferences(Field):
    """
    A list of identifiers of literature associated with the ChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeReferences"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ChronometricAgeRemarks(Field):
    """
    Notes or comments about the ChronometricAge.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: Any, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/chrono/terms/chronometricAgeRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
