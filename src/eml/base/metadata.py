from __future__ import annotations

from typing import Dict, List, Union

from lxml import etree as et

from dwca.xml import XMLObject


class EMLMetadata(XMLObject):
    """
    This element contains the additional metadata that is to be included in the document.

    Parameters
    ----------
    xml: lxml.etree.Element or str, optional
        An XML element instance or string representing a XML well define file.
    """
    PRINCIPAL_TAG = "metadata"

    def __init__(
            self,
            xml: Union[et.Element, str] = None
    ) -> None:
        super().__init__()
        if isinstance(xml, str):
            self.__content__ = et.fromstring(xml)
        else:
            self.__content__ = xml
        return

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLMetadata | None:
        """
        Generate a EMLMetadata from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLMetadata
            An EMLMetadata object.
        """
        if element is None:
            return None
        metadata = EMLMetadata(xml=element)
        metadata.__namespace__ = nmap
        return metadata

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance from this EMLMetadata object.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        return self.__content__


class EMLAdditionalMetadata(XMLObject):
    """
    A flexible field for including any other relevant metadata that pertains to the resource being described.

    Parameters
    ----------
    metadata: EMLMetadata
        This element contains the additional metadata that is to be included in the document.
    _id: str, optional
        Unique identifier for the additional metadata.
    describes: List[str], optional
        A pointer to the id attribute for the sub-portion of the resource that is described by this additional metadata.
    """
    PRINCIPAL_TAG = "additionalMetadata"

    def __init__(self, metadata: EMLMetadata, _id: str = None, describes: List[str] = None) -> None:
        super().__init__()
        self.__metadata__ = metadata
        self.__id__ = _id
        self.__describes__ = list()
        if describes is not None:
            self.__describes__.extend(describes)
        return

    @property
    def id(self) -> str:
        """str: Unique identifier for the additional metadata."""
        return self.__id__


    @property
    def metadata(self) -> EMLMetadata:
        """EMLMetadata: This element contains the additional metadata that is to be included in the document."""
        return self.__metadata__

    @property
    def describes(self) -> List[str]:
        """List[str]: A pointer to the id attribute for the sub-portion of the resource."""
        return self.__describes__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLAdditionalMetadata | None:
        """
        Generate an EMLAdditionalMetadata object from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLAdditionalMetadata
            An EMLAdditionalMetadata object.
        """
        if element is None:
            return None
        describes = list()
        for describe_elem in element.findall("describes", nmap):
            describes.append(describe_elem.text)
        metadata = EMLAdditionalMetadata(
            metadata=EMLMetadata.parse(element.find("metadata", nmap), nmap),
            _id=element.get("id", None),
            describes=describes,
        )
        metadata.__namespace__ = nmap
        return metadata

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance from the AdditionalMetadata object.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        root = et.Element("additionalMetadata")
        root.append(self.metadata.to_element())
        if self.id is not None:
            root.set("id", self.id)
        for describe in self.describes:
            describe_elem = self.object_to_element("describes")
            describe_elem.text = describe
            root.append(describe_elem)
        return root
