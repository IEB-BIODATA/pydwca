from dwca.classes import DataFile


class Occurrence(DataFile):
    """
    An existence of an organism at a particular place at a particular time.
    """
    URI = DataFile.URI + "Occurrence"
