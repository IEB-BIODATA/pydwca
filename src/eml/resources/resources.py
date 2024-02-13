from __future__ import annotations

from lxml import etree as et

from enum import Enum


class EMLResource(Enum):
    """
    Type of the resources described by the EML file.
    """
    DATASET = 0
    CITATION = 1
    SOFTWARE = 2
    PROTOCOL = 3

    @classmethod
    def get_resource_type(cls, element: et.Element) -> EMLResource:
        """
        Get the resource type from the tag of one element inside another XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element instance.

        Returns
        -------
        EMLResource
            Type of resource.

        Raises
        ------
        ValueError
            If resource type is not a valid type.
        """
        for resource in EMLResource:
            if element.find(resource.name.lower()) is not None:
                return resource
        raise ValueError(f"""One of the following must be present: {', '.join(
            [eml_resource.name.lower() for eml_resource in EMLResource]
        )}""")
