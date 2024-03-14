from __future__ import annotations
from typing import Dict, Tuple, Any

from lxml import etree as et

from eml.types import EMLObject, _NoTagObject, Scope, ExtensionURI


class SemanticAnnotation(EMLObject, _NoTagObject):
    """
    A precisely-defined semantic statement about this resource.

    Parameters
    ----------
    property_uri : Tuple[str, str]
        The persistent URI used to identify a property from a vocabulary.
    value_uri : Tuple[str, str]
        The persistent URI used to identify a value from a vocabulary.
    _id : str, optional
        Unique identifier within the scope.
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    """
    def __init__(
            self,
            property_uri: Tuple[str, str],
            value_uri: Tuple[str, str],
            _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
    ) -> None:
        super().__init__(_id, scope, system)
        self.__property__ = ExtensionURI(property_uri[0], property_uri[1])
        self.__value__ = ExtensionURI(value_uri[0], value_uri[1])
        return

    @property
    def property_uri(self) -> ExtensionURI:
        """ExtensionURI: The persistent URI used to identify a property from a vocabulary."""
        return self.__property__

    @property
    def value_uri(self) -> ExtensionURI:
        """ExtensionURI: The persistent URI used to identify a value from a vocabulary."""
        return self.__value__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> SemanticAnnotation:
        """
        Semantic Annotation doesn't have a reference. This method raise an exception.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        SemanticAnnotation
            Object parsed that would reference another.

        Raises
        ------
        ValueError
            Semantic Annotation cannot reference another annotation.
        """
        raise ValueError("Semantic Annotation cannot reference another annotation")

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> SemanticAnnotation:
        """
        Generate a Semantic Annotation from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        SemanticAnnotation
            Object parsed.
        """
        property_elem = element.find("propertyURI", nmap)
        value_elem = element.find("valueURI", nmap)
        return SemanticAnnotation(
            (property_elem.text, property_elem.get("label")),
            (value_elem.text, value_elem.get("label")),
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None)
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance.

        Returns
        -------
        lxml.etree.Element
            XML element instance.
        """
        element = _NoTagObject.to_element(self)
        element = self._to_element_(element)
        self.property_uri.set_tag("propertyURI")
        element.append(self.property_uri.to_element())
        self.value_uri.set_tag("valueURI")
        element.append(self.value_uri.to_element())
        return element

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SemanticAnnotation):
            return (super().__eq__(other) and
                    self.property_uri == other.property_uri and
                    self.value_uri == other.value_uri)
        else:
            return False
