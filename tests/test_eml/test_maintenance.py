import datetime as dt
import unittest

import lxml.etree as et

from eml.types import Maintenance, MaintUpFreqType
from test_xml.test_xml import TestXML


class TestMaintenance(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
    }

    def test_parse_none(self):
        self.assertIsNone(Maintenance.parse(None, {}), "Change History from None.")

    def test_parse_simple(self):
        text_xml = """
<maintenance>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </description>
</maintenance>
        """
        maintenance = Maintenance.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
            maintenance.description.paragraphs[0],
            "Error on parsing description."
        )
        self.assertIsNone(maintenance.maintenance_update_frequency, "Frequency from nowhere.")
        self.assertEqual(0, len(maintenance.change_history), "Change history from nowhere.")
        self.assertEqualTree(et.fromstring(text_xml), maintenance.to_element(), "Error on to element.")

    def test_parse_complete(self):
        text_xml = """
<maintenance>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </description>
    <maintenanceUpdateFrequency>annually</maintenanceUpdateFrequency>
    <changeHistory>
        <changeScope>Scope</changeScope>
        <oldValue>Document</oldValue>
        <changeDate>2001</changeDate>
    </changeHistory>
</maintenance>
        """
        maintenance = Maintenance.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
            maintenance.description.paragraphs[0],
            "Error on parsing description."
        )
        self.assertEqual(MaintUpFreqType.ANNUALLY, maintenance.maintenance_update_frequency, "Error on parsing frequency.")
        self.assertEqual(1, len(maintenance.change_history), "Error on parsing change history.")
        self.assertEqual("Scope", maintenance.change_history[0].change_scope, "Error on parsing change history (\"change\").")
        self.assertEqualTree(et.fromstring(text_xml), maintenance.to_element(), "Error on to element.")

    def test_parse_multiple_change_history(self):
        text_xml = """
<maintenance>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.</para>
    </description>
    <maintenanceUpdateFrequency>annually</maintenanceUpdateFrequency>
    <changeHistory>
        <changeScope>Scope</changeScope>
        <oldValue>Document</oldValue>
        <changeDate>2001</changeDate>
    </changeHistory>
    <changeHistory>
        <changeScope>Scope</changeScope>
        <oldValue>System</oldValue>
        <changeDate>2002</changeDate>
    </changeHistory>
    <changeHistory>
        <changeScope>Scope</changeScope>
        <oldValue>Document</oldValue>
        <changeDate>2003</changeDate>
    </changeHistory>
</maintenance>
        """
        maintenance = Maintenance.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam nec.",
            maintenance.description.paragraphs[0],
            "Error on parsing description."
        )
        self.assertEqual(MaintUpFreqType.ANNUALLY, maintenance.maintenance_update_frequency,
                         "Error on parsing frequency.")
        self.assertEqual(3, len(maintenance.change_history), "Error on parsing change history.")
        self.assertEqual("Scope", maintenance.change_history[0].change_scope,
                         "Error on parsing change history (\"change\").")
        self.assertEqual("Document", maintenance.change_history[0].old_value,
                         "Error on parsing change history (\"old value\", 1).")
        self.assertEqual(dt.date(year=2001, month=1, day=1), maintenance.change_history[0].change_date,
                         "Error on parsing change history (\"date\", 1).")
        self.assertEqual("System", maintenance.change_history[1].old_value,
                         "Error on parsing change history (\"old value\", 2).")
        self.assertEqual(dt.date(year=2002, month=1, day=1), maintenance.change_history[1].change_date,
                         "Error on parsing change history (\"date\", 2).")
        self.assertEqual("Document", maintenance.change_history[2].old_value,
                         "Error on parsing change history (\"old value\", 3).")
        self.assertEqual(dt.date(year=2003, month=1, day=1), maintenance.change_history[2].change_date,
                         "Error on parsing change history (\"date\", 3).")
        self.assertEqualTree(et.fromstring(text_xml), maintenance.to_element(), "Error on to element.")


if __name__ == '__main__':
    unittest.main()
