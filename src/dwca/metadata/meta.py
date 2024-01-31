from __future__ import annotations

from typing import List, Dict

import lxml.etree as et

from dwca.metadata import Core, Extension
from dwca.xml import XMLObject


class Metadata(XMLObject):
    """
    Metadata class of the Darwin Core Archive storing the
    file name of the archive elements

    Parameters
    ----------
    metadata : str, optional
        Name of the metadata file (e.g.: eml.xml)
    """
    PRINCIPAL_TAG = "archive"
    """str : Require tag of the metadata"""

    def __init__(self, metadata: str = None) -> None:
        super().__init__()
        self.__metadata__ = metadata
        self.__core__ = None
        self.__extensions__: List[Extension] = list()
        return

    @property
    def core(self) -> Core:
        """
        Core : Core object representing the data entity upon which records
            are based on
        """
        return self.__core__

    @property
    def extensions(self) -> List[Extension]:
        """
        List[Extension] : A list of Extension objects representing the entities
            directly related to the core
        """
        return self.__extensions__

    @property
    def metadata_filename(self) -> str:
        """
        str : If present, the metadata filename (e.g.: eml.xml)
        """
        return self.__metadata__

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> Metadata:
        """
        Parses an `lxml.etree.Element` in a Metadata instance

        Parameters
        ----------
        element : `lxml.etree.Element`
            XML element to be parsed
        nsmap : Dict
            Namespace prefix:uri

        Returns
        -------
        Metadata
            New Metadata instance with the data from the element
        """
        metadata = Metadata(element.get("metadata", None))
        core = Core.parse(element.find(f"{{{nsmap[None]}}}core"), nsmap=nsmap)
        metadata.__core__ = core
        for extension in element.findall(f"{{{nsmap[None]}}}extension"):
            metadata.__extensions__.append(Extension.parse(extension, nsmap=nsmap))
        return metadata

    def to_element(self) -> et.Element:
        """
        Generates an element from a Metadata instance. This
        element can be used to write the XML file containing
        the Metadata  information. See :func:`~dwca.xml.xml_object.XMLObject.to_xml`

        Returns
        -------
        lxml.etree.Element
            XML element from Metadata instance
        """
        element = super().to_element()
        if self.__metadata__ is not None:
            element.set("metadata", self.__metadata__)
        return element
