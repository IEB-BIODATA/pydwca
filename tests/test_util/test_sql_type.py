import unittest
import datetime as dt
from typing import Union

from xml_common.utils import type_to_sql


class TestTypeSQL(unittest.TestCase):
    def test_int(self):
        self.assertEqual("INTEGER", type_to_sql(int), "Error converting int.")

    def test_float(self):
        self.assertEqual("REAL", type_to_sql(float), "Error converting float.")

    def test_str(self):
        self.assertEqual("VARCHAR", type_to_sql(str), "Error converting str.")

    def test_bool(self):
        self.assertEqual("BOOLEAN", type_to_sql(bool), "Error converting bool.")

    def test_datetime(self):
        self.assertEqual("DATETIME", type_to_sql(dt.datetime), "Error converting datatime.")

    def test_bytes(self):
        self.assertEqual("BLOB", type_to_sql(bytes), "Error converting byte.")

    def test_object(self):
        self.assertEqual("VARCHAR", type_to_sql(Union[str, int]), "Error converting union.")
        class A:
            pass
        self.assertEqual("VARCHAR", type_to_sql(A), "Error converting object.")


if __name__ == '__main__':
    unittest.main()
