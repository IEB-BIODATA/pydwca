from __future__ import annotations
from typing import Dict, Union, List, Tuple

from lxml import etree as et

from eml.types import EMLObject, _NoTagObject, Scope, ResponsibleParty, Role, EMLTextType


class ResearchProject(EMLObject, _NoTagObject):
    """
    Descriptor of a research context for a dataset or another project.

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
    title : str | List[str]
        Title(s) of the project.
    personnel : List[Tuple[ResponsibleParty, Role]]
        Contact and role information for people involved in the research project.
    abstract : EMLTextType, optional
        Project Abstract.
    funding : EMLTextType, optional
        Funding information.
    related_projects : List[ResearchProject], optional
        This field is a recursive link to another project.

    Raises
    ------
    TypeError
        If it is not a reference, raises TypeError if title or personnel is not given.
    """
    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            title: Union[str, List[str]] = None,
            personnel: List[Tuple[ResponsibleParty, Role]] = None,
            abstract: EMLTextType = None,
            funding: EMLTextType = None,
            related_projects: List[ResearchProject] = None
    ) -> None:
        EMLObject.__init__(self, _id, scope, system, referencing, references_system)
        _NoTagObject.__init__(self)
        self.__titles__ = list()
        self.__personnel__ = list()
        self.__abstract__ = abstract
        self.__funding__ = funding
        self.__related_projects__ = list()
        if not self.referencing:
            if title is None or len(title) == 0:
                raise TypeError("ResearchProject requires at least one title.")
            if personnel is None or len(personnel) == 0:
                raise TypeError("ResearchProject requires at least one personnel.")
            if isinstance(title, str):
                self.__titles__.append(title)
            else:
                self.__titles__.extend(title)
            self.__personnel__ = personnel
            if related_projects is not None:
                self.__related_projects__.extend(related_projects)
        return

    @property
    def title(self) -> str | None:
        """str: A descriptive title for the research project."""
        if len(self.__titles__) == 0:
            return None
        return self.__titles__[0]

    @property
    def titles(self) -> List[str]:
        """List[str]: A list of all titles of this project."""
        return self.__titles__

    @property
    def personnel(self) -> List[Tuple[ResponsibleParty, Role]]:
        """List[Tuple[ResponsibleParty, Role]]: Contact and role information for people involved in the research project."""
        return self.__personnel__

    @property
    def abstract(self) -> EMLTextType:
        """EMLTextType: Project Abstract."""
        return self.__abstract__

    @property
    def funding(self) -> EMLTextType:
        """EMLTextType: Funding information."""
        return self.__funding__

    @property
    def award(self) -> List:
        """List: Awards information."""
        # TODO: Implement Awards (https://eml.ecoinformatics.org/schema/eml-project_xsd.html#ResearchProjectType_award)
        return list()

    @property
    def study_area_description(self) -> None:
        """None: Description of the study area."""
        # TODO: Implement StudyAreaDescription (https://eml.ecoinformatics.org/schema/eml-project_xsd.html#ResearchProjectType_studyAreaDescription)
        return

    @property
    def design_description(self) -> None:
        """None: Description of research design."""
        # TODO: Implement DesignDescription (https://eml.ecoinformatics.org/schema/eml-project_xsd.html#ResearchProjectType_designDescription)
        return

    @property
    def related_project(self) -> List[ResearchProject]:
        """List[ResearchProject]: List of related projects."""
        return self.__related_projects__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> ResearchProject:
        """
        Generate a Research Project referencing another Research Project.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        ResearchProject
            Object parsed that reference another research project on document.
        """
        references = element.find("references")
        return ResearchProject(
            _id=references.text,
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> ResearchProject:
        """
        Generate a Research Project that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        ResearchProject
            Object parsed.
        """
        abstract_elem = element.find("abstract", namespaces=nmap)
        related_elem = element.findall("relatedProject", namespaces=nmap)
        return ResearchProject(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            title=[title.text for title in element.findall("title")],
            personnel=[
                (ResponsibleParty.parse(person, nmap), ResponsibleParty.get_role(person, nmap))
                for person in element.findall("personnel")
            ],
            abstract=None if abstract_elem is None else EMLTextType.parse(abstract_elem, nmap),
            related_projects=[ResearchProject.parse(related, nmap) for related in related_elem]
        )

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the Research Project object.

        Returns
        -------
        lxml.tree.Element
            Object in the XML Element format.

        Raises
        ------
        RuntimeError
            If tag is not set before calling this method.
        """
        res_proj = _NoTagObject.to_element(self)
        res_proj = self._to_element_(res_proj)
        references = self.generate_references_element()
        if references is None:
            for title in self.titles:
                title_elem = self.object_to_element("title")
                title_elem.text = title
                res_proj.append(title_elem)
            for person, role in self.personnel:
                person.set_tag("personnel")
                person_elem = person.to_element()
                role_elem = self.object_to_element("role")
                role_elem.text = role.to_camel_case()
                person_elem.append(role_elem)
                res_proj.append(person_elem)
            for related in self.related_project:
                related.set_tag("relatedProject")
                res_proj.append(related.to_element())
        return res_proj
