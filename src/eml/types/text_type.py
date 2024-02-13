from __future__ import annotations

from typing import Dict, List, Union, Any

from lxml import etree as et

from dwca.utils import Language
from eml.types import EMLSection, _NoTagObject
from eml.types import I18nString


class EMLTextType(_NoTagObject):
    """
    A simple text description.

    Parameters
    ----------
    sections : List[EMLSection], optional
        A section of related text.
    paragraphs : List[I18String or str], optional
        A simple paragraph of text.
    markdowns : List[str], optional
        A block of text formatted with Markdown directives.
    language : Language, optional
        Language of abstract.
    """
    def __init__(
            self, sections: List[EMLSection] = None,
            paragraphs: List[Union[I18nString, str]] = None,
            markdowns: List[str] = None,
            language: Language = Language.ENG
    ) -> None:
        super().__init__()
        self.__sections__: List[EMLSection] = list()
        if sections is not None:
            self.__sections__.extend(sections)
        self.__paragraphs__: List[I18nString] = list()
        if paragraphs is not None:
            for paragraph in paragraphs:
                self.__paragraphs__.append(I18nString(paragraph))
        self.__markdowns__: List[str] = list()
        if markdowns is not None:
            self.__markdowns__.extend(markdowns)
        self.__lang__ = Language.ENG
        if language is not None:
            self.__lang__ = language
        return

    @property
    def sections(self) -> List[EMLSection]:
        """List[EMLSection]: A section of related text."""
        return self.__sections__

    @property
    def paragraphs(self) -> List[I18nString]:
        """List[I18nString]: A simple paragraph of text."""
        return self.__paragraphs__

    @property
    def markdowns(self) -> List[str]:
        """List[str]: A block of text formatted with Markdown directives."""
        return self.__markdowns__

    @property
    def language(self) -> Language:
        """Language: Language of the text."""
        return self.__lang__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLTextType | None:
        """
        Generate an EMLTextType from an XML element.
        
        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to be parsed.
        nmap : Dict
            Namespace of the XML element.

        Returns
        -------
        EMLTextType
            Parsed object
        """
        if element is None:
            return None
        sections = list()
        for section in element.findall("section", nmap):
            sections.append(EMLSection.parse(section, nmap))
        paragraphs = list()
        for paragraph in element.findall("para", nmap):
            paragraphs.append(I18nString.parse(paragraph, nmap))
        markdowns = list()
        for markdown in element.findall("markdown", nmap):
            markdowns.append(markdown.text)
        text_type = EMLTextType(sections, paragraphs, markdowns)
        text_type.__namespace__ = nmap
        return text_type

    def to_element(self) -> et.Element:
        """
        Get an XML Element from the EMLTextType object

        Returns
        -------
        lxml.etree.Element
            XML Element with the information of the EMLTextType instance
        """
        text_type = super().to_element()
        for section in self.sections:
            text_type.append(section.to_element())
        for para in self.paragraphs:
            para.set_tag("para")
            text_type.append(para.to_element())
        for markdown in self.markdowns:
            mark_elem = self.object_to_element("markdown")
            mark_elem.text = markdown
            text_type.append(mark_elem)
        return text_type

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EMLTextType):
            return (
                self.sections == other.sections and
                self.paragraphs == other.paragraphs and
                self.markdowns == other.markdowns
            )
        else:
            return False
