from __future__ import annotations

from enum import Enum
from typing import Dict, List, Tuple, Any

from lxml import etree as et

from dwca.xml import XMLObject
from eml.types import EMLObject, Scope, ExtensionString, EMLTextType


class EMLOnline(XMLObject):
    """
    Online distribution information.

    Parameters
    ----------
    online_description : I18nString or str, optional
        Brief description of the content of online.
    url : str, optional
        A URL from which this resource can be downloaded or information can be obtained about downloading it.
    url_function : EMLOnline.FunctionType, optional
        "information" when the URL meant for informational purposes or "download" URL returns the data stream itself.
    connection : EMLOnline.Connection, optional
         A connection to a data service.
    connection_definition : EMLOnline.ConnectionDefinition, optional
        The definition of a connection that will be used in another location in the EML document.
    """
    PRINCIPAL_TAG = "online"

    class FunctionType(Enum):
        """
        Function of the URL.
        """
        DOWNLOAD = 0
        INFORMATION = 1

    class ParameterDefinition(XMLObject):
        """
        The definition of a parameter that is needed to properly use this connection scheme.

        Parameters
        ----------
        name : str
            The Name of a parameter that is needed to properly use this connection scheme.
        definition : str
            The definition of a parameter that is needed to properly use this connection scheme.
        default_value : str, optional
            The default value for a parameter that is needed to properly use this connection scheme.
        """
        PRINCIPAL_TAG = "parameterDefinition"
        """str: Principal tag `parameterDefinition`"""

        def __init__(self, name: str, definition: str, default_value: str = None) -> None:
            super().__init__()
            self.__name__ = name
            self.__def__ = definition
            self.__default__ = default_value
            return

        @property
        def name(self) -> str:
            """str: The Name of a parameter that is needed to properly use this connection scheme."""
            return self.__name__

        @property
        def definition(self) -> str:
            """str: The definition of a parameter that is needed to properly use this connection scheme."""
            return self.__def__

        @property
        def default_value(self) -> str:
            """str: The default value for a parameter that is needed to properly use this connection scheme."""
            return self.__default__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> EMLOnline.ParameterDefinition | None:
            """
            Parse an XML element into a ParameterDefinition object

            Parameters
            ----------
            element : xml.etree.Element
                XML element to be parsed
            nmap : Dict
                Namespace

            Returns
            -------
            EMLOnline.ParameterDefinition
                Instance with the information of the XML element
            """
            name_elem = element.find("name", nmap)
            def_elem = element.find("definition", nmap)
            default_elem = element.find("defaultValue", nmap)
            default_value = None
            if default_elem is not None:
                default_value = default_elem.text if default_elem.text is not None else ""
            param_def = EMLOnline.ParameterDefinition(
                name=name_elem.text if name_elem.text is not None else "",
                definition=def_elem.text if def_elem.text is not None else "",
                default_value=default_value
            )
            param_def.__namespace__ = nmap
            return param_def

        def to_element(self) -> et.Element:
            """
            Generate an XML element from Parameter Definition instance

            Returns
            -------
            xml.etree.Element
                XML element instance with the Parameter Definition information
            """
            param_def = super().to_element()
            name_elem = self.object_to_element("name")
            name_elem.text = self.name
            param_def.append(name_elem)
            def_elem = self.object_to_element("definition")
            def_elem.text = self.definition
            param_def.append(def_elem)
            if self.default_value is not None:
                default_elem = self.object_to_element("defaultValue")
                default_elem.text = self.default_value
                param_def.append(default_elem)
            return param_def

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, EMLOnline.ParameterDefinition):
                return (
                    self.name == other.name and
                    self.definition == other.definition
                )
            else:
                return False

        def __gt__(self, other: EMLOnline.ParameterDefinition) -> bool:
            if not isinstance(other, EMLOnline.ParameterDefinition):
                raise TypeError(f"'>' not supported between instances of 'EML.ParameterDefinition' and '{type(other)}'")
            else:
                return self.name > other.name

        def __ge__(self, other: EMLOnline.ParameterDefinition) -> bool:
            return self > other or self == other

        def __lt__(self, other: EMLOnline.ParameterDefinition) -> bool:
            if not isinstance(other, EMLOnline.ParameterDefinition):
                raise TypeError(f"'<' not supported between instances of 'EML.ParameterDefinition' and '{type(other)}'")
            else:
                return self.name < other.name

        def __le__(self, other: EMLOnline.ParameterDefinition) -> bool:
            return self < other or self == other

    class ConnectionDefinition(EMLObject):
        """
        Definition of the connection protocol.

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
        scheme_name : ExtensionString, optional
            The name of the scheme used to identify this connection.
        description : EMLTextType, optional
            The description of the scheme used to identify this connection.
        parameters : List[EMLOnline.ParameterDefinition], optional
            A list of definitions of a parameter that is needed to properly use this connection scheme.
        """
        PRINCIPAL_TAG = "connectionDefinition"
        """str: Principal tag `connectionDefinition`"""

        def __init__(
                self, _id: str = None,
                scope: Scope = Scope.DOCUMENT,
                system: str = None,
                referencing: bool = False,
                references_system: str = None,
                scheme_name: ExtensionString = None,
                description: EMLTextType = None,
                parameters: List[EMLOnline.ParameterDefinition] = None,
        ) -> None:
            super().__init__(_id, scope, system, referencing, references_system)
            self.__scheme_name__ = scheme_name
            self.__description__ = description
            self.__param__: List[EMLOnline.ParameterDefinition] = list()
            if parameters is not None:
                self.__param__.extend(parameters)
            return

        @property
        def scheme_name(self) -> ExtensionString:
            """ExtensionString: The name of the scheme used to identify this connection."""
            return self.__scheme_name__

        @property
        def description(self) -> EMLTextType:
            """EMLTextType: The description of the scheme used to identify this connection."""
            return self.__description__

        @property
        def parameters(self) -> List[EMLOnline.ParameterDefinition]:
            """
            List[EMLOnline.ParameterDefinition]: List of parameters that are needed to use this connection scheme.
            """
            return self.__param__

        @classmethod
        def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLOnline.ConnectionDefinition:
            """
            Generate a ConnectionDefinition object referencing another from an XML element

            Parameters
            ----------
            element : lxml.etree.Element
                XML element object to parse
            nmap : Dict
                Namespace

            Returns
            -------
            EMLOnline.ConnectionDefinition
                Instance parsed from XML Element
            """
            references = element.find("references", nmap)
            return EMLOnline.ConnectionDefinition(
                _id=references.text,
                scope=cls.get_scope(element),
                system=element.get("system", None),
                referencing=True,
                references_system=references.get("system", None),
            )

        @classmethod
        def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLOnline.ConnectionDefinition:
            """
            Generate a ConnectionDefinition object from an XML element

            Parameters
            ----------
            element : lxml.etree.Element
                XML element object to parse
            nmap : Dict
                Namespace

            Returns
            -------
            EMLOnline.ConnectionDefinition
                Instance parsed from XML Element
            """
            scheme_elem = element.find("schemeName", nmap)
            if scheme_elem is not None:
                scheme_name = ExtensionString.parse(scheme_elem, nmap)
            else:
                scheme_name = None
            des_elem = element.find("description", nmap)
            if des_elem is not None:
                description = EMLTextType.parse(des_elem, nmap)
            else:
                description = None
            parameters = list()
            for param_elem in element.findall("parameterDefinition", nmap):
                parameters.append(EMLOnline.ParameterDefinition.parse(param_elem, nmap))
            return EMLOnline.ConnectionDefinition(
                _id=element.get("id", None),
                scope=cls.get_scope(element),
                system=element.get("system", None),
                referencing=False,
                scheme_name=scheme_name,
                description=description,
                parameters=parameters,
            )

        def to_element(self) -> et.Element:
            """
            Generate an XML element with the instance information.

            Returns
            -------
            lxml.etree.Element
                XML Element instance
            """
            conn_def = super().to_element()
            conn_def = self._to_element_(conn_def)
            if self.referencing:
                return conn_def
            if self.scheme_name is not None:
                self.scheme_name.set_tag("schemeName")
                conn_def.append(self.scheme_name.to_element())
            if self.description is not None:
                self.description.set_tag("description")
                conn_def.append(self.description.to_element())
            for parameter in self.parameters:
                conn_def.append(parameter.to_element())
            return conn_def

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, EMLOnline.ConnectionDefinition):
                parameter_equals = self.parameters is None and other.parameters is None
                if not parameter_equals:
                    if self.parameters is not None and other.parameters is not None:
                        parameter_equals = sorted(self.parameters) == sorted(other.parameters)
                return (
                    super().__eq__(other) and
                    self.scheme_name == other.scheme_name and
                    self.description == other.description and
                    parameter_equals
                )
            else:
                return False

    class Connection(EMLObject):
        """
        A description of the information needed to make an application connection to a data service.

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
        connection_definition : EMLOnline.ConnectionDefinition, optional
            Definition of the connection protocol.
        parameters : List[Tuple[str, str]], optional
            A parameter to be used to make this connection.
        """
        PRINCIPAL_TAG = "connection"

        def __init__(
                self, _id: str = None,
                scope: Scope = Scope.DOCUMENT,
                system: str = None,
                referencing: bool = False,
                references_system: str = None,
                connection_definition: EMLOnline.ConnectionDefinition = None,
                parameters: List[Tuple[str, str]] = None,
        ) -> None:
            super().__init__(_id, scope, system, referencing, references_system)
            self.__conn_def__ = connection_definition
            self.__param__ = list()
            if parameters is not None:
                self.__param__.extend(parameters)
            return

        @property
        def connection_definition(self) -> EMLOnline.ConnectionDefinition:
            """
            EMLOnline.ConnectionDefinition: Definition of the connection protocol.
            """
            return self.__conn_def__

        @property
        def parameters(self) -> List[Tuple[str, str]]:
            """List[Tuple[str, str]]: A parameter to be used to make this connection."""
            return self.__param__

        @classmethod
        def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLOnline.Connection:
            """
            Generate a Connection instance referencing another instance.

            Parameters
            ----------
            element : lxml.etree.Element
                An XML element instance to parse.
            nmap : Dict
                Namespace.

            Returns
            -------
            EMLOnline.Connection
                Instance of Connection referencing another.
            """
            references = element.find("references", nmap)
            return EMLOnline.Connection(
                _id=references.text,
                scope=cls.get_scope(element),
                system=element.get("system", None),
                referencing=True,
                references_system=references.get("system", None)
            )

        @classmethod
        def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLOnline.Connection:
            """
            Generate a Connection instance from an XML element.

            Parameters
            ----------
            element : lxml.etree.Element
                An XML element instance to parse.
            nmap : Dict
                Namespace.

            Returns
            -------
            EMLOnline.Connection
                Instance with the information from the XML element.
            """
            des_elem = element.find("connectionDefinition", nmap)
            if des_elem is not None:
                conn_des = EMLOnline.ConnectionDefinition.parse(des_elem, nmap)
            else:
                conn_des = None
            parameters = list()
            for param_elem in element.findall("parameter", nmap):
                parameters.append((
                    param_elem.find("name").text,
                    param_elem.find("value").text,
                ))
            return EMLOnline.Connection(
                _id=element.get("id", None),
                scope=cls.get_scope(element),
                system=element.get("system", None),
                referencing=False,
                connection_definition=conn_des,
                parameters=parameters,
            )

        def to_element(self) -> et.Element:
            """
            Generate an XML Element with instance information.

            Returns
            -------
            lxml.etree.Element
                An XML Element instance.
            """
            conn_elem = super().to_element()
            conn_elem = self._to_element_(conn_elem)
            if self.referencing:
                return conn_elem
            if self.connection_definition is not None:
                conn_elem.append(self.connection_definition.to_element())
            for parameter in self.parameters:
                param_elem = self.object_to_element("parameter")
                name_elem = self.object_to_element("name")
                name_elem.text = parameter[0]
                param_elem.append(name_elem)
                value_elem = self.object_to_element("value")
                value_elem.text = parameter[1]
                param_elem.append(value_elem)
                conn_elem.append(param_elem)
            return conn_elem

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, EMLOnline.Connection):
                return (
                    super().__eq__(other) and
                    self.connection_definition == other.connection_definition and
                    sorted(self.parameters) == sorted(other.parameters)
                )
            else:
                return False

    def __init__(
            self, online_description: str = None,
            url: str = None,
            url_function: EMLOnline.FunctionType = None,
            connection: EMLOnline.Connection = None,
            connection_definition: EMLOnline.ConnectionDefinition = None
    ) -> None:
        super().__init__()
        conn = 0
        if url is not None:
            conn += 1
        if connection is not None:
            conn += 1
        if connection_definition is not None:
            conn += 1
        if conn > 1:
            raise ValueError(
                "Just one of the following can be given: "
                "`online_description`, `connection` or "
                "`connection_definition`"
            )
        self.__online_description__ = online_description
        self.__url__ = url
        if self.__url__ is not None:
            self.__url_func__ = EMLOnline.FunctionType.DOWNLOAD
        else:
            self.__url_func__ = None
        if url_function is not None:
            self.__url_func__ = url_function
        self.__conn__ = connection
        self.__conn_def__ = connection_definition
        return

    @property
    def online_description(self) -> str:
        """str: Brief description of the content of online."""
        return self.__online_description__

    @property
    def url(self) -> str:
        """str: A URL from which this resource can be downloaded or information can be obtained about downloading it."""
        return self.__url__

    @property
    def url_function(self) -> EMLOnline.FunctionType:
        """EMLOnline.FunctionType: Function of the url."""
        return self.__url_func__

    @property
    def connection(self) -> EMLOnline.Connection:
        """EMLOnline.Connection: A connection to a data service."""
        return self.__conn__

    @property
    def connection_definition(self) -> EMLOnline.ConnectionDefinition:
        """
        EMLOnline.ConnectionDefinition: Definition of the connection protocol.
        """
        return self.__conn_def__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLOnline | None:
        """
        Generate an EMLOnline instance from an XML element.

        Parameters
        ----------
        element : lxml.etree.Element
            An XML element instance.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLOnline
            Instance parsed.
        """
        if element is None:
            return None
        onl_des = element.find("onlineDescription", nmap)
        if onl_des is not None:
            online_des = onl_des.text
        else:
            online_des = None
        url_elem = element.find("url", nmap)
        url_func = None
        if url_elem is not None:
            url = url_elem.text
            got_url_func = url_elem.get("function", "download")
            for candid_func in EMLOnline.FunctionType:
                if got_url_func.lower() == candid_func.name.lower():
                    url_func = candid_func
                    break
        else:
            url = None
        conn_elem = element.find("connection", nmap)
        if conn_elem is not None:
            conn = EMLOnline.Connection.parse(conn_elem, nmap)
        else:
            conn = None
        des_elem = element.find("connectionDefinition", nmap)
        if des_elem is not None:
            conn_des = EMLOnline.ConnectionDefinition.parse(des_elem, nmap)
        else:
            conn_des = None
        online = EMLOnline(
            online_description=online_des,
            url=url,
            url_function=url_func,
            connection=conn,
            connection_definition=conn_des
        )
        online.__namespace__ = nmap
        return online

    def to_element(self) -> et.Element:
        """
        Generate an XML element from an Online instance.

        Returns
        -------
        lxml.etree.Element
            XML element with EMLOnline instance information.
        """
        online_elem = super().to_element()
        if self.online_description is not None:
            desc_elem = self.object_to_element("onlineDescription")
            desc_elem.text = self.online_description
            online_elem.append(desc_elem)
        if self.url is not None:
            url_elem = self.object_to_element("url")
            url_elem.set("function", self.url_function.name.lower())
            url_elem.text = self.url
            online_elem.append(url_elem)
        if self.connection is not None:
            online_elem.append(self.connection.to_element())
        if self.connection_definition is not None:
            online_elem.append(self.connection_definition.to_element())
        return online_elem
