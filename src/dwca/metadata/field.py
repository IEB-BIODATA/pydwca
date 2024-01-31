from __future__ import annotations
from typing import Any, Dict

from lxml import etree as et

from dwca.xml import XMLObject


class Field(XMLObject):
    PRINCIPAL_TAG = "field"
    """str: Principal tag `field`"""

    def __init__(self, term: str, index: int | str = None, default: Any = None, vocabulary: str = None) -> None:
        super().__init__()
        self.__term__ = term
        self.__index__ = int(index)
        self.__default__ = default
        self.__vocabulary__ = vocabulary
        return

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> Field | None:
        if element is None:
            return None
        if "term" not in element.attrib:
            raise TypeError("Field must have a term")
        field = Field(
            element.get("term"),
            element.get("index", None),
            element.get("default", None),
            element.get("vocabulary", None)
        )
        field.__namespace__ = nsmap
        return Field(
            element.get("term"),
            element.get("index", None),
            element.get("default", None),
            element.get("vocabulary", None)
        )

    def to_element(self) -> et.Element:
        element = super().to_element()
        element.set("term", self.__term__)
        if self.__index__ is not None:
            element.set("index", str(self.__index__))
        if self.__default__ is not None:
            element.set("default", self.__default__)
        if self.__vocabulary__ is not None:
            element.set("vocabulary", self.__vocabulary__)
        return element

    def __repr__(self) -> str:
        return f"<Field [term={self.__term__}]>"
