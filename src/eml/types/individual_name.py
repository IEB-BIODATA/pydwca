from __future__ import annotations
from typing import Dict, Union, List

from lxml import etree as et

from dwca.utils import Language
from dwca.xml import XMLObject
from eml.types import I18nString


class IndividualName(XMLObject):
    """
    Class representing the full name of the person being described.

    Parameters
    ----------
    last_name : str or I18nString
        The last name of the individual.
    first_name : str, I18nString or List[I18nString], optional
        The given name of the individual.
    salutation : str, I18nString or List[I18nString], optional
        The salutation used to address an individual.
    language : Language, optional
        In case of given, the language of all the parameters given
    """
    PRINCIPAL_TAG = "individualName"

    def __init__(
            self, last_name: Union[str, I18nString],
            first_name: Union[str, I18nString, List[I18nString]] = None,
            salutation: Union[str, I18nString, List[I18nString]] = None,
            language: Language = None,
    ) -> None:
        super().__init__()
        if language is not None:
            self.__last_name__ = I18nString(last_name, lang=language)
        else:
            self.__last_name__ = I18nString(last_name)
        self.__languages__ = {self.__last_name__.language}
        self.__first_name__: List[I18nString] = list()
        if isinstance(first_name, list):
            self.__first_name__.extend(first_name)
        elif first_name is not None:
            if language is not None:
                self.__first_name__.append(I18nString(first_name, lang=language))
            else:
                self.__first_name__.append(I18nString(first_name))
        for fs in self.__first_name__:
            self.__languages__.add(fs.language)
        self.__salutation__: List[I18nString] = list()
        if isinstance(salutation, list):
            self.__salutation__.extend(salutation)
        elif salutation is not None:
            if language is not None:
                self.__salutation__.append(I18nString(salutation, lang=language))
            else:
                self.__salutation__.append(I18nString(salutation))
        for s in self.__salutation__:
            self.__languages__.add(s.language)
        return

    @property
    def last_name(self) -> I18nString:
        """
        I18nString: The last name of the individual.
        """
        return self.__last_name__

    @property
    def first_name(self) -> List[I18nString]:
        """
        List[I18nString]: The given name of the individual.
        """
        return self.__first_name__

    @property
    def salutation(self) -> List[I18nString]:
        """
        List[I18nString]: The salutation used to address an individual.
        """
        return self.__salutation__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> IndividualName | None:
        """
        Parses a lxml element into an IndividualName object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        IndividualName
            Object parsed.
        """
        if element is None:
            return None
        given_names = list()
        for given_name in element.findall('givenName', nmap):
            given_names.append(I18nString.parse(given_name, nmap))
        salutations = list()
        for salutation in element.findall('salutation', nmap):
            salutations.append(I18nString.parse(salutation, nmap))
        last_name = I18nString.parse(element.find('surName', nmap), nmap)
        individual_name = IndividualName(last_name, first_name=given_names, salutation=salutations)
        individual_name.__namespace__ = nmap
        return individual_name

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the object.

        Returns
        -------
        lxml.tree.Element
            Object in the Element format.
        """
        individual_name = super().to_element()
        for salutation in self.salutation:
            salutation.set_tag("salutation")
            individual_name.append(salutation.to_element())
        for first_name in self.first_name:
            first_name.set_tag("givenName")
            individual_name.append(first_name.to_element())
        last_name = self.last_name
        last_name.set_tag("surName")
        individual_name.append(last_name.to_element())
        return individual_name

    def lang(self, language: Language) -> str:
        """
        Returns the individual name text representation in the given language.

        Parameters
        ----------
        language : Language
            The language to get the text representation.

        Returns
        -------
        str
            Text representation of object in the selected language
        """
        if language not in self.__languages__:
            raise AssertionError(f"{language.name.lower()} not present in {repr(self)}")
        first_name = ""
        for fs in self.first_name:
            if language == fs.language:
                first_name = f", {str(fs)[0]}."
                break
        salutation = ""
        for s in self.salutation:
            if language == s.language:
                salutation = f" {s}."
                break
        return f"{self.last_name}{first_name}{salutation}"

    def __str__(self) -> str:
        if len(self.__languages__) > 1:
            raise ValueError("Cannot convert to string when more than one language is present")
        first_name = ""
        salutation = ""
        if len(self.first_name) > 0:
            first_name = ", " + str(self.first_name[0])[0] + "."
        if len(self.salutation) > 0:
            salutation = " " + str(self.salutation[0]) + "."
        return f"{self.last_name}{first_name}{salutation}"

    def __repr__(self) -> str:
        last_name = f"Last Name: {self.last_name} [{self.last_name.language.name.lower()}]"
        first_name = ""
        if len(self.first_name) > 0:
            first_name = f""", First Name: {"/".join(
                f"{fn} [{fn.language.name.lower()}]" for fn in self.first_name
            )}"""
        salutation = ""
        if len(self.salutation) > 0:
            salutation = f""", Salutation: {"/".join(
                f"{s} [{s.language.name.lower()}]" for s in self.salutation
            )}"""
        return f"<Individual Name {{{last_name}{first_name}{salutation}}}>"
