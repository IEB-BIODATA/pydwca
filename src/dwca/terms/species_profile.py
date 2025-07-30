from dwca.terms import Field


class IsMarine(Field):
    """
    A boolean flag indicating whether the taxon is a marine organism, i.e. can be found in/above sea water.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isMarine"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IsFreshwater(Field):
    """
    A boolean flag indicating whether the taxon occurrs in freshwater habitats, i.e. can be found in/above rivers or lakes.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isFreshwater"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IsTerrestrial(Field):
    """
    A boolean flag indicating the taxon is a terrestial organism, i.e. occurrs on land as opposed to the sea.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isTerrestrial"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IsInvasive(Field):
    """
    Flag indicating a species known to be invasive/alien in some are of the world. detailed native and introduced distribution areas can be published with the distribution extension..

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isInvasive"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IsHybrid(Field):
    """
    Flag indicating a hybrid organism. this does not have to be reflected in the name, but can be based on other studies like chromosome numbers etc.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isHybrid"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class IsExtinct(Field):
    """
    Flag indicating an extinct organism. details about the timeperiod the organism has lived in can be supplied below.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/isExtinct"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class LivingPeriod(Field):
    """
    The (geological) time a currently extinct organism is known to have lived. for geological times of fossils ideally based on a vocabulary like http://en.wikipedia.org/wiki/geologic_column.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/livingPeriod"
    TYPE = bool

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class AgeInDays(Field):
    """
    Maximum observed age of an organism given as number of days.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/ageInDays"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class SizeInMillimeters(Field):
    """
    Maximum observed size of an organism in millimeter. can be either height, length or width, whichever is greater..

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/sizeInMillimeters"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class MassInGrams(Field):
    """
    Maximum observed weight of an organism in grams..

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/massInGrams"
    TYPE = float

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class LifeForm(Field):
    """
    A term describing the growth/lifeform of an organism. should be based on a vocabulary like raunkiær for plants: http://en.wikipedia.org/wiki/raunkiær_plant_life-form. recommended vocabulary: http://rs.gbif.org/vocabulary/gbif/life_form.xml.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.gbif.org/terms/1.0/lifeForm"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return

class SpeciesSex(Field):
    """
    Comma seperated list of known sexes to exist for this organism. recommended vocabulary is: http://rs.gbif.org/vocabulary/gbif/sex.xml.

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
