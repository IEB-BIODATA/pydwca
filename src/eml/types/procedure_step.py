from __future__ import annotations
from typing import Dict, List

import lxml.etree as et

from eml.types import _NoTagObject, EMLTextType


class ProcedureStep(_NoTagObject):
    """
    Represent a description of a specific step of the method.

    Parameters
    ----------
    description : EMLTextType
        Description of the methods employed in collecting or generating a data set or other resource or in quality control and assurance.
    citation : EMLCitation, optional
        Literature citation relating to the methods used.
    protocol : EMLProtocol, optional
        Protocol description relating to the methods used.
    instrumentation : List[str], optional
        Instruments used for measurement and recording data.
    software : List[EMLSoftware], optional
        Software used in the processing of data.
    sub_step : List[ProcedureStep], optional
        This fields allows the nesting of additional method steps within this step.
    """
    def __init__(
            self, description: EMLTextType,
            citation: EMLCitation = None,
            protocol: EMLProtocol = None,
            instrumentation: List[str] = None,
            software: List[EMLSoftware] = None,
            sub_step: List[ProcedureStep] = None
    ) -> None:
        super().__init__()
        self.__description__ = description
        if citation is not None and protocol is not None:
            raise TypeError("ProcedureStep() allow only one of citation (`eml.resource.EMLCitation`) "
                            "or a protocol (`eml.resource.EMLProtocol`).")
        self.__citation__ = citation
        self.__protocol__ = protocol
        self.__instrumentation__ = list()
        if instrumentation is not None:
            self.__instrumentation__.extend(instrumentation)
        self.__software__ = list()
        if software is not None:
            self.__software__.extend(software)
        self.__sub_step__ = list()
        if sub_step is not None:
            self.__sub_step__.extend(sub_step)
        return

    @property
    def description(self) -> EMLTextType:
        """EMLTextType: Description of the methods employed in collecting or generating a data set or other resource or in quality control and assurance."""
        return self.__description__

    @property
    def citation(self) -> EMLCitation:
        """EMLCitation: Literature citation relating to the methods used."""
        return self.__citation__

    @property
    def protocol(self) -> EMLProtocol:
        """EMLProtocol: Protocol description relating to the methods used."""
        return self.__protocol__

    @property
    def instrumentation(self) -> List[str]:
        """List[str]: Instruments used for measurement and recording data."""
        return self.__instrumentation__

    @property
    def software(self) -> List[EMLSoftware]:
        """List[EMLSoftware]: Software used in the processing of data."""
        return self.__software__

    @property
    def sub_step(self) -> List[ProcedureStep]:
        """List[ProcedureStep]: List of sub step, useful for hierarchical method descriptions."""
        return self.__sub_step__

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> ProcedureStep | None:
        """
        Parses a lxml element into a Procedure Step object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        ProcedureStep
            Object parsed.
        """
        if element is None:
            return None
        citation_elem = element.find("citation", nmap)
        if citation_elem is not None:
            from eml.resources import EMLCitation
            citation = EMLCitation.parse(citation_elem, nmap)
        else:
            citation = None
        protocol_elem = element.find("protocol", nmap)
        if protocol_elem is not None:
            from eml.resources import EMLProtocol
            protocol = EMLProtocol.parse(protocol_elem, nmap)
        else:
            protocol = None
        instrumentation = list()
        for instrument_elem in element.findall("instrumentation", nmap):
            instrumentation.append(instrument_elem.text)
        software = list()
        software_list = element.findall("software", nmap)
        if len(software_list) > 0:
            from eml.resources import EMLSoftware
            for software_elem in software_list:
                software.append(EMLSoftware.parse(software_elem, nmap))
        sub_step = list()
        for sub_step_elem in element.findall("subStep", nmap):
            sub_step.append(ProcedureStep.parse(sub_step_elem, nmap))
        return ProcedureStep(
            description=EMLTextType.parse(element.find("description", nmap), nmap),
            citation=citation,
            protocol=protocol,
            instrumentation=instrumentation,
            software=software,
            sub_step=sub_step
        )

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the Procedure Step object.

        Returns
        -------
        lxml.tree.Element
            Methods instance in the Element format.
        """
        element = super().to_element()
        self.description.set_tag("description")
        element.append(self.description.to_element())
        if self.citation is not None:
            element.append(self.citation.to_element())
        if self.protocol is not None:
            element.append(self.protocol.to_element())
        for instrument in self.instrumentation:
            instrument_elem = self.object_to_element("instrumentation")
            instrument_elem.text = instrument
            element.append(instrument_elem)
        for software in self.software:
            element.append(software.to_element())
        for sub_step in self.sub_step:
            sub_step.set_tag("subStep")
            element.append(sub_step.to_element())
        return element
