from dwca.classes import DataFile


class Identification(DataFile):
    """
    A taxonomic determination (e.g., the assignment to a dwc:Taxon).
    """
    URI = DataFile.URI + "Identification"
