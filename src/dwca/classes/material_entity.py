from dwca.classes import DataFile


class MaterialEntity(DataFile):
    """
    An entity that can be identified, exists for some period of time, and consists of physical matter while it exists.
    """
    URI = DataFile.URI + "MaterialEntity"
