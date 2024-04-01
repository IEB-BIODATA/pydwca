import datetime
import datetime as dt
import unittest

from lxml import etree as et

from dwca.terms import ChronometricAgeDeterminedDate
from test_xml.test_xml import TestXML


class TestDateTimeField(TestXML):
    def test_parse(self):
        chron_determined_xml = """<field index="3" term="http://rs.tdwg.org/chrono/terms/chronometricAgeDeterminedDate"/>"""
        chron_determined = ChronometricAgeDeterminedDate.from_string(chron_determined_xml)
        self.assertEqual(
            "http://rs.tdwg.org/chrono/terms/chronometricAgeDeterminedDate",
            chron_determined.uri,
            "Wrong URI"
        )
        self.assertEqual(3, chron_determined.index, "Wrong index")
        self.assertEqualTree(
            et.fromstring(chron_determined_xml),
            chron_determined.to_element(),
            "Wrong generated element."
        )
        pass

    def test_format(self):
        chron_determined = ChronometricAgeDeterminedDate(3)
        value = "1963-03-08T14:07-0600"
        self.assertEqual(
            dt.datetime(year=1963, month=3, day=8, hour=14, minute=7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "2009-02-20T08:40Z"
        self.assertEqual(
            dt.datetime(year=2009, month=2, day=20, hour=8, minute=40, tzinfo=datetime.timezone.utc),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "2018-08-29T15:19"
        self.assertEqual(
            dt.datetime(year=2018, month=8, day=29, hour=15, minute=19),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "1809-02-12"
        self.assertEqual(
            dt.datetime(year=1809, month=2, day=12),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "1906-06"
        self.assertEqual(
            dt.datetime(year=1906, month=6, day=1),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "1971"
        self.assertEqual(
            dt.datetime(year=1971, month=1, day=1),
            chron_determined.format(value),
            f"Error formatting datetime ({value})"
        )
        value = "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"
        self.assertRaisesRegex(
            ValueError, "does not match any", chron_determined.format, value
        )


if __name__ == '__main__':
    unittest.main()
