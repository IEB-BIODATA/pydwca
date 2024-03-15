from __future__ import annotations

from enum import Enum
from typing import List, Dict, Any


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
        else:  # self.value == (2, 2, 0):
            return [
                "https://eml.ecoinformatics.org/eml-2.2.0",
                "xsd/eml.xsd"
            ]

    def get_namespace(self) -> Dict[Any, str]:
        """
        Get namespace of the given version.

        Returns
        -------
        Dict[Any, str]
            Namespace as a dictionary of value:uri.
        """
        if self.value == (2, 1, 1):
            nmap = {
                "eml": "eml://ecoinformatics.org/eml-2.1.1",
                "md": "eml://ecoinformatics.org/methods-2.1.1",
                "proj": "eml://ecoinformatics.org/project-2.1.1",
                "d": "eml://ecoinformatics.org/dataset-2.1.1",
                "res": "eml://ecoinformatics.org/resource-2.1.1",
                "dc": "http://purl.org/dc/terms/",
            }
        else:  # self.value == (2, 2, 0):
            nmap = {
                "eml": "https://eml.ecoinformatics.org/eml-2.2.0",
                "stmml": "http://www.xml-cml.org/schema/stmml-1.1"
            }
        nmap["xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        return nmap

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
