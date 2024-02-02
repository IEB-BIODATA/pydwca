from __future__ import annotations
from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class EMLInline(XMLObject):
    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLInline | None:
        pass

    def to_element(self) -> et.Element:
        pass
