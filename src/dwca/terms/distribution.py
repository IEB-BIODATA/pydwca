from dwca.terms import Field


class ThreatStatus(Field):
    """
    Threat status of a species as defined by iucn: https://www.iucnredlist.org/resources/categories-and-criteria.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://iucn.org/terms/threatStatus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class AppendixCITES(Field):
    """
    The cites (convention on international trade in endangered species of wild fauna and flora) appendix number the taxa is listed. it is possible to have different appendix numbers for different areas, but "global" as an area is also valid if its the same worldwide.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/appendixCITES"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return
