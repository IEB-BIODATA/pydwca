import unittest

from datetime_interval import Interval
from lxml import etree as et
import datetime as dt

from dwca.terms import EventDate
from test_xml.test_xml import TestXML


class TestUnionDateTimeField(TestXML):
    def test_parse(self):
        event_date_xml = """<field index="3" term="http://rs.tdwg.org/dwc/terms/eventDate"/>"""
        event_date = EventDate.from_string(event_date_xml)
        self.assertEqual(
            "http://rs.tdwg.org/dwc/terms/eventDate",
            event_date.uri,
            "Wrong URI"
        )
        self.assertEqual(3, event_date.index, "Wrong index")
        self.assertEqualTree(
            et.fromstring(event_date_xml),
            event_date.to_element(),
            "Wrong generated element."
        )
        pass

    def test_format(self):
        event_date = EventDate(3)
        value = "1963-03-08T14:07-0600"
        self.assertEqual(
            dt.datetime(year=1963, month=3, day=8, hour=14, minute=7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            event_date.format(value),
            "Error formatting union (datetime)"
        )
        value = "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"
        actual = event_date.format(value)
        expected = Interval(
            start=dt.datetime(year=2007, month=3, day=1, hour=13, tzinfo=dt.timezone.utc),
            end=dt.datetime(year=2008, month=5, day=11, hour=15, minute=30, tzinfo=dt.timezone.utc)
        )
        # self.assertEqual(expected, actual, "Error formatting union (interval)")
        self.assertEqual(
            expected.start, actual.start,
            "Error formatting union (interval, start)"
        )
        self.assertEqual(
            expected.end, actual.end,
            "Error formatting union (interval, end)"
        )
        value = "Invalid value"
        self.assertRaisesRegex(TypeError, "does not match any", event_date.format, value)


if __name__ == '__main__':
    unittest.main()
