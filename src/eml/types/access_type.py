from __future__ import annotations

from typing import Dict, Union, List

from lxml import etree as et

from dwca.utils import CamelCaseEnum
from eml.types import EMLObject, Scope, _NoTagObject


class AccessOrder(CamelCaseEnum):
    ALLOW_FIRST = 0
    DENY_FIRST = 1


class AccessPermission(CamelCaseEnum):
    READ = 0
    WRITE = 1
    CHANGE_PERMISSION = 2
    ALL = 3


class AccessRole(_NoTagObject):
    """
    Access Rules define a user's access to a resource.

    Parameters
    ----------
    principal : List[str]
        The user or group (principal) for which the access control applies.
    permission: List[AccessPermission]
         The type of permission being granted or denied.
    """
    def __init__(self, principal: List[str], permission: List[AccessPermission]) -> None:
        super().__init__()
        if len(principal) == 0:
            raise ValueError("At least one principal must be given")
        self.__principal__ = principal
        if len(permission) == 0:
            raise ValueError("At least one permission must be given")
        self.__permission__ = permission
        return

    @property
    def principal(self) -> List[str]:
        """
        List[str]: The user or group (principal) for which the access control applies.
        """
        return self.__principal__

    @property
    def permission(self) -> List[AccessPermission]:
        """List[AccessPermission]: The type of permission being granted or denied."""
        return self.__permission__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> AccessRole | None:
        """
        Generate a AccessRole instance from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        AccessRole
            An instance of AccessRole.
        """
        if element is None:
            return None
        principal = list()
        for prin_elem in element.findall("principal"):
            principal.append(prin_elem.text)
        permission = list()
        for perm_elem in element.findall("permission"):
            permission.append(AccessPermission.get_enum(perm_elem.text))
        access_role = AccessRole(principal, permission)
        access_role.__namespace__ = nmap
        return access_role

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance using this Access Role object.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        element = super().to_element()
        for principal in self.principal:
            prin_elem = self.object_to_element("principal")
            prin_elem.text = principal
            element.append(prin_elem)
        for permission in self.permission:
            perm_elem = self.object_to_element("permission")
            perm_elem.text = permission.to_camel_case()
            element.append(perm_elem)
        return element


class AccessType(EMLObject):
    """
    Access control rules for the entire resource, which can be overridden by access rules in distribution trees.

    Parameters
    ----------
    auth_system : str
        The authentication system is used to verify the user or group to whom access is allowed or denied.
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
    order: Order, optional
        The order in which the allow and deny rules should be applied.
    allow: AccessRole
        A rule that grants a permission type. Mandatory if AccessType is not a reference.
    deny: AccessRole
        A rule that revokes a permission type. Mandatory if AccessType is not a reference.
    """
    PRINCIPAL_TAG = "access"

    def __init__(
            self, auth_system: str,
            _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            order: Union[AccessOrder, str] = AccessOrder.ALLOW_FIRST,
            allow: AccessRole = None,
            deny: AccessRole = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        self.__auth__ = auth_system
        if isinstance(order, AccessOrder):
            self.__order__ = order
        elif isinstance(order, str):
            self.__order__ = AccessOrder.get_enum(order)
        else:
            raise TypeError(f"'order' parameter must be a AccessOrder or sting, not a {type(order)}")
        self.__allow__ = allow
        self.__deny__ = deny
        return

    @property
    def auth_system(self) -> str:
        """str: The authentication system is used to verify the user or group to whom access is allowed or denied."""
        return self.__auth__

    @property
    def order(self) -> AccessOrder:
        """AccessOrder: The order in which the allow and deny rules should be applied."""
        return self.__order__

    @property
    def allow(self) -> AccessRole:
        """AccessRole: A rule that grants a permission type."""
        return self.__allow__

    @property
    def deny(self) -> AccessRole:
        """AccessRole: A rule that revokes a permission type."""
        return self.__deny__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> AccessType:
        """
        Generate an AccessType object that references another AccessType.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        AccessType
            Instance of AccessType
        """
        references = element.find("references", nmap)
        return AccessType(
            auth_system=element.get("authSystem"),
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLObject:
        """
        Generate an AccessType object that does not reference another AccessType.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        AccessType
            Instance of AccessType
        """
        return AccessType(
            auth_system=element.get("authSystem"),
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            allow=AccessRole.parse(element.find("allow", nmap), nmap),
            deny=AccessRole.parse(element.find("deny", nmap), nmap),
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element instance using this object.

        Returns
        -------
        lxml.etree.Element
            An XML element instance.
        """
        element = super().to_element()
        element = self._to_element_(element)
        element.set("authSystem", self.auth_system)
        element.set("order", self.order.to_camel_case())
        if self.referencing:
            return element
        self.allow.set_tag("allow")
        element.append(self.allow.to_element())
        self.deny.set_tag("deny")
        element.append(self.deny.to_element())
        return element
