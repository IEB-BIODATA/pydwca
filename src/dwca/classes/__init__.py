from typing import Dict, Type
from warnings import warn

from lxml import etree as et

from dwca.classes.data_file import DataFile
from dwca.classes.occurrence import Occurrence
from dwca.classes.organism import Organism
from dwca.classes.material_entity import MaterialEntity
from dwca.classes.material_sample import MaterialSample
from dwca.classes.event import Event
from dwca.classes.location import Location
from dwca.classes.geological_context import GeologicalContext
from dwca.classes.identification import Identification
from dwca.classes.taxon import Taxon
from dwca.classes.resource_relationship import ResourceRelationship
from dwca.classes.measurement_or_fact import MeasurementOrFact
from dwca.classes.chronometric_age import ChronometricAge
from dwca.classes.outside_class import OutsideClass

EXPECTED_NAMESPACES = [
    "http://rs.tdwg.org/dwc/terms/",
    "http://purl.org/dc/terms/",
    "http://rs.tdwg.org/chrono/terms/",
]

CLASSES: Dict[str, Type[DataFile]] = {
    "Occurrence": Occurrence,
    "Organism": Organism,
    "MaterialEntity": MaterialEntity,
    "MaterialSample": MaterialSample,
    "Event": Event,
    "Location": Location,
    "GeologicalContext": GeologicalContext,
    "Identification": Identification,
    "Taxon": Taxon,
    "ResourceRelationship": ResourceRelationship,
    "MeasurementOrFact": MeasurementOrFact,
    "ChronometricAge": ChronometricAge,
}


def get_dwc_class(element: et.Element) -> DataFile:
    """
    Extract the row type from an XML element instance.

    Parameters
    ----------
    element : lxml.etree.Element
        XML element instance.

    Returns
    -------
    DataFile
        An object representing the class term.
    """
    row_type_url = element.get("rowType")
    for namespace in EXPECTED_NAMESPACES:
        if namespace in row_type_url:
            from dwca.classes import CLASSES
            row_type = row_type_url.replace(namespace, "")
            return CLASSES[row_type]
    warn(f"{row_type_url} not in expected namespace.")
    return OutsideClass
