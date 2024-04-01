from __future__ import annotations

from typing import Dict

from lxml import etree as et

from eml.resources.distribution import EMLOnline, EMLOffline, EMLInline
from eml.types import EMLObject, Scope


class EMLDistribution(EMLObject):
    """
    Information on how the resource is distributed online and offline.

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
    online : EMLOnline, optional
        Online distribution information.
    offline : EMLOffline, optional
        Data are available offline.
    inline : EMLInline, optional
        Data distributed inline in the metadata.
    """
    PRINCIPAL_TAG = "distribution"

    def __init__(self, _id: str = None, scope: Scope = Scope.DOCUMENT, system: str = None, referencing: bool = False,
                 references_system: str = None, online: EMLOnline = None, offline: EMLOffline = None,
                 inline: EMLInline = None) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        if not self.referencing:
            declared = (online is not None) + (offline is not None) + (inline is not None)
            if declared == 0:
                raise TypeError("At least declare online, offline or inline distribution.")
            if declared > 1:
                raise TypeError("Declare only one of the following: online, offline or inline distribution.")
        self.__online__ = online
        self.__offline__ = offline
        self.__inline__ = inline
        return

    @property
    def online(self) -> EMLOnline:
        """EMLOnline: Online distribution information."""
        return self.__online__

    @property
    def offline(self) -> EMLOffline:
        """EMLOffline: Data are available offline."""
        return self.__offline__

    @property
    def inline(self) -> EMLInline:
        """EMLInline: Data distributed inline in the metadata."""
        return self.__inline__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLDistribution:
        """
        Generate an EML Distribution referencing another EML Distribution.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLDistribution
            Object parsed that reference another.
        """
        references = element.find("references", nmap)
        return EMLDistribution(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLDistribution:
        """
        Generate an EML Distribution that do not reference another.

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
        online = EMLOnline.parse(element.find("online", nmap), nmap)
        offline = EMLOffline.parse(element.find("offline", nmap), nmap)
        inline = EMLInline.parse(element.find("inline", nmap), nmap)
        return EMLDistribution(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            online=online,
            offline=offline,
            inline=inline,
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element with EMLDistribution instance information.

        Returns
        -------
        lxml.etree.Element
            XML element object
        """
        dist_elem = super().to_element()
        dist_elem = self._to_element_(dist_elem)
        dist_elem.append(self.online.to_element()) if self.online is not None else None
        dist_elem.append(self.offline.to_element()) if self.offline is not None else None
        dist_elem.append(self.inline.to_element()) if self.inline is not None else None
        return dist_elem
