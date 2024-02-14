from __future__ import annotations

from dwca.base import DarwinCore


class SimpleDarwinCore(DarwinCore):
    """
    Class representing a Simple Darwin Core standard.
    """
    @classmethod
    def from_file(cls, path_to_archive: str) -> SimpleDarwinCore:
        pass

    def to_file(self, path_to_archive: str, encoding: str = "utf-8") -> None:
        pass
