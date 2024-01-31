from __future__ import annotations
from typing import Dict, Union

from lxml import etree as et

from dwca.utils import Language
from dwca.xml import XMLObject


class I18nString(XMLObject):
    """
    Internationalization of a string representing a text and its language.

    Parameters
    ----------
    value : str or I18nString
        Value of the string.
    lang : Language or str
        Language of the string or valid abbreviation. Default `ENG` (English).

    Raises
    ------
    TypeError
        Wrong language type.
    NotImplementedError
        Abbreviation not available yet or wrong language.
    """
    def __init__(self, value: Union[str, I18nString], lang: Union[Language, str] = Language.ENG) -> None:
        super().__init__()
        if isinstance(value, I18nString):
            self.__value__ = str(value)
            self.__lang__ = value.language
            self.__tag__ = value.__tag__
        else:
            self.__value__ = value
            language = Language.ENG
            if lang is None:
                pass
            elif isinstance(lang, str):
                found = False
                for candid_lang in Language:
                    if lang.lower() == candid_lang.name.lower():
                        language = candid_lang
                        found = True
                        break
                if not found:
                    raise NotImplementedError(f"{lang} not in the available languages")
            elif isinstance(lang, Language):
                language = lang
            else:
                raise TypeError("Language must be a Language type or a valid string")
            self.__lang__ = language
            self.__tag__ = None
        return

    @property
    def language(self) -> Language:
        """Language: The language of the string."""
        return self.__lang__

    def __str__(self) -> str:
        return self.__value__

    def __repr__(self) -> str:
        return f"<i18n String ({self.__value__}) [{self.language.name.lower()}]>"

    def __eq__(self, other: Union[str, I18nString]) -> bool:
        if isinstance(other, str):
            return self.__value__ == other
        elif isinstance(other, I18nString):
            return self.__value__ == other.__value__ and self.language == other.language
        else:
            return False

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> I18nString | None:
        """
        Parses a lxml element into an i18n String.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        I18nString
            Object parsed.
        """
        if element is None:
            return None
        return I18nString(element.text, lang=element.get(f"{{{cls.NAMESPACES['xml']}}}lang", "eng"))

    def to_element(self) -> et.Element:
        """
        Generate a lxml.tree.Element from the i18n string.

        Returns
        -------
        lxml.tree.Element
            Object in the XML Element format.

        Raises
        ------
        RuntimeError
            If tag is not set before calling this method.
        """
        if self.__tag__ is None:
            raise RuntimeError("First, set tag to call `to_element`")
        element = et.Element(self.__tag__)
        element.text = self.__value__
        element.set(f"{{{self.__namespace__['xml']}}}lang", self.__lang__.name.lower())
        return element

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Always return True due tag not existing until set

        Parameters
        ----------
        tag : str
            Any tag.
        nmap : Dict
            Namespace.
        """
        return

    def set_tag(self, tag: str) -> None:
        """
        Set tag for the element output.

        Parameters
        ----------
        tag : str
            Tag of the XML output element.

        Returns
        -------
        None
            Set tag.
        """
        self.__tag__ = tag
        return
