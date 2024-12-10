from __future__ import annotations

from typing import Dict, List

from lxml import etree as et

from eml.resources import Resource
from eml.types import ResponsibleParty, EMLTextType, Maintenance, Methods, ResearchProject


class EMLDataset(Resource):
    """
    Dataset represents the base type for the dataset element on an EML document.

    Parameters
    ----------
    purpose : EMLTextType, optional
        A synopsis of the purpose of this dataset.
    introduction : EMLTextType, optional
        An overview of the background and context for the dataset.
    getting_started : EMLTextType, optional
        A high level overview of interpretation, structure, and content of the dataset.
    acknowledgement : EMLTextType, optional
        Text that acknowledges funders and other key contributors.
    maintenance : Maintenance, optional
        A description of the maintenance of this data resource.
    contact : List[ResponsibleParty]
        The contact for this dataset.
    publisher : ResponsibleParty, optional
        The publisher of this data set.
    pub_place : str, optional
        The location that the resource was published.
    methods : Methods, optional
        The methods field documents scientific methods used in the collection of this dataset.
    project : ResearchProject, optional
        The project in which this dataset was collected.

    Other Parameters
    ----------------
    **kwargs : :class:`eml.resources.resource.Resource` parameters.
        The parameters of every type of Resource.
    """
    PRINCIPAL_TAG = "dataset"

    def __init__(
            self,
            purpose: EMLTextType = None,
            introduction: EMLTextType = None,
            getting_started: EMLTextType = None,
            acknowledgements: EMLTextType = None,
            maintenance: Maintenance = None,
            contact: List[ResponsibleParty] = None,
            publisher: ResponsibleParty = None,
            pub_place: str = None,
            methods: Methods = None,
            project: ResearchProject = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__contact__ = list()
        if self.referencing:
            return
        if contact is None or len(contact) == 0:
            raise ValueError("No contact provided.")
        self.__contact__.extend(contact)
        self.__purpose__ = purpose
        self.__intro__ = introduction
        self.__get_started__ = getting_started
        self.__acknowledge__ = acknowledgements
        self.__maint__ = maintenance
        self.__publisher__ = publisher
        self.__pub_place__ = pub_place
        self.__methods__ = methods
        self.__project__ = project
        return

    @property
    def contacts(self) -> List[ResponsibleParty]:
        """List[ResponsibleParty]: The contact for this dataset."""
        return self.__contact__

    @property
    def purpose(self) -> EMLTextType:
        """EMLTextType: A synopsis of the purpose of this dataset."""
        return self.__purpose__

    @property
    def introduction(self) -> EMLTextType:
        """EMLTextType: An overview of the background and context for the dataset."""
        return self.__intro__

    @property
    def getting_started(self) -> EMLTextType:
        """EMLTextType: A high level overview of interpretation, structure, and content of the dataset."""
        return self.__get_started__

    @property
    def acknowledgements(self) -> EMLTextType:
        """EMLTextType: Text that acknowledges funders and other key contributors."""
        return self.__acknowledge__

    @property
    def maintenance(self) -> Maintenance:
        """Maintenance: A description of the maintenance of this data resource."""
        return self.__maint__

    @property
    def publisher(self) -> ResponsibleParty:
        """ResponsibleParty: The publisher of this data set."""
        return self.__publisher__

    @property
    def pub_place(self) -> str:
        """str: The location that the resource was published."""
        return self.__pub_place__

    @property
    def methods(self) -> Methods:
        """Methods: The methods field documents scientific methods used in the collection of this dataset."""
        return self.__methods__

    @property
    def project(self) -> ResearchProject:
        """ResearchProject: The project in which this dataset was collected."""
        return self.__project__

    # TODO: Implement other attributes (https://eml.ecoinformatics.org/schema/eml_xsd#eml_dataset)

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> EMLDataset:
        """
        Generate an EML Dataset referencing another EML Dataset.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references another dataset.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLDataset
            Object parsed that reference another dataset.
        """
        kwargs = super().parse_kwargs(element, nmap)
        return EMLDataset(**kwargs)

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> EMLDataset:
        """
        Generate an EML Dataset that do not reference another dataset.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        EMLDataset
            Object parsed.
        """
        kwargs = super().parse_kwargs(element, nmap)
        purpose_elem = element.find("purpose", nmap)
        purpose = None if purpose_elem is None else EMLTextType.parse(purpose_elem, nmap)
        intro_elem = element.find("introduction", nmap)
        introduction = None if intro_elem is None else EMLTextType.parse(intro_elem, nmap)
        get_started_elem = element.find("gettingStarted", nmap)
        get_started = None if get_started_elem is None else EMLTextType.parse(get_started_elem, nmap)
        acknowledge_elem = element.find("acknowledgements", nmap)
        acknowledgements = None if acknowledge_elem is None else EMLTextType.parse(acknowledge_elem, nmap)
        maint_elem = element.find("maintenance", nmap)
        maint = None if maint_elem is None else Maintenance.parse(maint_elem, nmap)
        contact = list()
        for contact_elem in element.findall("contact", nmap):
            contact.append(ResponsibleParty.parse(contact_elem, nmap))
        publisher_elem = element.find("publisher", nmap)
        publisher = None if publisher_elem is None else ResponsibleParty.parse(publisher_elem, nmap)
        pub_place_elem = element.find("pubPlace", nmap)
        pub_place = None if pub_place_elem is None else pub_place_elem.text
        methods_elem = element.find("methods", nmap)
        methods = None if methods_elem is None else Methods.parse(methods_elem, nmap)
        project_elem = element.find("project", nmap)
        project = None if project_elem is None else ResearchProject.parse(project_elem, nmap)
        return EMLDataset(
            purpose=purpose,
            introduction=introduction,
            getting_started=get_started,
            acknowledgements=acknowledgements,
            maintenance=maint,
            contact=contact,
            publisher=publisher,
            pub_place=pub_place,
            methods=methods,
            project=project,
            **kwargs
        )

    def to_element(self) -> et.Element:
        """
        Generates an XML `Element` from this instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` from this instance
        """
        dataset = super().to_element()
        if self.referencing:
            return dataset
        for contact in self.contacts:
            contact.set_tag("contact")
            dataset.append(contact.to_element())
        if self.purpose is not None:
            self.purpose.set_tag("purpose")
            dataset.append(self.purpose.to_element())
        if self.introduction is not None:
            self.introduction.set_tag("introduction")
            dataset.append(self.introduction.to_element())
        if self.getting_started is not None:
            self.getting_started.set_tag("gettingStarted")
            dataset.append(self.getting_started.to_element())
        if self.acknowledgements is not None:
            self.acknowledgements.set_tag("acknowledgements")
            dataset.append(self.acknowledgements.to_element())
        if self.maintenance is not None:
            dataset.append(self.maintenance.to_element())
        if self.publisher is not None:
            self.publisher.set_tag("publisher")
            dataset.append(self.publisher.to_element())
        if self.pub_place is not None:
            pub_place_elem = self.object_to_element("pubPlace")
            pub_place_elem.text = self.pub_place
            dataset.append(pub_place_elem)
        if self.methods is not None:
            dataset.append(self.methods.to_element())
        if self.project is not None:
            self.project.set_tag("project")
            dataset.append(self.project.to_element())
        return dataset
