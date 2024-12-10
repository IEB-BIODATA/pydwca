import unittest
import datetime as dt
import lxml.etree as et

from eml.types import ChangeHistory
from test_xml.test_xml import TestXML


class TestChangeHistory(TestXML):
    def test_parse_none(self):
        self.assertIsNone(ChangeHistory.parse(None, {}), "Change History from None.")

    def test_parse_simple(self):
        text_xml = """
<changeHistory>
    <changeScope>Scope</changeScope>
    <oldValue>Document</oldValue>
    <changeDate>2001</changeDate>
</changeHistory>
        """
        change_history = ChangeHistory.from_string(text_xml)
        self.assertEqual("Scope", change_history.change_scope, "Error on parsing change scope.")
        self.assertEqual("Document", change_history.old_value, "Error on parsing old value.")
        self.assertEqual(dt.date(year=2001, month=1, day=1), change_history.change_date, "Error on parsing change date.")
        self.assertEqualTree(et.fromstring(text_xml), change_history.to_element(), "Error on to element.")

    def test_parse_with_comment(self):
        text_xml = """
<changeHistory>
    <changeScope>Scope</changeScope>
    <oldValue>Document</oldValue>
    <changeDate>2001</changeDate>
    <comment>Testing change history</comment>
</changeHistory>
        """
        change_history = ChangeHistory.from_string(text_xml)
        self.assertEqual("Scope", change_history.change_scope, "Error on parsing change scope.")
        self.assertEqual("Document", change_history.old_value, "Error on parsing old value.")
        self.assertEqual(dt.date(year=2001, month=1, day=1), change_history.change_date,
                         "Error on parsing change date.")
        self.assertEqualTree(et.fromstring(text_xml), change_history.to_element(), "Error on to element.")


if __name__ == '__main__':
    unittest.main()
