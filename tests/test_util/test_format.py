import unittest
from typing import List, Tuple, Any, Union

import datetime as dt

from datetime_interval import Interval

from xml_common.utils import format_to_type


class MetaNewType(type):
    def __str__(cls) -> str:
        return 'NewType'


class MetaAnotherType(type):
    def __str__(cls) -> str:
        return '<AnotherType>'


class NewType(metaclass=MetaNewType):
    pass


class AnotherType(metaclass=MetaAnotherType):
    pass


class FormatTest(unittest.TestCase):

    def test_format_int(self):
        a = "23"
        self.assertEqual(23, format_to_type(a, int), "Incorrect format to integer.")

    def test_format_float(self):
        a = "23"
        self.assertGreaterEqual(1e-10, abs(23 - format_to_type(a, float)), "Incorrect format to float.")
        b = "3.14"
        self.assertGreaterEqual(1e-10, abs(3.14 - format_to_type(b, float)), "Incorrect format to float.")

    def test_format_str(self):
        a = "23"
        self.assertEqual("23", format_to_type(a, str), "Incorrect format to string.")
        b = "abc"
        self.assertEqual("abc", format_to_type(b, str), "Incorrect format to string.")

    def test_format_list(self):
        a = "1 | 2 | 3"
        self.assertEqual(["1", "2", "3"], format_to_type(a, List[str]), "Incorrect format to list of string.")

    def test_format_tuple(self):
        a = "1/2/3"
        self.assertEqual(
            ("1", "2", "3"),
            format_to_type(a, Tuple[str, str, str]),
            "Incorrect format to tuple of string."
        )
        self.assertEqual(
            (1, 2, 3),
            format_to_type(a, Tuple[int, int, int]),
            "Incorrect format to tuple of integer."
        )
        self.assertEqual(
            (1, "2", 3),
            format_to_type(a, Tuple[int, str, int]),
            "Incorrect format to tuple."
        )

    def test_address_error(self):
        a = "abc"
        self.assertIsNone(format_to_type(a, int, True), "Format incorrect not addressed")

    def test_not_address_error(self):
        a = "abc"
        self.assertRaises(
            ValueError,
            format_to_type,
            a, int, False
        )

    def test_not_type_error(self):
        a = "abc"
        self.assertRaisesRegex(TypeError, "<NewType>",
                               format_to_type, a, NewType)
        self.assertRaisesRegex(TypeError, "<AnotherType>",
                               format_to_type, a, AnotherType)

    def test_warning_any(self):
        a = "abc"
        with self.assertWarnsRegex(UserWarning, "<Any>"):
            self.assertEqual(
                a, format_to_type(a, Any), "Error on format Any"
            )

    def test_format_union(self):
        a = "abc"
        self.assertEqual("abc", format_to_type(a, Union[int, str]), "Error on format to string (in union)")

    def test_format_union_error(self):
        a = "abc"
        self.assertRaisesRegex(
            TypeError,
            "any of <class 'int'>, <class 'float'>",
            format_to_type,
            a, Union[int, float]
        )

    def test_format_datetime(self):
        a = "2024-04-05T01:01:07-0600"
        self.assertEqual(
            dt.datetime(2024, 4, 5, 1, 1, 7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            format_to_type(a, dt.datetime),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M:%S%z`"
        )
        b = "2024-04-04T01:07-0500"
        self.assertEqual(
            dt.datetime(2024, 4, 4, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5))),
            format_to_type(b, dt.datetime),
            "Incorrect format of datetime `%Y-%m-%dT%H:%M%z`"
        )
        c = "2024"
        self.assertEqual(
            dt.datetime(2024, 1, 1, 0, 0, 0),
            format_to_type(c, dt.datetime),
            "Incorrect format of datetime `%Y`"
        )
        d = ""
        self.assertIsNone(
            format_to_type(d, dt.datetime),
            "Incorrect format of empty datetime"
        )

    def test_format_datetime_error(self):
        a = "2024/04/05<->01:01:07"
        self.assertRaisesRegex(
            ValueError,
            "does not match",
            format_to_type,
            a, dt.datetime
        )

    def test_format_interval(self):
        a = "2024-04-04T01:01:07-0600/2024-04-05T01:07-0500"
        self.assertEqual(
            dt.datetime(2024, 4, 4, 1, 1, 7, tzinfo=dt.timezone(dt.timedelta(hours=-6))),
            format_to_type(a, Interval).start,
            "Incorrect format of datetime `%Y-%m-%dT%H:%M:%S%z`"
        )
        self.assertEqual(
            dt.datetime(2024, 4, 5, 1, 7, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5))),
            format_to_type(a, Interval).end,
            "Incorrect format of datetime `%Y-%m-%dT%H:%M%z`"
        )
        b = "2023/2024-04"
        self.assertEqual(
            dt.datetime(2023, 1, 1),
            format_to_type(b, Interval).start,
            "Incorrect format of datetime `%Y`"
        )
        self.assertEqual(
            dt.datetime(2024, 4, 1),
            format_to_type(b, Interval).end,
            "Incorrect format of datetime `%Y-%m`"
        )


if __name__ == '__main__':
    unittest.main()
