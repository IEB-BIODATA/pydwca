from __future__ import annotations

from typing import Dict, Union, Any

from lxml import etree as et

from dwca.utils import Language
from dwca.xml import XMLObject
from eml.types import I18nString


class EMLSection(XMLObject):
    """
    A section of related text.

    The "section" element allows for grouping related paragraphs
    of text together, with an optional title.

    Parameters
    ----------
    title : I18nString or str, optional
        The optional title of the section.
    paragraph : I18String or str, optional
        A simple paragraph of text. If section is not given, this parameter is mandatory.
    section : Section, optional
        A section of related text. If paragraph is not given, this parameter is mandatory.
    language : Language, optional
        Language of section. Default `"ENG"`
    """
    PRINCIPAL_TAG = "section"

    def __init__(
            self, title: Union[I18nString, str] = None,
            paragraph: Union[I18nString, str] = None,
            section: EMLSection = None,
            language: Language = Language.ENG,
    ) -> None:
        super().__init__()
        if title is None:
            self.__title__ = None
        else:
            self.__title__ = I18nString(title)
        if paragraph is None and section is None:
            raise ValueError("Paragraph or section must be specified")
        if paragraph is None:
            self.__paragraph__ = None
        else:
            self.__paragraph__ = I18nString(paragraph)
        self.__section__ = section
        self.__lang__ = Language.ENG
        if language is None:
            self.__lang__ = Language.ENG
        else:
            self.__lang__ = language
        return

    @property
    def title(self) -> I18nString:
        """I18nString: The optional title of the section."""
        return self.__title__

    @property
    def paragraph(self) -> I18nString:
        """I18nString: A simple paragraph of text."""
        return self.__paragraph__

    @property
    def section(self) -> EMLSection:
        """EMLSection: A section of related text."""
        return self.__section__

    @property
    def language(self) -> Language:
        """Language: Language of section."""
        return self.__lang__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLSection | None:
        """
        Generate an EMLSection from an XML element.
        
        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to be parsed.
        nmap : Dict
            Namespace of the XML element.

        Returns
        -------
        EMLSection
            Parsed object
        """
        if element is None:
            return None
        subsection = None
        sect_elem = element.find("section", nmap)
        if sect_elem is not None:
            subsection = EMLSection.parse(sect_elem, nmap)
        language = None
        lang_elem = element.get(f"{{{cls.NAMESPACES['xml']}}}lang", None)
        if lang_elem is not None:
            language = Language.get_language(lang_elem)
        section = EMLSection(
            title=I18nString.parse(element.find("title", nmap), nmap),
            paragraph=I18nString.parse(element.find("para", nmap), nmap),
            section=subsection,
            language=language
        )
        section.__namespace__ = nmap
        return section

    def to_element(self) -> et.Element:
        """
        Get an XML Element from the EMLSection object

        Returns
        -------
        lxml.etree.Element
            XML Element with the information of the EMLSection instance
        """
        section = super().to_element()
        if self.title is not None:
            self.title.set_tag("title")
            section.append(self.title.to_element())
        if self.paragraph is not None:
            self.paragraph.set_tag("para")
            section.append(self.paragraph.to_element())
        if self.section is not None:
            section.append(self.section.to_element())
        return section

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EMLSection):
            return (
                self.title == other.title and
                self.paragraph == other.paragraph and
                self.section == other.section
            )
        else:
            return False
