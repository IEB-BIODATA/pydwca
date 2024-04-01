from __future__ import annotations
from enum import Enum


class CamelCaseEnum(Enum):
    """
    Enum class that allow conversion and retrieval using camel case name.
    """
    def to_camel_case(self):
        """
        Converts name to camel case (eg: camelCase).

        Returns
        -------
        str
            Name of role in camel case.
        """
        words = self.name.split("_")
        return "".join([
            word.lower() if i == 0 else word.lower().capitalize()
            for i, word in enumerate(words)
        ])

    def __str__(self) -> str:
        words = self.name.split("_")
        return " ".join([
            word.capitalize() for word in words
        ])

    @classmethod
    def get_enum(cls, name: str) -> CamelCaseEnum:
        """
        Obtain the Enum from the string with the name in camel case.

        Parameters
        ----------
        name : str
            Camel case name.

        Returns
        -------
        CamelCaseEnum
            Instance of CamelCaseEnum.

        Raises
        ------
        ValueError
            Not a valid name.
        """
        for enum in cls:
            if enum.to_camel_case() == name:
                return enum
        raise ValueError(f"{name} not a valid name for {cls.__name__}.")
