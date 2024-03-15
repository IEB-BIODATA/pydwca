from __future__ import annotations

import logging
from typing import Dict, Union, List, Any

from lxml import etree as et

from dwca.utils import Language
from eml.types import EMLObject, Scope, I18nString


class EMLAddress(EMLObject):
    """
    The full address information for a given responsible party entry.

    Parameters
    ----------
    _id : str, optional
        Unique identifier within the scope.
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined
    references_system : str, optional
        System attribute of reference
    delivery_point : str, I18nString or List[I18String], optional
        The location for postal deliveries.
    city : str or I18nString, optional
        The name of the city for the contact.
    administrative_area : str or I18nString, optional
        The political area of a country.
    postal_code : str or I18nString, optional
        The postal code used for routing to an address.
    country : str or I18nString, optional
        The name of the country for the contact's address.
    """
    PRINCIPAL_TAG = "address"

    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            delivery_point: Union[str, I18nString, List[I18nString]] = None,
            city: Union[str, I18nString] = None,
            administrative_area: Union[str, I18nString] = None,
            postal_code: Union[str, I18nString] = None,
            country: Union[str, I18nString] = None,
            language: Language.ENG = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__delivery_point__: List[I18nString] = list()
        if isinstance(delivery_point, list):
            self.__delivery_point__.extend(delivery_point)
        elif delivery_point is not None:
            self.__delivery_point__.append(I18nString(delivery_point, lang=language))
        self.__city__ = None
        if city is not None:
            self.__city__ = I18nString(city, lang=language)
        self.__admin_area__ = None
        if administrative_area is not None:
            self.__admin_area__ = I18nString(administrative_area, lang=language)
        self.__postal_code__ = None
        if postal_code is not None:
            self.__postal_code__ = I18nString(postal_code, lang=language)
        self.__country__ = None
        if country is not None:
            self.__country__ = I18nString(country, lang=language)
        return

    @property
    def delivery_point(self) -> List[I18nString]:
        """
        List[I18nString]: The location for postal deliveries.
        """
        return self.__delivery_point__

    @property
    def city(self) -> I18nString:
        """
        I18String: The name of the city for the contact.
        """
        return self.__city__

    @property
    def administrative_area(self) -> I18nString:
        """
        I18nString: The political area of a country.
        """
        return self.__admin_area__

    @property
    def postal_code(self) -> I18nString:
        """
        I18nString: The postal code used for routing to an address.
        """
        return self.__postal_code__

    @property
    def country(self) -> I18nString:
        """
        I18nString: The name of the country for the contact's address.
        """
        return self.__country__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLAddress:
        """
        Generate an EML Address referencing another EML Address.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references EML address.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLAddress
            Object parsed that reference an Address.
        """
        references = element.find("references")
        address = EMLAddress(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )
        return address

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLAddress:
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
        EMLAddress
            Object parsed.
        """
        delivery_points = list()
        for delivery_point in element.findall("deliveryPoint"):
            delivery_points.append(I18nString.parse(delivery_point, nmap))
        address = EMLAddress(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            delivery_point=delivery_points,
            city=I18nString.parse(element.find("city", nmap), nmap),
            administrative_area=I18nString.parse(element.find("administrativeArea", nmap), nmap),
            postal_code=I18nString.parse(element.find("postalCode", nmap), nmap),
            country=I18nString.parse(element.find("country", nmap), nmap)
        )
        return address

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        address = super().to_element()
        address = self._to_element_(address)
        references = self.generate_references_element()
        if references is None:
            for delivery_point in self.delivery_point:
                delivery_point.set_tag("deliveryPoint")
                address.append(delivery_point.to_element())
            if self.city is not None:
                self.city.set_tag("city")
                address.append(self.city.to_element())
            if self.administrative_area:
                self.administrative_area.set_tag("administrativeArea")
                address.append(self.administrative_area.to_element())
            if self.postal_code is not None:
                self.postal_code.set_tag("postalCode")
                address.append(self.postal_code.to_element())
            if self.country is not None:
                self.country.set_tag("country")
                address.append(self.country.to_element())
        return address

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EMLAddress):
            return (super().__eq__(other) and
                    sorted(self.delivery_point) == sorted(other.delivery_point) and
                    self.city == other.city and
                    self.administrative_area == other.administrative_area and
                    self.postal_code == other.postal_code and
                    self.country == other.country)
        else:
            return False
