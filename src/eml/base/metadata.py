from __future__ import annotations

import datetime as dt
from typing import Dict

import lxml.etree as et

from dwca.xml import XMLObject


class EMLGbifMetadata(XMLObject):
    def __init__(self) -> None:
        super().__init__()
        self.__date_stamp__ = None
        self.__hierarchy_level__ = None
        self.__citation__ = None
        self.__resource_logo_url__ = None

    def to_element(self) -> et.Element:
        root = et.Element("gbif")
        if self.__date_stamp__ is not None:
            date_stamp = et.SubElement(root, "dateStamp")
            date_stamp.text = self.__date_stamp__.isoformat()
            root.append(date_stamp)
        if self.__hierarchy_level__ is not None:
            hierarchy_level = et.SubElement(root, "hierarchyLevel")
            hierarchy_level.text = self.__hierarchy_level__
        if self.__citation__ is not None:
            citation = et.SubElement(root, "citation")
            citation.text = self.__citation__
        if self.__resource_logo_url__ is not None:
            resource_logo = et.SubElement(root, "resourceLogoUrl")
            resource_logo.text = self.__resource_logo_url__
        return root

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> EMLGbifMetadata:
        assert element.tag == 'gbif', "GBIF tag not included"
        gbif_metadata = EMLGbifMetadata()
        date_stamp = element.find("dateStamp")
        if date_stamp is not None:
            gbif_metadata.__date_stamp__ = dt.datetime.fromisoformat(date_stamp.text)
        hierarchy_level = element.find("hierarchyLevel")
        if hierarchy_level is not None:
            gbif_metadata.__hierarchy_level__ = hierarchy_level.text
        citation = element.find("citation")
        if citation is not None:
            gbif_metadata.__citation__ = citation.text
        resource_logo = element.find("resourceLogoUrl")
        if resource_logo is not None:
            gbif_metadata.__resource_logo_url__ = resource_logo.text
        return gbif_metadata


class EMLMetadata(XMLObject):
    def __init__(self) -> None:
        super().__init__()
        self.__gbif__ = None
        return

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> EMLMetadata:
        assert element.tag == "metadata", "Metadata tag not included"
        metadata = EMLMetadata()
        gbif_metadata = element.find("gbif")
        if gbif_metadata is not None:
            metadata.__gbif__ = EMLGbifMetadata.parse(gbif_metadata, nsmap)
        return metadata

    def to_element(self) -> et.Element:
        root = et.Element("additionalMetadata")
        actual_root = et.Element("metadata")
        root.append(actual_root)
        if self.__gbif__ is not None:
            actual_root.append(self.__gbif__.to_element())
        return root
