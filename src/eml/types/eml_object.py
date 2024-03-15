from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

from lxml import etree as et
from enum import Enum

from dwca.xml import XMLObject
from eml.types import ExtensionString


class Scope(Enum):
    DOCUMENT = 0
    SYSTEM = 1


class EMLObject(XMLObject, ABC):
    """
    Abstract class representing most of the EML document

    Parameters
    ----------
    _id : str, optional
        Unique identifier within the scope.
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined.
    references_system : str, optional
        System attribute of reference.
    """
    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None
    ) -> None:
        super().__init__()
        self.__id__ = _id
        self.__scope__ = scope
        self.__system__ = system
        self.__referencing__ = referencing
        if self.__referencing__:
            assert self.__id__ is not None, "Must give the id of the element being referenced."
        self.__references__ = ExtensionString(self.__id__, system=references_system)
        return

    @property
    def id(self) -> str:
        """str: Unique identifier of the resource"""
        return self.__id__

    @property
    def scope(self) -> Scope:
        """Scope: The scope of the identifier."""
        return self.__scope__

    @property
    def system(self) -> str:
        """str: The data management system within which an identifier is in scope and therefore unique."""
        return self.__system__

    @property
    def referencing(self) -> bool:
        """bool: Whether the resource is referencing another or is being defined"""
        return self.__referencing__

    @property
    def references(self) -> ExtensionString:
        """bool: Whether the resource is referencing another or is being defined"""
        return self.__references__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLObject | None:
        """
        Common parse of an EML object

        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to parse
        nmap : Dict
            Namespace

        Returns
        -------
        EMLObject
            Parsed EML Object
        """
        if element is None:
            return None
        _id = element.get("id", None)
        references = element.find("references", nmap)
        if _id is not None and references is not None:
            raise AssertionError("""
If an element references another element, it may not have an id. This prevents circular references.
See https://eml.ecoinformatics.org/validation-and-content-references#id-and-scope-examples
            """)
        if references is not None:
            eml_object = cls.get_referrer(element, nmap)
        else:
            eml_object = cls.get_no_referrer(element, nmap)
        eml_object.__namespace__ = nmap
        return eml_object

    @classmethod
    @abstractmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLObject:
        """
        Generate an EML Object referencing another EML Object.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLObject
            Object parsed that reference another.
        """
        pass

    @classmethod
    @abstractmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLObject:
        """
        Generate an EML Object that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLObject
            Object parsed.
        """
        pass

    @staticmethod
    def get_scope(element: et.Element) -> Scope:
        """
        Get the scope from the element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to find scope.

        Returns
        -------
        Scope
            A valid Scope.

        Raises
        ------
        ValueError
            Not a valid scope string.
        """
        scope = element.get("scope", None)
        if scope is None or scope == "document":
            return Scope.DOCUMENT
        elif scope == "system":
            return Scope.SYSTEM
        else:
            raise ValueError(f"{scope} is not a valid scope ('document' or 'system')")

    def generate_references_element(self) -> et.Element:
        """
        Generate the `<references>` element.

        Returns
        -------
        xml.etree.Element
            XML `Element` representing the references of referrer resource.
        """
        if not self.referencing:
            return None
        else:
            self.__references__.set_tag("references")
            return self.__references__.to_element()

    def _to_element_(self, element: et.Element) -> et.Element:
        """
        Add references values and common values to element.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        references = self.generate_references_element()
        if references is not None:
            element.append(references)
        else:
            if self.id is not None:
                element.set("id", self.id)
        element.set("scope", self.scope.name.lower())
        if self.system is not None:
            element.set("system", self.system)
        return element

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EMLObject):
            return (
                    self.id == other.id and
                    self.scope == other.scope and
                    self.system == other.system and
                    self.referencing == other.referencing and
                    self.references == other.references
            )
        else:
            return False
