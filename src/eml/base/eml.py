from __future__ import annotations

from typing import Dict

from lxml import etree as et

from dwca.utils import Language
from dwca.xml import XMLObject
from eml.base import EMLMetadata
from eml.resources import EMLResource, EMLDataset, EMLCitation, EMLProtocol, EMLSoftware


class EML(XMLObject):
    """
    Class representing an `Ecological Metadata Language <https://eml.ecoinformatics.org/>`_

    Parameters
    ----------
    package_id : str
        A globally unique identifier for the data package described by this EML that can be used to cite it elsewhere.
    system : str
        The data management system within which an identifier is in scope and therefore unique.
    scope : str, optional
        The scope of the identifier.
    language: str
        Language abbreviation to be used, defaults to `"eng"`
    """
    PRINCIPAL_TAG = "eml"
    """str: Principal tag `eml`"""
    NAMESPACE_TAG = "eml"
    """str: Namespace tag `eml`, to be replace for `{uri}tag`"""

    def __init__(
            self,
            package_id: str,
            system: str,
            resource_type: EMLResource,
            scope: str = None,
            language: str = "eng"
    ) -> None:
        super().__init__()
        self.__schema_location__ = ""
        self.__package__ = package_id
        self.__system__ = system
        self.__scope__ = scope
        for lang in Language:
            if lang.name.lower() == language.lower():
                self.__lang__ = lang
        self.__access__ = None
        self.__resource_type__ = resource_type
        if resource_type == EMLResource.DATASET:
            self.__resource__ = EMLDataset()
        elif resource_type == EMLResource.CITATION:
            self.__resource__ = EMLCitation()
        elif resource_type == EMLResource.SOFTWARE:
            self.__resource__ = EMLSoftware()
        elif resource_type == EMLResource.PROTOCOL:
            self.__resource__ = EMLProtocol()
        else:
            raise ValueError(f"{resource_type.name.lower()} is not allowed")
        self.__eml_annotations__ = None
        self.__additional__ = list()
        return

    @property
    def package_id(self) -> str:
        return self.__package__

    @property
    def system(self) -> str:
        return self.__system__

    @property
    def scope(self) -> str:
        return self.__scope__

    @property
    def language(self) -> Language:
        return self.__lang__

    @property
    def resource_type(self) -> EMLResource:
        return self.__resource_type__

    @classmethod
    def parse(cls, element: et.Element, nsmap: Dict) -> EML:
        assert element.get("packageId", None) is not None, "`packageId` attribute is not present in document"
        found = False
        resource_found = EMLResource.DATASET
        for resource_type in EMLResource:
            if found:
                if element.find(resource_type.name.lower()) is not None:
                    raise ValueError(
                        f"More than one resource found: {resource_found.name.lower()} and {resource_type.name.lower()}"
                    )
            else:
                resource_element = element.find(resource_type.name.lower())
                if resource_element is not None:
                    found = True
                    resource_found = resource_type
        if not found:
            raise ValueError(f"""One of the following must be present: {', '.join(
                [eml_resource.name.lower() for eml_resource in EMLResource]
            )}""")
        print(resource_found)
        eml = EML(
            element.get("packageId"),
            element.get("system"),
            resource_found,
            element.get("scope", None),
            element.get(f"{{{nsmap['xml']}}}lang", "eng")
        )
        for add_metadata in element.findall("additionalMetadata", nsmap):
            eml_metadata = EMLMetadata.parse(add_metadata.find("metadata"), nsmap)
            eml_metadata.__namespace__ = nsmap
            eml.__additional__.append(eml_metadata)
        return eml

    def to_element(self) -> et.Element:
        root = et.Element(self.get_principal_tag())
        root.set("packageId", self.__package__)
        root.set(f"{{{self.NAMESPACES['xsi']}}}schemaLocation", self.__schema_location__)
        root.set("system", self.__system__)
        root.set("scope", self.__scope__)
        root.set(f"{{{self.NAMESPACES['xml']}}}lang", self.__lang__.name.lower())
        root.append(self.__dataset__.to_element())
        root.append(self.__metadata__.to_element())
        return root
