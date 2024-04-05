import datetime as dt
import unittest
from typing import List, Tuple, Union

from datetime_interval import Interval

from xml_common.utils import unformat_type


class NewType:
    pass


class FormatTest(unittest.TestCase):

    def test_unformat_int(self):
        a = 23
        self.assertEqual("23", unformat_type(a, int), "Incorrect encode from integer.")

    def test_unformat_float(self):
        a = 3.14
        self.assertEqual(str(3.14), unformat_type(a, float), "Incorrect encode from float.")

    def test_unformat_str(self):
        a = "23"
        self.assertEqual("23", unformat_type(a, str), "Incorrect encode from string.")
        b = "abc"
        self.assertEqual("abc", unformat_type(b, str), "Incorrect encode from string.")

    def test_unformat_list(self):
        a = ["1", "2", "3"]
        self.assertEqual("1 | 2 | 3", unformat_type(a, List[str]), "Incorrect encode from list of string.")

    def test_unformat_tuple(self):
        a = ("1", "2", "3")
        self.assertEqual(
            "1/2/3",
            unformat_type(a, Tuple[str, str, str]),
            "Incorrect encode from tuple of string."
        )
        b = (1, 2, 3)
        self.assertEqual(
            "1/2/3",
            unformat_type(b, Tuple[int, int, int]),
            "Incorrect encode from tuple of integer."
        )
        c = (1, "2", 3)
        self.assertEqual(
            "1/2/3",
            unformat_type(c, Tuple[int, str, int]),
            "Incorrect encode from tuple."
        )

    def test_unformat_datetime(self):
        a = dt.datetime(2024, 4, 5, 1, 1, 7, tzinfo=dt.timezone(dt.timedelta(hours=-6)))
        self.assertEqual(
            "2024-04-05T01:01:07-0600",
            unformat_type(a, dt.datetime),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M:%S%z`"
        )
        b = dt.datetime(2024, 4, 4, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
        self.assertEqual(
            "2024-04-04T01:07-0500",
            unformat_type(b, dt.datetime),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M%z`"
        )
        c = dt.datetime(2024, 1, 1, 0, 0, 0)
        self.assertEqual(
            "2024",
            unformat_type(c, dt.datetime),
            "Incorrect format of datetime `%Y`"
        )
        d = None
        self.assertEqual(
            "", unformat_type(d, dt.datetime),
            "Incorrect format of empty datetime"
        )

    def test_unformat_interval(self):
        a = Interval(
            start=dt.datetime(2024, 4, 4, 1, 1, 7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            end=dt.datetime(2024, 4, 5, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
        )
        self.assertEqual(
            "2024-04-04T01:01:07-0600/2024-04-05T01:07-0500",
            unformat_type(a, Interval),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M:%S%z/%Y-%m-%dT%H:%M%z`"
        )
        b = Interval(
            start=dt.datetime(2023, 1, 1),
            end=dt.datetime(2024, 4, 1)
        )
        self.assertEqual(
            "2023/2024-04",
            unformat_type(b, Interval),
            "Incorrect format of datetime `%Y/%Y-%m`"
        )

    def test_unformat_date_or_interval(self):
        a = Interval(
            start=dt.datetime(2024, 4, 4, 1, 1, 7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            end=dt.datetime(2024, 4, 5, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
        )
        self.assertEqual(
            "2024-04-04T01:01:07-0600/2024-04-05T01:07-0500",
            unformat_type(a, Union[Interval, dt.datetime]),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M:%S%z/%Y-%m-%dT%H:%M%z`"
        )
        b = dt.datetime(2024, 4, 4, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
        self.assertEqual(
            "2024-04-04T01:07-0500",
            unformat_type(b, Union[Interval, dt.datetime]),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M%z`"
        )

    def test_incorrect_type(self):
        a = "235"
        self.assertRaisesRegex(
            AssertionError, "Value must be",
            unformat_type, a, NewType
        )
        self.assertRaisesRegex(
            AssertionError, "Value must be a list",
            unformat_type, a, List[str]
        )


if __name__ == '__main__':
    unittest.main()
