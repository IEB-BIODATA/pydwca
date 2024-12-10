from __future__ import annotations
import datetime as dt
from typing import Dict
from lxml import etree as et
from xml_common import XMLObject
from xml_common.utils import format_datetime
from xml_common.utils.type_functions import unformat_datetime


class ChangeHistory(XMLObject):
    """
    Attributes:
    -----------
    change_scope : str
        An expression describing the scope to which the documented change was applied.
    old_value : str
        The previous value of the data prior to the change.
    change_date : datetime.datetime
        The date the changes were applied.
    comment : str, optional
        Explanation or justification for the change made to the data.
    """
    PRINCIPAL_TAG = "changeHistory"

    def __init__(
            self, change_scope: str, old_value: str,
            change_date: dt.date, comment: str = None
    ) -> None:
        super().__init__()
        self.__change_scope__ = change_scope
        self.__old_value__ = old_value
        self.__change_dt__ = change_date
        self.__comment__ = comment
        return

    @property
    def change_scope(self) -> str:
        """str: An expression describing the scope to which the documented change was applied."""
        return self.__change_scope__

    @property
    def old_value(self) -> str:
        """str: The previous value of the data prior to the change."""
        return self.__old_value__

    @property
    def change_date(self) -> dt.date:
        """datetime.date: The date the changes were applied."""
        return self.__change_dt__

    @property
    def comment(self) -> str:
        """str: Explanation or justification for the change made to the data."""
        return self.__comment__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> ChangeHistory | None:
        """
        Parses a lxml element into a ChangeHistory object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        ChangeHistory
            Instance from parsed xml element.
        """
        if element is None:
            return None
        comment_elem = element.find("comment", nmap)
        comment = comment_elem.text if comment_elem is not None else None
        return ChangeHistory(
            change_scope=element.find("changeScope", nmap).text,
            old_value=element.find("oldValue", nmap).text,
            change_date=format_datetime(element.find("changeDate", nmap).text).date(),
            comment=comment
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element with ChangeHistory instance information.

        Returns
        -------
        lxml.etree.Element
            XML element object
        """
        change_hist_elem = super().to_element()
        change_scope_elem = self.object_to_element("changeScope")
        change_scope_elem.text = self.change_scope
        change_hist_elem.append(change_scope_elem)
        old_value_elem = self.object_to_element("oldValue")
        old_value_elem.text = self.old_value
        change_hist_elem.append(old_value_elem)
        change_date_elem = self.object_to_element("changeDate")
        change_date_elem.text = unformat_datetime(dt.datetime.combine(self.change_date, dt.time()))
        change_hist_elem.append(change_date_elem)
        if self.comment is not None:
            comment_elem = self.object_to_element("comment")
            comment_elem.text = self.comment
            change_hist_elem.append(comment_elem)
        return change_hist_elem
