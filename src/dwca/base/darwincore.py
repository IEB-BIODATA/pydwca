from __future__ import annotations

from abc import ABC, abstractmethod


class DarwinCore(ABC):
    """
    Base class of this package.
    """
    def __init__(self) -> None:
        return

    @classmethod
    @abstractmethod
    def from_file(cls, path_to_archive: str) -> DarwinCore:
        """
        Generate a Darwin Core Standard from a file.

        Parameters
        ----------
        path_to_archive : str
            Path of the archive file.

        Returns
        -------
        DarwinCore
            Instance of the Darwin Core Standard.
        """
        pass

    @abstractmethod
    def to_file(self, path_to_archive: str, encoding: str = "utf-8") -> None:
        """
        Generate a Darwin Core file using the information of this instance.

        Parameters
        ----------
        path_to_archive : str
            Path of the archive to generate.
        encoding : str, optional
            Encoding of the corresponding files. Default `"utf-8"`.

        Returns
        -------
        None
            Writes file.
        """
        pass
