from __future__ import annotations
from typing import Dict, List, Union

from lxml import etree as et

from eml.types import ProcedureStep
from xml_common import XMLObject


class Methods(XMLObject):
    """
    Class representing the methods field documents scientific methods used in the collection of this dataset.

    Parameters
    ----------
    method_steps : List[ProcedureStep]
        A list of description of a specific step of the method. At least one must be given.
    data_sources : List[List[EMLDataset] | None], optional
        The sources of data used by each method step.

    Raises
    ------
    RuntimeError
        At least one step must be given.
    """
    class MethodStep(ProcedureStep):
        """
        Represent the description of a specific step of the method.

        Parameters
        ----------
        procedure_step : ProcedureStep
            A description of a specific step.
        data_source : List[EMLDataset], optional
            Sources of data used by this MethodStep.
        """
        PRINCIPAL_TAG = "methodStep"
        def __init__(
                self,
                procedure_step: ProcedureStep,
                data_source: List[EMLDataset] = None
        ) -> None:
            super().__init__(
                description=procedure_step.description,
                citation=procedure_step.citation,
                protocol=procedure_step.protocol,
                instrumentation=procedure_step.instrumentation,
                software=procedure_step.software,
                sub_step=procedure_step.sub_step
            )
            self.__data_source__ = list()
            if data_source is not None:
                self.__data_source__.extend(data_source)
            return

        @property
        def data_source(self) -> List[EMLDataset]:
            """List[EMLDataset]: Sources of data used by this MethodStep."""
            return self.__data_source__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> Methods.MethodStep | None:
            """
            Parses a lxml element into a Method Step object.

            Parameters
            ----------
            element : lxml.tree.Element
                Object in the Element format to be parsed into a Python object.
            nmap : Dict
                Dictionary of namespace.

            Returns
            -------
            Methods.MethodStep
                Object parsed.
            """
            procedure_step = super().parse(element, nmap)
            data_source = list()
            data_elem = element.findall("dataSource", nmap)
            if len(data_elem) > 0:
                from eml.resources import EMLDataset
                for ds in data_elem:
                    data_source.append(EMLDataset.parse(ds, nmap))
            return Methods.MethodStep(
                procedure_step=procedure_step,
                data_source=data_source
            )

        def to_element(self) -> et.Element:
            """
            Generates a lxml.tree.Element from the Method Step object.

            Returns
            -------
            lxml.tree.Element
                Methods instance in the Element format.
            """
            self.set_tag(self.PRINCIPAL_TAG)
            element = super().to_element()
            for ds in self.data_source:
                ds.PRINCIPAL_TAG = "dataSource"
                element.append(ds.to_element())
            return element

    PRINCIPAL_TAG = "methods"

    def __init__(
            self, method_steps: List[ProcedureStep],
            data_sources: List[Union[List[EMLDataset], None]] = None
    ) -> None:
        super().__init__()
        self.__m_steps__ = list()
        for i, method_step in enumerate(method_steps):
            ms_kwargs = {"procedure_step": method_step}
            if data_sources is not None:
                try:
                    ms_kwargs["data_source"] = data_sources[i]
                except IndexError:
                    pass
            self.__m_steps__.append(Methods.MethodStep(**ms_kwargs))
        if len(self.__m_steps__) == 0:
            raise TypeError("At least one step must be given.")
        return

    @property
    def method_steps(self) -> List[Methods.MethodStep]:
        """List[MethodStep]: A list of description of a specific step of the method."""
        return self.__m_steps__

    @property
    def sampling(self) -> None:
        """None: Description of sampling procedures including the geographic, temporal and taxonomic coverage of the study."""
        # TODO: implement Sampling (https://eml.ecoinformatics.org/schema/eml-methods_xsd.html#MethodsType_sampling)
        return

    @property
    def quality_control(self) -> List[ProcedureStep]:
        """ProcedureStep: Information on possible errors or on the quality of a data set."""
        # TODO: implement Quality Control (https://eml.ecoinformatics.org/schema/eml-methods_xsd.html#MethodsType_qualityControl)
        return list()

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> Methods | None:
        """
        Parses a lxml element into a Methods object.

        Parameters
        ----------
        element : lxml.tree.Element
            Object in the Element format to be parsed into a Python object.
        nmap : Dict
            Dictionary of namespace.

        Returns
        -------
        Methods
            Object parsed.
        """
        if element is None:
            return None
        method_steps = list()
        data_sources = list()
        for ms in element.findall("methodStep", nmap):
            method_steps.append(Methods.MethodStep.parse(ms, nmap))
            ds_elements = ms.findall("dataSource", nmap)
            ds = list()
            if len(ds_elements) > 0:
                from eml.resources import EMLDataset
                for ds_elem in ds_elements:
                    ds.append(EMLDataset.parse(ds_elem, nmap))
            data_sources.append(ds)
        return Methods(
            method_steps=method_steps,
            data_sources=data_sources
        )

    def to_element(self) -> et.Element:
        """
        Generates a lxml.tree.Element from the Methods object.

        Returns
        -------
        lxml.tree.Element
            Methods instance in the Element format.
        """
        element = super().to_element()
        for method_step in self.method_steps:
            element.append(method_step.to_element())
        return element
