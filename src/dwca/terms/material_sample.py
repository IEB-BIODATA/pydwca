from dwca.terms import Field


class MaterialSampleID(Field):
    """
    An identifier for the MaterialSample (as opposed to a particular digital record of the MaterialSample).
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/materialSampleID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
