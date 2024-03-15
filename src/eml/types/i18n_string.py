from __future__ import annotations

from typing import Dict, Union

from lxml import etree as et

from dwca.utils import Language
from eml.types import _NoTagObject


class I18nString(_NoTagObject):
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
            if value is None:
                self.__value__ = ""
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

    def __gt__(self, other: Union[str, I18nString]) -> bool:
        if isinstance(other, str):
            return self.__value__ > other
        elif isinstance(other, I18nString):
            return str(self) > str(other)
        else:
            raise TypeError(f"'>' not supported between instances of 'I18n String' and '{type(other)}'")

    def __ge__(self, other: Union[str, I18nString]) -> bool:
        return self.__value__ > other or self.__value__ == other

    def __lt__(self, other: Union[str, I18nString]) -> bool:
        if isinstance(other, str):
            return self.__value__ < other
        elif isinstance(other, I18nString):
            return str(self) < str(other)
        else:
            raise TypeError(f"'<' not supported between instances of 'I18n String' and '{type(other)}'")

    def __le__(self, other: Union[str, I18nString]) -> bool:
        return self.__value__ < other or self.__value__ == other

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
        text = element.text if element.text is not None else ""
        return I18nString(text, lang=element.get(f"{{{cls.NAMESPACES['xml']}}}lang", "eng"))

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
        element = super().to_element()
        element.text = self.__value__
        element.set(f"{{{self.__namespace__['xml']}}}lang", self.__lang__.name.lower())
        return element
