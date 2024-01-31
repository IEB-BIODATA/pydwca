import logging
import unittest
from copy import deepcopy

import lxml.etree as et


class TestXML(unittest.TestCase):
    def assertEqualTree(self, expected: et.ElementTree, actual: et.ElementTree, msg: str) -> None:
        try:
            self.assertEqual(expected.tag, actual.tag, "Not same tag")
            # scope = document is same as None
            exp_attributes = deepcopy(expected.attrib)
            if "scope" not in exp_attributes:
                exp_attributes["scope"] = "document"
            if "{http://www.w3.org/XML/1998/namespace}lang" not in exp_attributes:
                exp_attributes["{http://www.w3.org/XML/1998/namespace}lang"] = "eng"
            actual_attributes = deepcopy(actual.attrib)
            if "scope" not in actual_attributes:
                actual_attributes["scope"] = "document"
            if "{http://www.w3.org/XML/1998/namespace}lang" not in actual_attributes:
                actual_attributes["{http://www.w3.org/XML/1998/namespace}lang"] = "eng"
            self.assertEqual(exp_attributes, actual_attributes, "Not same attributes")
            expected_tags = set([child.tag for child in expected])
            actual_tags = set([child.tag for child in actual])
            self.assertCountEqual(expected_tags, actual_tags, "Different tags")
            for tag in expected_tags:
                for expected_child, actual_child in zip(expected.findall(tag), actual.findall(tag)):
                    self.assertEqualTree(expected_child, actual_child, msg=msg)
        except AssertionError:
            raise AssertionError(f"{et.tostring(expected).decode()} != {et.tostring(actual).decode()} : {msg}")
