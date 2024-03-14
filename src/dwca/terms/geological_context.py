from dwca.terms import Field


class GeologicalContextID(Field):
    """
    An identifier for the set of information associated with a GeologicalContext.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/geologicalContextID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestEonOrLowestEonothem(Field):
    """
    The earliest possible geochronologic eon or lowest chrono-stratigraphic eonothem.

    The full name of the earliest possible geochronologic eon
    or lowest chrono-stratigraphic eonothem or the informal
    name ("Precambrian") attributable to the stratigraphic
    horizon from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestEonOrHighestEonothem(Field):
    """
    The latest possible geochronologic eon or highest chrono-stratigraphic eonothem.

    The full name of the latest possible geochronologic eon
    or highest chrono-stratigraphic eonothem or the informal
    name ("Precambrian") attributable to the stratigraphic
    horizon from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestEraOrLowestErathem(Field):
    """
    The earliest possible geochronologic era or lowest chronostratigraphic erathem.

    The full name of the earliest possible geochronologic era
    or lowest chronostratigraphic erathem attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestEraOrHighestErathem(Field):
    """
    The latest possible geochronologic era or highest chronostratigraphic erathem.

    The full name of the latest possible geochronologic era
    or highest chronostratigraphic erathem attributable to
    the stratigraphic horizon from which the MaterialEntity
    was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestPeriodOrLowestSystem(Field):
    """
    The earliest possible geochronologic period or lowest chronostratigraphic system.

    The full name of the earliest possible geochronologic period or
    lowest chronostratigraphic system attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestPeriodOrHighestSystem(Field):
    """
    The latest possible geochronologic period or highest chronostratigraphic system.

    The full name of the latest possible geochronologic period or
    highest chronostratigraphic system attributable to the
    stratigraphic horizon from which the MaterialEntity
    was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestEpochOrLowestSeries(Field):
    """
    The earliest possible geochronologic epoch or lowest chronostratigraphic series.

    The full name of the earliest possible geochronologic epoch
    or lowest chronostratigraphic series attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestEpochOrHighestSeries(Field):
    """
    The latest possible geochronologic epoch or highest chronostratigraphic series.

    The full name of the latest possible geochronologic epoch or
    highest chronostratigraphic series attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class EarliestAgeOrLowestStage(Field):
    """
    The earliest possible geochronologic age or lowest chronostratigraphic stage.

    The full name of the earliest possible geochronologic age
    or lowest chronostratigraphic stage attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LatestAgeOrHighestStage(Field):
    """
    The latest possible geochronologic age or highest chronostratigraphic stage.

    The full name of the latest possible geochronologic age or
    highest chronostratigraphic stage attributable to the
    stratigraphic horizon from which the MaterialEntity was
    collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LowestBiostratigraphicZone(Field):
    """
    The lowest possible geological biostratigraphic zone.

    The full name of the lowest possible geological
    biostratigraphic zone of the stratigraphic horizon
    from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/lowestBiostratigraphicZone"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class HighestBiostratigraphicZone(Field):
    """
    The highest possible geological biostratigraphic zone.

    The full name of the highest possible geological
    biostratigraphic zone of the stratigraphic horizon
    from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/highestBiostratigraphicZone"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LithostratigraphicTerms(Field):
    """
    The combination of all litho-stratigraphic names for the rock.

    The combination of all litho-stratigraphic names for the rock
    from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/lithostratigraphicTerms"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LithostratigraphicGroup(Field):
    """
    The full name of the lithostratigraphic group from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/group"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LithostratigraphicFormation(Field):
    """
    The full name of the lithostratigraphic formation from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/formation"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LithostratigraphicMember(Field):
    """
    The full name of the lithostratigraphic member from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/member"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class LithostratigraphicBed(Field):
    """
    The full name of the lithostratigraphic bed from which the MaterialEntity was collected.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/bed"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
