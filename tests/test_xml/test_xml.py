import re
import unittest
from copy import deepcopy

from lxml import etree as et


class TestXML(unittest.TestCase):
    DEFAULT_TAGS = {}

    def assertEqualTree(self, expected: et.ElementTree, actual: et.ElementTree, msg: str) -> None:
        try:
            self.assertEqual(expected.tag, actual.tag, "Not same tag")
            expected_text = expected.text.strip() if expected.text is not None else ""
            actual_text = actual.text.strip() if actual.text is not None else ""
            self.assertEqual(expected_text, actual_text, "Not same text")
            self.assertDictEqual(expected.nsmap, actual.nsmap, "Not same namespaces")
            # Add default values:
            exp_attributes = deepcopy(expected.attrib)
            actual_attributes = deepcopy(actual.attrib)
            for key, value in self.DEFAULT_TAGS.items():
                if key not in exp_attributes:
                    exp_attributes[key] = value
                if key not in actual_attributes:
                    actual_attributes[key] = value
            self.assertEqual(exp_attributes, actual_attributes, "Not same attributes")
            expected_tags = set([child.tag for child in expected])
            actual_tags = set([child.tag for child in actual])
            self.assertCountEqual(expected_tags, actual_tags, "Different tags")
            for tag in expected_tags:
                for expected_child, actual_child in zip(expected.findall(tag), actual.findall(tag)):
                    self.assertEqualTree(expected_child, actual_child, msg=msg)
        except AssertionError:
            raise AssertionError(f"{et.tostring(expected).decode()} != {et.tostring(actual).decode()} : {msg}")

    def assertNotEqualTree(self, expected: et.ElementTree, actual: et.ElementTree, msg: str) -> None:
        with self.assertRaises(AssertionError, msg=msg):
            self.assertEqualTree(expected, actual, msg)

    @staticmethod
    def normalize_sql(sql: str) -> str:
        """
        Normalize an SQL statement string from comparison purpose.

        Parameters
        ----------
        sql : str
            An SQL statement string.

        Returns
        -------
        str
            The same statement with normalize space.
        """
        sql = re.sub(r'\s+', ' ', sql)
        return sql.strip()
