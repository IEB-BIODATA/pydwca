from __future__ import annotations

from typing import Any, Dict
from lxml import etree as et

from dwca.terms import Field


class OutsideTerm(Field):
    """
    Terms defined outside the Darwin Core specifications.

    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    uri : str
        URI of the term.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    TYPE = str

    def __init__(self, index: int | str, uri: str = None, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        self.URI = uri
        return

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> OutsideTerm | None:
        """
        Generate a OutsideTerm object from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        OutsideTerm
            An OutsideTerm object.
        """
        if element is None:
            return None
        if "term" not in element.attrib:
            raise TypeError("Field must have a term")
        field = OutsideTerm(
            element.get("index"),
            element.get("term", None),
            element.get("default", None),
            element.get("vocabulary", None),
        )
        field.__namespace__ = nmap
        return field
