from __future__ import annotations

from typing import Dict, Any
from urllib.parse import urlparse

from lxml import etree as et

from eml.types import _NoTagObject


class ExtensionURI(_NoTagObject):
    """
    Extension URI representing an uri value with extra attributes.

    Parameters
    ----------
    value : str
        Value of the URI.
    label : str
        A human-readable representation of the URI.
    """
    def __init__(self, value: str, label: str) -> None:
        super().__init__()
        validate_url = urlparse(value)
        if validate_url.scheme == '' or validate_url.netloc == '':
            raise ValueError(f"{value} is not a valid URI")
        self.__value__ = value
        self.__label__ = label
        return

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ExtensionURI):
            return str(self) == str(other) and self.label == other.label
        elif isinstance(other, str):
            return str(self) == other
        else:
            return False

    def __str__(self) -> str:
        return self.__value__

    def __repr__(self) -> str:
        return f"<ExtensionURI ({str(self)} [label={self.label}])>"

    @property
    def label(self) -> str:
        """str: A human-readable representation of the URI."""
        return self.__label__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> ExtensionURI | None:
        """
        Generate an ExtensionURI object from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        ExtensionURI
            An URI with a human-readable label.
        """
        if element is None:
            return None
        return ExtensionURI(element.text, element.get("label"))

    def to_element(self) -> et.Element:
        """
        Generate an XML element with the information of the extension URI.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        element = super().to_element()
        element.set("label", self.label)
        element.text = str(self)
        return element
