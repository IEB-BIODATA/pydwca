from __future__ import annotations

from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class ResponsibleParty(XMLObject):
    """
    The individual, organization, or role associated with a resource.
    """
    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> XMLObject | None:
        pass

    def to_element(self) -> et.Element:
        pass
