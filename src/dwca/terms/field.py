from __future__ import annotations

from abc import ABC
from typing import Any, Dict

from lxml import etree as et

from dwca.xml import XMLObject


class Field(XMLObject, ABC):
    """
    Element use to specify the location and content of data within a :class:`dwca.classes.data_file.DataFile`.

    Parameters
    ----------
    index : int
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    PRINCIPAL_TAG = "field"
    URI = "http://rs.tdwg.org/dwc/terms/"
    """str: URI for the term represented by this field."""
    TYPE = Any
    """type: Type of the field."""

    def __init__(self, index: int | str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__()
        self.__index__ = int(index)
        self.__default__ = default
        self.__vocabulary__ = vocabulary
        return

    @property
    def index(self) -> int:
        """int: Specifies the position of the column in the row."""
        return self.__index__

    @property
    def default(self) -> Any:
        """Any: Specifies a value to use if one is not supplied"""
        return self.__default__

    @property
    def vocabulary(self) -> str:
        """str: An URI for a vocabulary that the source values for this Field are based on."""
        return self.__vocabulary__

    @property
    def uri(self) -> str:
        """str: An URI for the term represented by this field"""
        return self.URI

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> Field | None:
        """
        Generate a Field object from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        Field
            A Field object.
        """
        if element is None:
            return None
        if "term" not in element.attrib:
            raise TypeError("Field must have a term")
        field = cls(
            index=element.get("index", None),
            default=element.get("default", None),
            vocabulary=element.get("vocabulary", None)
        )
        field.__namespace__ = nmap
        return field

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance from this object.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        element = super().to_element()
        element.set("term", self.uri)
        if self.__index__ is not None:
            element.set("index", str(self.__index__))
        if self.__default__ is not None:
            element.set("default", self.__default__)
        if self.__vocabulary__ is not None:
            element.set("vocabulary", self.__vocabulary__)
        return element

    def __repr__(self) -> str:
        return f"<Field [term={self.uri}]>"