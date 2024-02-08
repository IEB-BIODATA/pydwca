import unittest

import datetime as dt
from lxml import etree as et

from eml.resources.coverage import TemporalCoverage
from eml.types import Scope
from test_xml.test_xml import TestXML


class TestTemporalCoverage(TestXML):
    def test_parse_none(self):
        self.assertIsNone(TemporalCoverage.parse(None, {}), "Time Coverage from nowhere")

    def test_parse_invalid(self):
        text_xml = """
<temporalCoverage id="1" scope="system" system="http://gbif.org">
</temporalCoverage>
        """
        self.assertRaises(
            ValueError,
            TemporalCoverage.from_string,
            text_xml
        )

    def test_parse(self):
        text_xml = """
<temporalCoverage id="1" scope="system" system="http://gbif.org">
    <singleDateTime>
        <calendarDate>2001-01-01</calendarDate>
        <time>14:06:09-08:00</time>
    </singleDateTime>
</temporalCoverage>
        """
        coverage = TemporalCoverage.from_string(text_xml)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(Scope.SYSTEM, coverage.scope, "Error on parsing scope")
        self.assertFalse(coverage.referencing, "Error on parsing")
        self.assertEqual("http://gbif.org", coverage.system, "Error on parsing system")
        self.assertEqual(
            dt.datetime(
                2001, 1, 1,
                14, 6, 9,
                tzinfo=dt.timezone(dt.timedelta(hours=-8, minutes=0))
            ),
            coverage.single_datetime[0],
            "Error on parsing single date time"
        )
        self.assertEqual(1, len(coverage.single_datetime), "Error on parsing single date time")
        self.assertIsNone(coverage.range_datetime, "Range datetime from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_multiple_dates(self):
        text_xml = """
<temporalCoverage id="1" scope="system" system="http://gbif.org">
    <singleDateTime>
        <calendarDate>2001-01-01</calendarDate>
        <time>14:06:09-08:00</time>
    </singleDateTime>
    <singleDateTime>
        <calendarDate>2011-12-31</calendarDate>
        <time>08:31:22Z</time>
    </singleDateTime>
</temporalCoverage>
        """
        coverage = TemporalCoverage.from_string(text_xml)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(Scope.SYSTEM, coverage.scope, "Error on parsing scope")
        self.assertFalse(coverage.referencing, "Error on parsing")
        self.assertEqual("http://gbif.org", coverage.system, "Error on parsing system")
        self.assertEqual(2, len(coverage.single_datetime), "Error on parsing single date time")
        self.assertEqual(
            dt.datetime(
                2001, 1, 1,
                14, 6, 9,
                tzinfo=dt.timezone(dt.timedelta(hours=-8))
            ),
            coverage.single_datetime[0],
            "Error on parsing single date time"
        )
        self.assertEqual(
            dt.datetime(
                2011, 12, 31,
                8, 31, 22,
            ),
            coverage.single_datetime[1],
            "Error on parsing second single date time"
        )
        self.assertIsNone(coverage.range_datetime, "Range datetime from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_range(self):
        text_xml = """
<temporalCoverage id="1" scope="system" system="http://gbif.org">
    <rangeOfDates>
        <beginDate>
            <calendarDate>2001-01-01</calendarDate>
            <time>08:31:22Z</time>
        </beginDate>
        <endDate>
            <calendarDate>2021-01-01</calendarDate>
        </endDate>
    </rangeOfDates>
</temporalCoverage>
        """
        coverage = TemporalCoverage.from_string(text_xml)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(Scope.SYSTEM, coverage.scope, "Error on parsing scope")
        self.assertFalse(coverage.referencing, "Error on parsing")
        self.assertEqual("http://gbif.org", coverage.system, "Error on parsing system")
        self.assertEqual(0, len(coverage.single_datetime), "Single datetime from nowhere")
        self.assertEqual(
            dt.datetime(
                2001, 1, 1,
                8, 31, 22,
            ),
            coverage.range_datetime[0],
            "Error on parsing begin range date time"
        )
        self.assertEqual(
            dt.date(
                2021, 1, 1
            ),
            coverage.range_datetime[1],
            "Error on parsing end range date time"
        )
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_alt_time_scale_none(self):
        self.assertIsNone(
            TemporalCoverage.AlternativeTimeScale.parse(
            None, {}),
            "Alterative from nowhere"
        )

    def test_parse_alternative_time_scale(self):
        wikipedia_explanation = ("Through analysis of seafloor magnetic "
                                 "anomalies and dating of reversal "
                                 "sequences on land, paleomagnetists "
                                 "have been developing a Geomagnetic "
                                 "Polarity Time Scale (GPTS).")
        text_xml = f"""
<alternativeTimeScale>
    <timeScaleName>Geomagnetic Polarity Time Scale</timeScaleName>
    <timeScaleAgeEstimate>C28r</timeScaleAgeEstimate>
    <timeScaleAgeUncertainty>+/- 5 Ma</timeScaleAgeUncertainty>
    <timeScaleAgeExplanation>{wikipedia_explanation}</timeScaleAgeExplanation>
    <timeScaleCitation scope="document">
        <references>3</references>
    </timeScaleCitation>
</alternativeTimeScale>
        """
        alternative_ts = TemporalCoverage.AlternativeTimeScale.from_string(text_xml)
        self.assertEqual(
            "Geomagnetic Polarity Time Scale",
            alternative_ts.name,
            "Error on parsing time scale name"
        )
        self.assertEqual(
            "C28r",
            alternative_ts.age_estimate,
            "Error on parsing time scale age estimate"
        )
        self.assertEqual(
            "+/- 5 Ma",
            alternative_ts.age_uncertainty,
            "Error on parsing time scale age uncertainty"
        )
        self.assertEqual(
            wikipedia_explanation,
            alternative_ts.age_explanation,
            "Error on parsing time scale age explanation"
        )
        self.assertEqual(1, len(alternative_ts.citation), "Error on parsing time scale citation")
        self.assertEqual("3", alternative_ts.citation[0].id, "Error on parsing time scale citation")
        self.assertTrue(alternative_ts.citation[0].referencing, "Error on parsing time scale citation")
        self.assertEqualTree(et.fromstring(text_xml), alternative_ts.to_element(), "Error on to element")

    def test_parse_alternative_time(self):
        text_xml = f"""
<temporalCoverage id="1" scope="system" system="http://gbif.org">
    <singleDateTime>
        <alternativeTimeScale>
            <timeScaleName>Geomagnetic Polarity Time Scale</timeScaleName>
            <timeScaleAgeEstimate>C28r</timeScaleAgeEstimate>
            <timeScaleCitation scope="document">
                <references>3</references>
            </timeScaleCitation>
        </alternativeTimeScale>
    </singleDateTime>
</temporalCoverage>
        """
        coverage = TemporalCoverage.from_string(text_xml)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(Scope.SYSTEM, coverage.scope, "Error on parsing scope")
        self.assertFalse(coverage.referencing, "Error on parsing")
        self.assertEqual("http://gbif.org", coverage.system, "Error on parsing system")
        self.assertEqual(1, len(coverage.single_datetime), "Error on parsing single datetime")
        self.assertEqual(
            "Geomagnetic Polarity Time Scale",
            coverage.single_datetime[0].name,
            "Error on parsing time scale name"
        )
        self.assertEqual(
            "C28r",
            coverage.single_datetime[0].age_estimate,
            "Error on parsing time scale age estimate"
        )
        self.assertIsNone(
            coverage.single_datetime[0].age_uncertainty,
            "Time scale age uncertainty from nowhere"
        )
        self.assertIsNone(
            coverage.single_datetime[0].age_explanation,
            "Time scale age explanation from nowhere"
        )
        self.assertEqual(1, len(coverage.single_datetime[0].citation), "Error on parsing time scale citation")
        self.assertEqual("3", coverage.single_datetime[0].citation[0].id, "Error on parsing time scale citation")
        self.assertTrue(coverage.single_datetime[0].citation[0].referencing, "Error on parsing time scale citation")
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_parse_reference(self):
        text_xml = """
<temporalCoverage scope="system">
    <references system="http://gbif.org">1</references>
</temporalCoverage>
        """
        coverage = TemporalCoverage.from_string(text_xml)
        self.assertEqual("1", coverage.id, "Error on parsing id")
        self.assertEqual(Scope.SYSTEM, coverage.scope, "Error on parsing scope")
        self.assertIsNone(coverage.system, "System from nowhere")
        self.assertTrue(coverage.referencing, "Error on parsing")
        self.assertEqual("http://gbif.org", coverage.references.system, "Error on parsing references")
        self.assertIsNone(coverage.range_datetime, "Range datetime from nowhere")
        self.assertEqual(0, len(coverage.single_datetime), "Single datetime from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), coverage.to_element(), "Error on to element")

    def test_not_valid_datetime_to_xml(self):
        self.assertRaises(
            TypeError,
            TemporalCoverage.datetime_to_xml,
            "2001-01-01"
        )
        self.assertRaises(
            TypeError,
            TemporalCoverage.datetime_to_xml,
            (2001, 1, 1)
        )
        self.assertRaises(
            TypeError,
            TemporalCoverage.datetime_to_xml,
            2021
        )


if __name__ == '__main__':
    unittest.main()
