import os.path
import unittest
from typing import Tuple

from lxml import etree as et

from dwca.classes import OutsideClass
from test_dwca_classes.test_outside_class_common import TestOutsideCommon
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestOutside(TestOutsideCommon):
    def setUp(self) -> None:
        self.outside_xml, self.text = self.read_xml(os.path.join(PATH, os.pardir, "example_data", "meta.xml"))
        return

    def test_parse(self):
        super().__test_parse__()

    def test_none(self):
        super().__test_none__()

    def test_merge(self):
        super().__test_merge__()

    def test_missing_field(self):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
</core>
            """
        )

    def test_field_twice(self):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            """
<core>
    <files>
      <location>missing.txt</location>
    </files>
    <id index="0"/>
    <field index="0" term=""/>
    <field index="1" term=""/>
    <field index="3" term=""/>
    <field index="2" term=""/>
    <field index="3" term=""/>
    <field index="4" term=""/>
</core>
            """
        )

    def test_parse_invalid(self):
        self.assertRaises(
            AssertionError,
            OutsideClass.from_string,
            '<extension />'
        )
        self.assertRaises(
            KeyError,
            OutsideClass.from_string,
            """
<core-id>
    <field index="0" term=""/>
</core-id>
            """
        )


if __name__ == '__main__':
    unittest.main()
