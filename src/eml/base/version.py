from __future__ import annotations

from enum import Enum
from typing import List


class EMLVersion(Enum):
    """
    Version of the specification of the EML used.
    """
    VERSION_2_1_1 = (2, 1, 1)
    VERSION_2_2_0 = (2, 2, 0)
    LATEST = VERSION_2_2_0

    def schema_location(self) -> List[str]:
        """
        The schema location of the given version.

        Returns
        -------
        List[str]
            A list of url where the schema of the XML version is located.

        Raises
        ------
        NotImplementedError
            Version not implemented or not existing.
        """
        if self.value == (2, 1, 1):
            return [
                "eml://ecoinformatics.org/eml-2.1.1",
                "http://rs.gbif.org/schema/eml-gbif-profile/1.0.1/eml.xsd"
            ]
        elif self.value == (2, 2, 0):
            return [
                "https://eml.ecoinformatics.org/eml-2.2.0",
                "xsd/eml.xsd"
            ]
        else:
            raise NotImplementedError(f"{self.value} version not implemented or not existing")

    @classmethod
    def get_version(cls, schema_location: str) -> EMLVersion:
        """
        Get version of EML parsing the schema location provided.

        Parameters
        ----------
        schema_location : str
            Schema location text.

        Returns
        -------
        EMLVersion
            Version of the EML.
        """
        if schema_location is None:
            return EMLVersion.LATEST
        schemas = schema_location.split(" ")
        for schema in schemas:
            if "ecoinformatics.org/eml-" in schema:
                version_str = schema.partition("ecoinformatics.org/eml-")[-1]
                return EMLVersion(tuple([int(v) for v in version_str.split(".")]))
        raise NotImplementedError(f"Version not found in: '{schema_location}'")
