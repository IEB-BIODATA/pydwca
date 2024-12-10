from __future__ import annotations

from math import frexp
from typing import Dict, List

from lxml import etree as et

from eml.types import EMLTextType, ChangeHistory
from xml_common import XMLObject
from xml_common.utils import CamelCaseEnum


class MaintUpFreqType(CamelCaseEnum):
    """
    Maintenance Update Frequency.

    Frequency with which changes and additions are made to the
    dataset after the initial dataset is completed.

    Attributes
    ----------
    ANNUALLY : int
        Every year.
    AS_NEEDED : int
        Maintenance as needed.
    BIANNUALLY : int
        Every two years.
    CONTINUALLY : int
        Maintenance continually.
    DAILY : int
        Every day.
    IRREGULAR : int
        Irregular maintenance.
    MONTHLY : int
        Every month.
    NOT_PLANNED : int
        Maintenance not planned.
    WEEKLY : int
        Every week.
    UNKNOWN : int
        Unknown maintenance.
    UNKOWN : int
        Unknown with typo.
    OTHER_MAINTENANCE_PERIOD : int
        Other unidentified maintenance period.
    """
    ANNUALLY = 1
    AS_NEEDED = 2
    BIANNUALLY = 3
    CONTINUALLY = 4
    DAILY = 5
    IRREGULAR = 6
    MONTHLY = 7
    NOT_PLANNED = 8
    WEEKLY = 9
    UNKNOWN = 10
    UNKOWN = 11
    OTHER_MAINTENANCE_PERIOD = 12


class Maintenance(XMLObject):
    """
    Class representing a description of the maintenance of a data resource.

    Parameters
    ----------
    description : EMLTextType
        A text description of the maintenance of this data resource.
    maintenance_update_frequency : MaintUpFreqType, optional
        Frequency with which changes and additions are made to the dataset after the initial dataset is completed.
    change_history : List[ChangeHistory], optional
        A description of changes made to the data since its release.
    """
    PRINCIPAL_TAG = "maintenance"

    def __init__(
            self, description: EMLTextType,
            maintenance_update_frequency: MaintUpFreqType = None,
            change_history: List[ChangeHistory] = None
    ):
        super().__init__()
        self.__description__ = description
        self.__muf__ = maintenance_update_frequency
        self.__c_hist__ = list()
        if change_history is not None:
            self.__c_hist__.extend(change_history)
        return

    @property
    def description(self) -> EMLTextType:
        """EMLTextType: A text description of the maintenance of this data resource."""
        return self.__description__

    @property
    def maintenance_update_frequency(self) -> MaintUpFreqType:
        """MaintUpFreqType: Frequency with which changes and additions are made to the dataset after the initial dataset is completed."""
        return self.__muf__

    @property
    def change_history(self) -> List[ChangeHistory]:
        """List[ChangeHistory]: A description of changes made to the data since its release."""
        return self.__c_hist__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> Maintenance | None:
        """
        Parses a lxml element into a Maintenance object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Maintenance object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        Maintenance
            Object parsed.
        """
        if element is None:
            return None
        freq_elem = element.find("maintenanceUpdateFrequency", nmap)
        muf = MaintUpFreqType.get_enum(freq_elem.text) if freq_elem is not None else None
        change_history_elems = element.findall("changeHistory", nmap)
        change_history = list()
        for ch in change_history_elems:
            change_history.append(ChangeHistory.parse(ch, nmap))
        return Maintenance(
            description=EMLTextType.parse(element.find("description", nmap), nmap),
            maintenance_update_frequency=muf,
            change_history=change_history
        )


    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the Maintenance object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        element = super().to_element()
        self.description.set_tag("description")
        element.append(self.description.to_element())
        if self.maintenance_update_frequency is not None:
            muf_elem = self.object_to_element("maintenanceUpdateFrequency")
            muf_elem.text = self.maintenance_update_frequency.to_camel_case()
            element.append(muf_elem)
        for ch in self.change_history:
            element.append(ch.to_element())
        return element
