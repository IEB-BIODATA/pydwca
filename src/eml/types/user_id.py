from typing import Dict

from lxml import etree as et

from dwca.xml import XMLObject


class EMLAddress(XMLObject):
    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> XMLObject | None:
        """
        Parses a lxml element into an XMLObject.

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
        pass

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        pass
