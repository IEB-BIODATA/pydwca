from __future__ import annotations

from enum import Enum


ABBREVIATIONS = {
    "es": "esp",
    "esp": "esp",
    "spanish": "esp",
    "en": "eng",
    "eng": "eng",
    "english": "eng",
}


class Language(Enum):
    """
    The language of the resource.

    Attributes
    ----------
    ESP : str
        Spanish language
    ENG : str
        English language
    """
    ESP = "Spanish"
    ENG = "English"

    @staticmethod
    def get_language(abbreviation: str) -> Language:
        for lang in Language:
            if lang.name.lower() == ABBREVIATIONS[abbreviation.lower()]:
                return lang
        raise NotImplementedError(f"{abbreviation} language not implemented yet")
