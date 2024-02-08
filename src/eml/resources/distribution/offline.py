from __future__ import annotations
from typing import Dict, List

from lxml import etree as et

from dwca.xml import XMLObject


class EMLOffline(XMLObject):
    """
    Offline distribution when data are available offline.

    Parameters
    ----------
    medium_name : str
        Name of the medium that for this resource distribution.
    medium_density : str, optional
        The density of the digital medium if this is relevant.
    medium_density_units : str, optional
        A numerical density's units.
    medium_volume : str, optional
        Total volume of the storage medium.
    medium_format : List[str], optional
        Format of the medium on which the resource is shipped.
    medium_note : str, optional
        Note about the media.
    """
    PRINCIPAL_TAG = 'offline'
    """str: Principle tag `offline`."""

    def __init__(
            self, medium_name: str,
            medium_density: str = None,
            medium_density_units: str = None,
            medium_volume: str = None,
            medium_format: List[str] = None,
            medium_note: str = None,
    ) -> None:
        super().__init__()
        self.__name__ = medium_name
        self.__density__ = medium_density
        self.__density_units__ = medium_density_units
        self.__volume__ = medium_volume
        self.__format__ = list()
        if medium_format is not None:
            self.__format__.extend(medium_format)
        self.__note__ = medium_note
        return

    @property
    def medium_name(self) -> str:
        """str: Name of the medium that for this resource distribution."""
        return self.__name__

    @property
    def medium_density(self) -> str:
        """str : Density of the digital medium if this is relevant."""
        return self.__density__

    @property
    def medium_density_units(self) -> str:
        """str : Numerical density's units."""
        return self.__density_units__

    @property
    def medium_volume(self) -> str:
        """str: Total volume of the storage medium."""
        return self.__volume__

    @property
    def medium_format(self) -> List[str]:
        """List[str]: Format of the medium on which this resource is shipped."""
        return self.__format__

    @property
    def medium_note(self) -> str:
        """str: Note about the media."""
        return self.__note__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLOffline | None:
        """
        Generate an EMLOffline object from an XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLOffline
            Instance with the offline media distribution.
        """
        if element is None:
            return None
        name_elem = element.find("mediumName", nmap)
        name = name_elem.text if name_elem.text is not None else ""
        density_elem = element.find("mediumDensity", nmap)
        if density_elem is not None:
            density = density_elem.text if density_elem.text is not None else ""
        else:
            density = None
        units_elem = element.find("mediumDensityUnits", nmap)
        if units_elem is not None:
            units = units_elem.text if units_elem.text is not None else ""
        else:
            units = None
        volume_elem = element.find("mediumVolume", nmap)
        if volume_elem is not None:
            volume = volume_elem.text if volume_elem.text is not None else ""
        else:
            volume = None
        medium_format = list()
        for format_elem in element.findall("mediumFormat", nmap):
            medium_format.append(format_elem.text if format_elem.text is not None else "")
        note_elem = element.find("mediumNote", nmap)
        if note_elem is not None:
            note = note_elem.text if note_elem.text is not None else ""
        else:
            note = None
        offline = EMLOffline(
            medium_name=name,
            medium_density=density,
            medium_density_units=units,
            medium_volume=volume,
            medium_format=medium_format,
            medium_note=note,
        )
        offline.__namespace__ = nmap
        return offline

    def to_element(self) -> et.Element:
        """
        Generate an XML element with the information of the EMLOffline instance.

        Returns
        -------
        lxml.etree.Element
            XML element with the information of the EMLOffline.
        """
        offline_elem = super().to_element()
        name = self.object_to_element("mediumName")
        name.text = self.medium_name
        offline_elem.append(name)
        if self.medium_density is not None:
            density_elem = self.object_to_element("mediumDensity")
            density_elem.text = self.medium_density
            offline_elem.append(density_elem)
        if self.medium_density_units is not None:
            units_elem = self.object_to_element("mediumDensityUnits")
            units_elem.text = self.medium_density
            offline_elem.append(units_elem)
        if self.medium_volume is not None:
            volume_elem = self.object_to_element("mediumVolume")
            volume_elem.text = self.medium_volume
            offline_elem.append(volume_elem)
        for medium_format in self.medium_format:
            format_elem = self.object_to_element("mediumFormat")
            format_elem.text = medium_format
            offline_elem.append(format_elem)
        if self.medium_note is not None:
            note_elem = self.object_to_element("mediumNote")
            note_elem.text = self.medium_note
            offline_elem.append(note_elem)
        return offline_elem
