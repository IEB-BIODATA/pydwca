from __future__ import annotations

from enum import Enum
from typing import Dict, List, Union

from lxml import etree as et

from dwca.utils import CamelCaseEnum
from eml.types import EMLObject, _NoTagObject, Scope, IndividualName, OrganizationName, PositionName, EMLAddress, \
    EMLPhone, I18nString


class Role(CamelCaseEnum):
    """
    The role the party played with respect to the resource.
    """
    AUTHOR = 0
    CONTENT_PROVIDER = 1
    CUSTODIAN_STEWARD = 2
    DISTRIBUTOR = 3
    EDITOR = 4
    METADATA_PROVIDER = 5
    ORIGINATOR = 6
    POINT_OF_CONTACT = 7
    PRINCIPAL_INVESTIGATOR = 8
    PROCESSOR = 9
    PUBLISHER = 10
    USER = 11


class ResponsibleParty(EMLObject, _NoTagObject):
    """
    The individual, organization, or role associated with a resource.

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
    individual_name : IndividualName, optional
        The full name of the person being described.
    organization_name : OrganizationName, optional
        The full name of the organization being described.
    position_name : PositionName, optional
        The name of the title or position associated with the resource.
    address : List[EMLAddress], optional
        A list of full addresses information for a given responsible party entry.
    phone : List[EMLPhone], optional
        A list of phone information about the contact.
    mail : List[str or I18nString], optional
        A list of email addresses of the contact.
    url : List[str], optional
        A list of links to associated online information, usually a website.
    """
    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            individual_name: IndividualName = None,
            organization_name: OrganizationName = None,
            position_name: PositionName = None,
            address: List[EMLAddress] = None,
            phone: List[EMLPhone] = None,
            mail: List[Union[str, I18nString]] = None,
            url: List[str] = None,
    ) -> None:
        EMLObject.__init__(self, _id, scope, system, referencing, references_system)
        _NoTagObject.__init__(self)
        if not self.referencing:
            assert_msg = ("At least one of the following must be given: individial_name, "
                          "organization_name or position_name")
            assert individual_name is not None or organization_name is not None or position_name is not None, assert_msg
        self.__individual__ = individual_name
        self.__organization__ = organization_name
        self.__position__ = position_name
        self.__address__: List[EMLAddress] = list()
        if address is not None:
            self.__address__.extend(address)
        self.__phone__: List[EMLPhone] = list()
        if phone is not None:
            self.__phone__.extend(phone)
        self.__mail__: List[I18nString] = list()
        if mail is not None:
            self.__mail__.extend([I18nString(m) for m in mail])
        self.__url__: List[str] = list()
        if url is not None:
            self.__url__.extend(url)
        return

    @property
    def individual_name(self) -> IndividualName:
        """IndividualName: the full name of the person being described."""
        return self.__individual__

    @property
    def organization_name(self) -> OrganizationName:
        """OrganizationName: The full name of the organization being described."""
        return self.__organization__

    @property
    def position_name(self) -> PositionName:
        """PositionName: The name of the title or position associated with the resource."""
        return self.__position__

    @property
    def address(self) -> List[EMLAddress]:
        """List[EMLAddress]: A list of full addresses information for a given responsible party entry."""
        return self.__address__

    @property
    def phone(self) -> List[EMLPhone]:
        """List[EMLPhone]: A list of phon information about the contact."""
        return self.__phone__

    @property
    def mail(self) -> List[I18nString]:
        """List[I18nString]: A list of email addresses of the contact."""
        return self.__mail__

    @property
    def url(self) -> List[str]:
        """List[str]: A list of links to associated online information, usually a website."""
        return self.__url__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> ResponsibleParty:
        """
        Generate a Responsible Party referencing another Responsible Party.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        ResponsibleParty
            Object parsed that reference another responsible party on document.
        """
        references = element.find("references")
        return ResponsibleParty(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> ResponsibleParty:
        """
        Generate a Responsible Party that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        ResponsibleParty
            Object parsed.
        """
        return ResponsibleParty(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            individual_name=IndividualName.parse(element.find("individualName", None), nmap),
            organization_name=OrganizationName.parse(element.find("organizationName", None), nmap),
            position_name=PositionName.parse(element.find("positionName", None), nmap),
            address=[EMLAddress.parse(address, nmap) for address in element.findall("address", nmap)],
            phone=[EMLPhone.parse(phone, nmap) for phone in element.findall("phone", nmap)],
            mail=[I18nString.parse(mail, nmap) for mail in element.findall("electronicMailAddress", nmap)],
            url=[url.text for url in element.findall("onlineUrl", nmap)],
        )

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the Responsible Party object.

        Returns
        -------
        lxml.tree.Element
            Object in the XML Element format.

        Raises
        ------
        RuntimeError
            If tag is not set before calling this method.
        """
        resp_party = _NoTagObject.to_element(self)
        resp_party = self._to_element_(resp_party)
        references = self.generate_references_element()
        if references is None:
            if self.individual_name is not None:
                resp_party.append(self.individual_name.to_element())
            if self.organization_name is not None:
                resp_party.append(self.organization_name.to_element())
            if self.position_name is not None:
                resp_party.append(self.position_name.to_element())
            for address in self.address:
                resp_party.append(address.to_element())
            for phone in self.phone:
                resp_party.append(phone.to_element())
            for email in self.mail:
                email.set_tag("electronicMailAddress")
                resp_party.append(email.to_element())
            for url in self.__url__:
                url_elem = et.Element("onlineUrl")
                url_elem.text = url
                resp_party.append(url_elem)
        return resp_party

    @classmethod
    def get_role(cls, element: et.Element, nmap: Dict) -> Role:
        """
        Get role for an XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element with role on it.
        nmap : Dict
            Namespace.

        Returns
        -------
        Role
            Value of the role inside the XML element.
        """
        role_elem = element.find("role", nmap)
        return Role.get_enum(role_elem.text)

    def __str__(self) -> str:
        position_name = "" if self.position_name is None else f"{self.position_name}"
        if self.organization_name is None:
            organization_name = position_name
        else:
            if len(position_name) == 0:
                organization_name = f"{self.organization_name}"
            else:
                organization_name = f"{position_name} at {self.organization_name}"
        if self.individual_name is None:
            return organization_name
        else:
            if len(organization_name) > 0:
                organization_name = f" ({organization_name})"
            return f"{self.individual_name}{organization_name}"
