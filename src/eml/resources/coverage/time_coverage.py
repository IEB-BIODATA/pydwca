from __future__ import annotations

from typing import Dict, List, Union, Tuple

from lxml import etree as et
import datetime as dt

from dwca.xml import XMLObject
from eml.types import EMLObject, Scope


class TemporalCoverage(EMLObject):
    """
    Temporal coverage information.

    Parameters
    ----------
    _id : str, optional
        Unique identifier within the scope.
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined.
    references_system : str, optional
        System attribute of reference.
    single_datetime : List[date or datetime or AlternativeTimeScale], optional
        Means of encoding a single date and time.
    range_datetime: Tuple[date or datetime or AlternativeTimeScale], optional
        Means of encoding a range of dates and times.
    """
    PRINCIPAL_TAG = "temporalCoverage"

    class AlternativeTimeScale(XMLObject):
        """
        A name, code, or date describing an event or period in an alternative timescale.

        Parameters
        ----------
        name : str
            Name of a recognized alternative timescale.
        age_estimate : str
            Either an absolute date or a relative age name describing an event or period in an alternative timescale.
        age_uncertainty : str, optional
            The error estimate for the alternative timescale.
        age_explanation : str, optional
            The name and/or description of the method used to calculate the timescale age estimate.
        citation : List[EMLCitation], optional
            Citation for works providing detailed information about any element of the timescale age.
        """
        PRINCIPAL_TAG = "alternativeTimeScale"

        def __init__(
                self, name: str,
                age_estimate: str,
                age_uncertainty: str = None,
                age_explanation: str = None,
                citation: List = None
        ) -> None:
            super().__init__()
            self.__name__ = name
            self.__estimate__ = age_estimate
            self.__uncertainty__ = age_uncertainty
            self.__explanation__ = age_explanation
            self.__citation__ = list()
            if citation is not None:
                self.__citation__.extend(citation)
            return

        @property
        def name(self) -> str:
            """str: Name of a recognized alternative time scale."""
            return self.__name__

        @property
        def age_estimate(self) -> str:
            """
            str: Age name describing an event or period in an alternative timescale.
            """
            return self.__estimate__

        @property
        def age_uncertainty(self) -> str:
            """str: The error estimate for the alternative timescale."""
            return self.__uncertainty__

        @property
        def age_explanation(self) -> str:
            """str: The name and/or description of the method used to calculate the timescale age estimate."""
            return self.__explanation__

        @property
        def citation(self) -> List:
            """
            List[EMLCitation]: Citation for works providing detailed information about any element of the timescale age.
            """
            return self.__citation__

        @classmethod
        def parse(cls, element: et.Element, nmap: Dict) -> TemporalCoverage.AlternativeTimeScale | None:
            """
            Generate an Alternative TimeScale object from an XML element.

            Parameters
            ----------
            element : lxml.etree.Element
                XML element instance to parse.
            nmap : Dict
                Namespace.

            Returns
            -------
            AlternativeTimeScale
                Instance with the information of the XML
            """
            if element is None:
                return None
            name_elem = element.find("timeScaleName", nmap)
            estimate_elem = element.find("timeScaleAgeEstimate", nmap)
            uncertainty_elem = element.find("timeScaleAgeUncertainty", nmap)
            uncertainty = None
            if uncertainty_elem is not None:
                uncertainty = uncertainty_elem.text if uncertainty_elem.text is not None else ""
            explanation_elem = element.find("timeScaleAgeExplanation", nmap)
            explanation = None
            if explanation_elem is not None:
                explanation = explanation_elem.text if explanation_elem.text is not None else ""
            citations = list()
            from eml.resources import EMLCitation
            for cite in element.findall("timeScaleCitation", nmap):
                citations.append(EMLCitation.parse(cite, nmap))
            alter_time_scale = TemporalCoverage.AlternativeTimeScale(
                name=name_elem.text if name_elem is not None else "",
                age_estimate=estimate_elem.text if estimate_elem is not None else "",
                age_uncertainty=uncertainty,
                age_explanation=explanation,
                citation=citations
            )
            alter_time_scale.__namespace__ = nmap
            return alter_time_scale

        def to_element(self) -> et.Element:
            """
            Generate an XML element from the information of this instance.

            Returns
            -------
            lxml.etree.Element
                An XML element
            """
            element = super().to_element()
            name_elem = self.object_to_element("timeScaleName")
            name_elem.text = self.name
            element.append(name_elem)
            age_estimate_elem = self.object_to_element("timeScaleAgeEstimate")
            age_estimate_elem.text = self.age_estimate
            element.append(age_estimate_elem)
            if self.age_uncertainty is not None:
                age_uncertainty_elem = self.object_to_element("timeScaleAgeUncertainty")
                age_uncertainty_elem.text = self.age_uncertainty
                element.append(age_uncertainty_elem)
            if self.age_explanation is not None:
                age_explanation_elem = self.object_to_element("timeScaleAgeExplanation")
                age_explanation_elem.text = self.age_explanation
                element.append(age_explanation_elem)
            for citation in self.citation:
                citation_elem = citation.to_element()
                citation_elem.tag = "timeScaleCitation"
                element.append(citation_elem)
            return element

    def __init__(
            self, _id: str = None,
            scope: Scope = Scope.DOCUMENT,
            system: str = None,
            referencing: bool = False,
            references_system: str = None,
            single_datetime: List[Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]] = None,
            range_datetime: Tuple[
                Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale],
                Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]
            ] = None,
    ) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        if (
                not self.referencing and
                (single_datetime is None or len(single_datetime) == 0) and
                range_datetime is None
        ):
            raise ValueError("Must provide at least one single datetime or a range")
        self.__range__ = range_datetime
        self.__single__ = list()
        if single_datetime is not None:
            self.__single__.extend(single_datetime)
        return

    @property
    def single_datetime(self) -> List[Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]]:
        """
        List[date or datetime or AlternativeTimeScale]: Means of encoding a single date and time.
        """
        return self.__single__

    @property
    def range_datetime(self) -> Tuple[
        Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale],
        Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]
    ]:
        """
        Tuple[date or datetime or AlternativeTimeScale]: Means of encoding a range of dates and times.
        """
        return self.__range__

    @classmethod
    def get_referrer(cls, element: et.Element, nmap: Dict) -> TemporalCoverage:
        """
        Generate a Time Coverage referencing another Time Coverage.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse with references object.
        nmap : Dict
            Namespace.

        Returns
        -------
        TemporalCoverage
            Object parsed that reference another.
        """
        references = element.find("references", nmap)
        return TemporalCoverage(
            _id=references.text if references.text is not None else "",
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=True,
            references_system=references.get("system", None)
        )

    @classmethod
    def get_no_referrer(cls, element: et.Element, nmap: Dict) -> TemporalCoverage:
        """
        Generate a TemporalCoverage that do not reference another.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        TemporalCoverage
            Object parsed.
        """
        single_datetime = list()
        for single_elem in element.findall("singleDateTime", nmap):
            single_datetime.append(cls.xml_to_datetime(single_elem, nmap))
        range_datetime = None
        range_elem = element.find("rangeOfDates", nmap)
        if range_elem is not None:
            begin_elem = range_elem.find("beginDate", nmap)
            end_elem = range_elem.find("endDate", nmap)
            range_datetime = cls.xml_to_datetime(begin_elem, nmap), cls.xml_to_datetime(end_elem, nmap)
        return TemporalCoverage(
            _id=element.get("id", None),
            scope=cls.get_scope(element),
            system=element.get("system", None),
            referencing=False,
            single_datetime=single_datetime,
            range_datetime=range_datetime,
        )

    def to_element(self) -> et.Element:
        """
        Generate an XML element with the information of the TemporalCoverage object.

        Returns
        -------
        lxml.etree.Element
            AN XML element.
        """
        element = super().to_element()
        element = self._to_element_(element)
        for single in self.single_datetime:
            single_elem = self.datetime_to_xml(single)
            single_elem.tag = "singleDateTime"
            element.append(single_elem)
        if self.range_datetime is not None:
            range_elem = self.object_to_element("rangeOfDates")
            begin_elem = self.datetime_to_xml(self.range_datetime[0])
            begin_elem.tag = "beginDate"
            range_elem.append(begin_elem)
            end_elem = self.datetime_to_xml(self.range_datetime[1])
            end_elem.tag = "endDate"
            range_elem.append(end_elem)
            element.append(range_elem)
        return element

    @staticmethod
    def xml_to_datetime(element: et.Element, nmap: Dict) -> Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]:
        """
        Convert an XML element instance to datetime object in the correspondant format.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element to parse.
        nmap : Dict
            Namespace.

        Returns
        -------
        datetime, date or AlternativeTimeScale
            Datetime in the corresponding format.
        """
        alternative_elem = element.find("alternativeTimeScale")
        if alternative_elem is not None:
            return TemporalCoverage.AlternativeTimeScale.parse(alternative_elem, nmap)
        time_elem = element.find("time")
        calendar_elem = element.find("calendarDate")
        try:
            calendar_date = dt.datetime.strptime(calendar_elem.text, "%Y-%m-%d").date()
        except ValueError:
            calendar_date = dt.datetime.strptime(calendar_elem.text, "%Y").date()
        if time_elem is not None:
            try:
                return dt.datetime.strptime(
                    f"{calendar_date.strftime('%Y-%m-%d')} {time_elem.text}",
                    "%Y-%m-%d %H:%M:%SZ"
                )
            except ValueError:
                return dt.datetime.strptime(
                    f"{calendar_date.strftime('%Y-%m-%d')} {time_elem.text}",
                    "%Y-%m-%d %H:%M:%S%z"
                )
        else:
            return calendar_date

    @staticmethod
    def datetime_to_xml(datetime: Union[dt.date, dt.datetime, TemporalCoverage.AlternativeTimeScale]) -> et.Element:
        """
        Convert a datetime to an XML element instance.

        Parameters
        ----------
        datetime : datetime, date or AlternativeTimeScale
            XML element to parse.

        Returns
        -------
        lxml.etree.Element
            XML element instance.

        Raises
        ------
        TypeError
            Not a valid datetime.
        """
        element = et.Element("placeholderDate")
        if isinstance(datetime, dt.datetime):
            calendar_elem = et.Element("calendarDate")
            calendar_elem.text = datetime.date().strftime("%Y-%m-%d")
            element.append(calendar_elem)
            time_elem = et.Element("time")
            time_elem.text = datetime.time().strftime("%H:%M:%S%z")
            element.append(time_elem)
        elif isinstance(datetime, dt.date):
            calendar_elem = et.Element("calendarDate")
            calendar_elem.text = datetime.strftime("%Y-%m-%d")
            element.append(calendar_elem)
        elif isinstance(datetime, TemporalCoverage.AlternativeTimeScale):
            element.append(datetime.to_element())
        else:
            raise TypeError("Not a valid datetime")
        return element
