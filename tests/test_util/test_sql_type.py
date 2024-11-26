import unittest
import datetime as dt
from typing import Union

from xml_common.utils import type_to_sql, format_to_sql


class TestTypeSQL(unittest.TestCase):
    def test_int(self):
        self.assertEqual("INTEGER", type_to_sql(int), "Error converting int.")
        self.assertEqual(5, format_to_sql(5, int), "Error formatting to int.")
        self.assertEqual(5, format_to_sql("5", int), "Error formatting to int, from string.")
        self.assertIsNone(format_to_sql(None, int), "Error formatting to int, from None.")

    def test_float(self):
        self.assertEqual("REAL", type_to_sql(float), "Error converting float.")
        self.assertEqual(0.5, format_to_sql(0.5, float), "Error formatting to float.")
        self.assertEqual(1, format_to_sql(1, float), "Error formatting to float, from string.")
        self.assertIsNone(format_to_sql(None, float), "Error formatting to float, from None.")

    def test_str(self):
        self.assertEqual("VARCHAR", type_to_sql(str), "Error converting str.")
        self.assertEqual("1", format_to_sql(1, str), "Error formatting to string.")
        self.assertEqual("Hello", format_to_sql("Hello", str), "Error formatting to string.")

    def test_bool(self):
        self.assertEqual("BOOLEAN", type_to_sql(bool), "Error converting bool.")
        self.assertTrue(format_to_sql(True, bool), "Error formatting to bool.")
        self.assertFalse(format_to_sql(False, bool), "Error formatting to bool.")

    def test_datetime(self):
        self.assertEqual("DATETIME", type_to_sql(dt.datetime), "Error converting datatime.")
        a_date = dt.datetime(1997, 10, 3)
        self.assertEqual(a_date, format_to_sql(a_date, dt.datetime), "Error formatting to datetime.")
        self.assertEqual(a_date, format_to_sql("1997-10-03", dt.datetime), "Error formatting to datetime, from string.")
        with self.assertRaisesRegex(ValueError, "is not supported to datetime"):
            format_to_sql(1997, dt.datetime)

    def test_bytes(self):
        self.assertEqual("BLOB", type_to_sql(bytes), "Error converting byte.")
        self.assertEqual(b"Hello", format_to_sql(b"Hello", bytes), "Error formatting to bytes.")
        self.assertEqual(b"Hello", format_to_sql("Hello", bytes), "Error formatting to bytes, from string.")
        self.assertEqual(bytes(20), format_to_sql(20, bytes), "Error formatting to bytes, from int.")

    def test_object(self):
        self.assertEqual("VARCHAR", type_to_sql(Union[str, int]), "Error converting union.")
        class A:
            pass
        a = A()
        self.assertEqual("VARCHAR", type_to_sql(A), "Error converting object.")
        self.assertEqual(str(a), format_to_sql(a, A), "Error formatting to object.")


if __name__ == '__main__':
    unittest.main()
