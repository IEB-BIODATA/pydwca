import logging
import unittest
import lxml.etree as et


class TestXML(unittest.TestCase):
    def assertEqualTree(self, expected: et.ElementTree, actual: et.ElementTree, msg: str) -> None:
        try:
            self.assertEqual(expected.tag, actual.tag, "Not same tag")
            logging.debug(expected.attrib)
            self.assertEqual(expected.attrib, actual.attrib, "Not same attributes")
            expected_tags = set([child.tag for child in expected])
            actual_tags = set([child.tag for child in actual])
            self.assertCountEqual(expected_tags, actual_tags, "Different tags")
            for tag in expected_tags:
                for expected_child, actual_child in zip(expected.findall(tag), actual.findall(tag)):
                    self.assertEqualTree(expected_child, actual_child, msg=msg)
        except AssertionError:
            raise AssertionError(f"{et.tostring(expected).decode()} != {et.tostring(actual).decode()} : {msg}")
