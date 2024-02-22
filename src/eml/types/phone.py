from __future__ import annotations
from typing import Dict, Union

from lxml import etree as et

from dwca.xml import XMLObject


class EMLPhone(XMLObject):
    """
    Information about the contact's telephone.

    Parameters
    ----------
    phone : str
        The phone field describes information about the responsible party's telephone.
    phone_type : str, optional
        The type of the phone to which this number applies. Default "voice".
    """
    PRINCIPAL_TAG = "phone"

    def __init__(self, phone: str, phone_type: str = "voice") -> None:
        super().__init__()
        self.__phone__ = phone
        self.__phone_type__ = phone_type
        return

    @property
    def phone(self) -> str:
        """
        str: The phone field describes information about the responsible party's telephone.
        """
        return self.__phone__

    @property
    def phone_type(self) -> str:
        """
        str: The type of the phone to which this number applies.
        """
        return self.__phone_type__

    def __eq__(self, other: Union[EMLPhone, str]) -> bool:
        if isinstance(other, str):
            return self.phone == other
        elif isinstance(other, EMLPhone):
            return self.phone == other.phone and self.phone_type == other.phone_type
        else:
            return False

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLPhone | None:
        """
        Parses a lxml element into an EML Phone object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        XMLObject
            Object parsed.
        """
        phone = EMLPhone(element.text, element.get("phonetype", "voice"))
        phone.__namespace__ = nmap
        return phone

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the EML Phone object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        phone_elem = super().to_element()
        phone_elem.set("phonetype", self.phone_type)
        return phone_elem
