import datetime as dt
from typing import Union, List

from datetime_interval import Interval

from dwca.terms import Field


class EventID(Field):
    """
    An identifier for the set of information associated with an Event (something that occurs at a place and time).
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/eventID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ParentEventID(Field):
    """
    An identifier for the broader Event that groups this and potentially other Events.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/parentEventID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EventType(Field):
    """
    The nature of the Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/eventType"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class FieldNumber(Field):
    """
    An identifier given to the Event in the field. Often serves as a link between field notes and the Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/fieldNumber"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EventDate(Field):
    """
    The date-time or interval during which an Event occurred.

    For occurrences, this is the date-time when the Event was recorded.
    Not suitable for a time in a geological context.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/eventDate"
    TYPE = Union[dt.datetime, Interval]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EventTime(Field):
    """
    The time or interval during which a Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/eventTime"
    TYPE = Union[dt.time, Interval]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class StartDayOfYear(Field):
    """
    The earliest integer day of the year on which the Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/startDayOfYear"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EndDayOfYear(Field):
    """
    The latest integer day of the year on which the Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/endDayOfYear"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DWCYear(Field):
    """
    The four-digit year in which the Event occurred, according to the Common Era Calendar.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/year"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DWCMonth(Field):
    """
    The integer month in which the Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/month"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DWCDay(Field):
    """
    The integer day of the month on which the Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/day"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VerbatimEventDate(Field):
    """
    The verbatim original representation of the date and time information for an Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimEventDate"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Habitat(Field):
    """
    A category or description of the habitat in which the Event occurred.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/habitat"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class SamplingProtocol(Field):
    """
    The names of, references to, or descriptions of the methods or protocols used during a Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/samplingProtocol"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class SampleSizeValue(Field):
    """
    A measurement of the size (time duration, length, area, or volume) of a sample in a sampling Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/sampleSizeValue"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class SampleSizeUnit(Field):
    """
    The unit of measurement of the size (time duration, length, area, or volume) of a sample in a sampling Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/sampleSizeUnit"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class SamplingEffort(Field):
    """
    The amount of effort expended during an Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/samplingEffort"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class FieldNotes(Field):
    """
    Notes taken in the field about the dwc:Event.

    One of:
    a) An indicator of the existence of the notes.
    b) A reference to (publication, URI) the notes.
    c) The text of the notes.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/fieldNotes"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EventRemarks(Field):
    """
    Comments or notes about the Event.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/eventRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
