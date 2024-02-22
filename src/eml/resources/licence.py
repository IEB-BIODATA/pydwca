from __future__ import annotations
from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class EMLLicense(XMLObject):
    """
    Information identifying a well-known license for the metadata and data.

    Parameters
    ----------
    name : str
        The official name of the license.
    url : str, optional
        The persistent URL for the license.
    identifier : str, optional
        License Identifier.
    """
    PRINCIPAL_TAG = "licensed"

    def __init__(self, name: str, url: str = None, identifier: str = None) -> None:
        super().__init__()
        self.__name__ = name
        self.__url__ = url
        self.__id__ = identifier
        return

    @property
    def name(self) -> str:
        """str: The official name of the license."""
        return self.__name__

    @property
    def url(self) -> str:
        """str: The persistent URL for the license."""
        return self.__url__

    @property
    def id(self) -> str:
        """str: License Identifier."""
        return self.__id__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLLicense | None:
        """
        Generate an EMLLicense object from a given XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse
        nmap : Dict
            Namespace

        Returns
        -------
        EMLLicense
            Parsed object
        """
        if element is None:
            return None
        name_elem = element.find("licenseName", nmap)
        name = name_elem.text if name_elem.text is not None else ""
        url_elem = element.find("url", nmap)
        if url_elem is not None:
            url = url_elem.text if url_elem.text is not None else ""
        else:
            url = None
        id_elem = element.find("identifier", nmap)
        if id_elem is not None:
            identifier = id_elem.text if id_elem.text is not None else ""
        else:
            identifier = None
        licence = EMLLicense(name, url=url, identifier=identifier)
        licence.__namespace__ = nmap
        return licence

    def to_element(self) -> et.Element:
        """
        Generate an XML element with EMLLicense instance information.

        Returns
        -------
        lxml.etree.Element
            XML element object
        """
        license_elem = super().to_element()
        license_name = self.object_to_element("licenseName")
        license_name.text = self.name
        license_elem.append(license_name)
        if self.url is not None:
            url = self.object_to_element("url")
            url.text = self.url
            license_elem.append(url)
        if self.id is not None:
            identifier = self.object_to_element("identifier")
            identifier.text = self.id
            license_elem.append(identifier)
        return license_elem
