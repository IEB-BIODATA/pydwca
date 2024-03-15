import unittest

from lxml import etree as et

from eml.types import AccessType, Scope, AccessPermission, AccessRole
from test_xml.test_xml import TestXML


class TestAccessType(TestXML):
    DEFAULT_TAGS = {
        "order": "allowFirst",
        "scope": "document",
    }

    def test_parse(self):
        text_xml = """
<access authSystem="ldap://ldap.ecoinformatics.org:389/dc=ecoinformatics,dc=org">
    <allow>
        <principal>uid=alice,o=LTER,dc=ecoinformatics,dc=org</principal>
        <permission>read</permission>
        <permission>write</permission>
    </allow>
    <deny>
        <principal>public</principal>
        <permission>write</permission>
    </deny>
</access>
        """
        access = AccessType.from_string(text_xml)
        self.assertEqual(
            "ldap://ldap.ecoinformatics.org:389/dc=ecoinformatics,dc=org",
            access.auth_system,
            "Error on parsing auth system"
        )
        self.assertFalse(access.referencing, "Error on parsing referencing")
        self.assertEqual(1, len(access.allow.principal), "Error on parsing allow (principal)")
        self.assertEqual(
            "uid=alice,o=LTER,dc=ecoinformatics,dc=org",
            access.allow.principal[0],
            "Error on parsing allow (principal)"
        )
        self.assertEqual(2, len(access.allow.permission), "Error on parsing allow (permission)")
        self.assertEqual(
            AccessPermission.READ,
            access.allow.permission[0],
            "Error on parsing allow (permission)"
        )
        self.assertEqual(
            AccessPermission.WRITE,
            access.allow.permission[1],
            "Error on parsing allow (permission)"
        )
        self.assertEqual(1, len(access.deny.principal), "Error on parsing deny (principal)")
        self.assertEqual(
            "public",
            access.deny.principal[0],
            "Error on parsing deny (principal)"
        )
        self.assertEqual(1, len(access.deny.permission), "Error on parsing deny (permission)")
        self.assertEqual(
            AccessPermission.WRITE,
            access.deny.permission[0],
            "Error on parsing deny (permission)"
        )
        self.assertEqualTree(et.fromstring(text_xml), access.to_element(), "Error on to element")

    def test_parse_none(self):
        self.assertIsNone(AccessType.parse(None, {}), "Element from nowhere")
        self.assertIsNone(AccessRole.parse(None, {}), "Element from nowhere")

    def test_referencing(self):
        text_xml = """
<access authSystem="ldap://ldap.ecoinformatics.org:389/dc=ecoinformatics,dc=org">
    <references system="http://gbif.org">Access Id</references>
</access>
        """
        access = AccessType.from_string(text_xml)
        self.assertEqual(
            "ldap://ldap.ecoinformatics.org:389/dc=ecoinformatics,dc=org",
            access.auth_system,
            "Error on parsing auth system"
        )
        self.assertEqual("Access Id", access.id, "Error on parsing id")
        self.assertEqual(Scope.DOCUMENT, access.scope, "Error on default scope")
        self.assertIsNone(access.system, "System from nowhere")
        self.assertTrue(access.referencing, "Error on parsing referencing")
        self.assertEqual("http://gbif.org", access.references.system, "Error on parsing references system")
        self.assertEqualTree(et.fromstring(text_xml), access.to_element(), "Error on to element")

    def test_error_initialization(self):
        self.assertRaises(TypeError, AccessType, "A system", order=45)

    def test_error_role_initialization(self):
        self.assertRaises(ValueError, AccessRole, [], [])
        self.assertRaises(ValueError, AccessRole, ["Control"], [])


if __name__ == '__main__':
    unittest.main()
