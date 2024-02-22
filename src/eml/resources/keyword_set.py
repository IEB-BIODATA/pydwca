from __future__ import annotations

from enum import Enum
from typing import Dict, List, Union

from lxml import etree as et

from dwca.xml import XMLObject
from eml.types import I18nString


class KeywordType(Enum):
    """
    The type of each keyword.

    Attributes
    ----------
    PLACE : int
        Keywords pertaining to a spatial location.
    STRATUM : int
        Keywords pertaining to a vertical stratum.
    TEMPORAL : int
        Keywords pertaining to temporal data.
    THEME : int
        Keywords pertaining to thematic subject.
    TAXONOMIC : int
        Keywords pertaining to taxon information.
    """
    NULL = 0
    PLACE = 1
    STRATUM = 2
    TEMPORAL = 4
    THEME = 5
    TAXONOMIC = 6


class EMLKeywordSet(XMLObject):
    """
    Keyword information that describes the resource.

    Parameters
    ----------
    keywords : List[I18nString, str]
        A list of keywords that describes the resource.
    thesaurus : str, optional
        The name of a thesaurus from which the keyword is derived.
    keywords_type : List[KeywordType], optional
        A list of the type of each keyword.
    """
    PRINCIPAL_TAG = "keywordSet"

    def __init__(
            self, keywords: List[Union[I18nString, str]],
            thesaurus: str = None,
            keywords_type: List[KeywordType] = None
    ) -> None:
        super().__init__()
        self.__keywords__: List[I18nString] = list()
        if len(keywords) <= 0:
            raise ValueError("KeywordSet needs at least one keyword")
        for keyword in keywords:
            self.__keywords__.append(I18nString(keyword))
        self.__thesaurus__ = thesaurus
        self.__keywords_type__: List[KeywordType] = list()
        if keywords_type is not None:
            self.__keywords_type__.extend(keywords_type)
        missing_types = len(self.__keywords__) - len(self.__keywords_type__)
        if missing_types:
            self.__keywords_type__.extend(
                [KeywordType.NULL] * missing_types
            )
        return

    @property
    def keywords(self) -> List[I18nString]:
        """List[I18nString]: A list of keywords that describes the resource."""
        return self.__keywords__

    @property
    def thesaurus(self) -> str:
        """str: The name of a thesaurus from which the keyword is derived."""
        return self.__thesaurus__

    @property
    def keywords_type(self) -> List[KeywordType]:
        """List[KeywordType]: A list of the type of each keyword."""
        return self.__keywords_type__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> EMLKeywordSet | None:
        """
        Generate an EMLKeywordSet from an XML element.
        
        Parameters
        ----------
        element : lxml.etree.Element
            XML Element to be parsed.
        nmap : Dict
            Namespace of the XML element.

        Returns
        -------
        EMLKeyword
            Parsed object
        """
        if element is None:
            return None
        keywords = list()
        keyword_types = list()
        for keyword in element.findall("keyword", nmap):
            keywords.append(I18nString.parse(keyword, nmap))
            key_type_elem = keyword.get("keywordType", None)
            if key_type_elem is None:
                keyword_types.append(KeywordType.NULL)
            else:
                found = False
                for key_type in KeywordType:
                    if key_type.name.lower() == key_type_elem.lower():
                        keyword_types.append(key_type)
                        found = True
                        break
                if not found:
                    keyword_types.append(KeywordType.NULL)
        thesaurus_elem = element.find("keywordThesaurus", nmap)
        if thesaurus_elem is not None:
            thesaurus = thesaurus_elem.text if thesaurus_elem.text is not None else ""
        else:
            thesaurus = None
        keyword_set = EMLKeywordSet(
            keywords=keywords,
            thesaurus=thesaurus,
            keywords_type=keyword_types
        )
        keyword_set.__namespace__ = nmap
        return keyword_set

    def to_element(self) -> et.Element:
        """
        Get an XML Element from the EMLKeywordSet object

        Returns
        -------
        lxml.etree.Element
            XML Element with the information of the EMLAbstract instance
        """
        keyword_set_elem = super().to_element()
        for keyword, keyword_type in zip(self.keywords, self.keywords_type):
            keyword.set_tag("keyword")
            key_elem = keyword.to_element()
            if keyword_type != KeywordType.NULL:
                key_elem.set("keywordType", keyword_type.name.lower())
            keyword_set_elem.append(key_elem)
        if self.thesaurus is not None:
            thesaurus_elem = self.object_to_element("keywordThesaurus")
            thesaurus_elem.text = self.thesaurus
            keyword_set_elem.append(thesaurus_elem)
        return keyword_set_elem
