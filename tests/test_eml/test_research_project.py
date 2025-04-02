from unittest import main
from lxml import etree as et
from eml.types import ResearchProject, Role, ResponsibleParty, I18nString
from test_xml.test_xml import TestXML


class TestResearchProject(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "{http://www.w3.org/XML/1998/namespace}lang": "eng"
    }

    def test_parse_none(self):
        self.assertIsNone(ResearchProject.parse(None, {}), "Research Project from nowhere.")

    def test_parse_referenced(self):
        text_xml = """
<project>
    <references>some-id</references>
</project>
        """
        res_proj = ResearchProject.from_string(text_xml)
        self.assertEqual(
            "some-id",
            res_proj.id,
            "Research Project parsed incorrectly."
        )
        self.assertIsNone(res_proj.title, "Title from nowhere.")
        self.assertEqual(0, len(res_proj.personnel), "Personnel from nowhere.")
        self.assertIsNone(res_proj.abstract, "Abstract from nowhere.")
        self.assertIsNone(res_proj.funding, "Funding from nowhere.")
        self.assertEqual(0, len(res_proj.award), "Award from nowhere.")
        self.assertIsNone(res_proj.study_area_description, "Study area description from nowhere.")
        self.assertIsNone(res_proj.design_description, "Design description from nowhere.")
        self.assertEqual(0, len(res_proj.related_project), "Related project from nowhere.")
        res_proj.set_tag("project")
        self.assertEqualTree(et.fromstring(text_xml), res_proj.to_element(), "Error on to element.")

    def test_parse_simple(self):
        text_xml = """
<project>
    <title>Example Title</title>
    <personnel>
        <organizationName>Example Organization</organizationName>
        <role>contentProvider</role>
    </personnel>
</project>
        """
        res_proj = ResearchProject.from_string(text_xml)
        self.assertEqual("Example Title", res_proj.title, "Error parsing title.")
        self.assertEqual(1, len(res_proj.titles), "Error parsing titles.")
        self.assertEqual(1, len(res_proj.personnel), "Error parsing personnel.")
        self.assertEqual(Role.CONTENT_PROVIDER, res_proj.personnel[0][1], "Error parsing personnel role.")
        self.assertIsNone(res_proj.abstract, "Abstract from nowhere.")
        self.assertIsNone(res_proj.funding, "Funding from nowhere.")
        self.assertEqual(0, len(res_proj.award), "Award from nowhere.")
        self.assertIsNone(res_proj.study_area_description, "Study area description from nowhere.")
        self.assertIsNone(res_proj.design_description, "Design description from nowhere.")
        self.assertEqual(0, len(res_proj.related_project), "Related project from nowhere.")
        res_proj.set_tag("project")
        self.assertEqualTree(et.fromstring(text_xml), res_proj.to_element(), "Error on to element.")

    def test_no_title(self):
        text_xml = """
<project>
    <personnel>
        <organizationName>Example Organization</organizationName>
        <role>contentProvider</role>
    </personnel>
</project>
        """
        with self.assertRaisesRegex(TypeError, "one title"):
            ResearchProject.from_string(text_xml)

    def test_no_personnel(self):
        text_xml = """
<project>
    <title>Example Title</title>
</project>
        """
        with self.assertRaisesRegex(TypeError, "one personnel"):
            ResearchProject.from_string(text_xml)

    def test_title_as_string(self):
        res_proj = ResearchProject(
            title="Example Title",
            personnel=[(
                ResponsibleParty(organization_name=I18nString("Example Organization")),
                Role.CONTENT_PROVIDER
            )],
        )
        self.assertEqual("Example Title", res_proj.title, "Error parsing title.")
        self.assertEqual(1, len(res_proj.titles), "Error parsing titles.")
        self.assertEqual(1, len(res_proj.personnel), "Error parsing personnel.")
        self.assertEqual(Role.CONTENT_PROVIDER, res_proj.personnel[0][1], "Error parsing personnel role.")
        self.assertIsNone(res_proj.abstract, "Abstract from nowhere.")
        self.assertIsNone(res_proj.funding, "Funding from nowhere.")
        self.assertEqual(0, len(res_proj.award), "Award from nowhere.")
        self.assertIsNone(res_proj.study_area_description, "Study area description from nowhere.")
        self.assertIsNone(res_proj.design_description, "Design description from nowhere.")
        self.assertEqual(0, len(res_proj.related_project), "Related project from nowhere.")

    def test_related_project(self):
        text_xml = """
<project>
    <title>Example Title</title>
    <personnel id="ex_org">
        <organizationName>Example Organization</organizationName>
        <role>contentProvider</role>
    </personnel>
    <relatedProject>
        <title>Related Project Title</title>
        <personnel>
            <references>ex_org</references>
            <role>contentProvider</role>
        </personnel>
    </relatedProject>
</project>
        """
        res_proj = ResearchProject.from_string(text_xml)
        self.assertEqual("Example Title", res_proj.title, "Error parsing title.")
        self.assertEqual(1, len(res_proj.titles), "Error parsing titles.")
        self.assertEqual(1, len(res_proj.personnel), "Error parsing personnel.")
        self.assertEqual(Role.CONTENT_PROVIDER, res_proj.personnel[0][1], "Error parsing personnel role.")
        self.assertIsNone(res_proj.abstract, "Abstract from nowhere.")
        self.assertIsNone(res_proj.funding, "Funding from nowhere.")
        self.assertEqual(0, len(res_proj.award), "Award from nowhere.")
        self.assertIsNone(res_proj.study_area_description, "Study area description from nowhere.")
        self.assertIsNone(res_proj.design_description, "Design description from nowhere.")
        self.assertEqual(1, len(res_proj.related_project), "Error parsing related project.")
        self.assertEqual("ex_org", res_proj.related_project[0].personnel[0][0].id, "Error parsing personnel of related project.")
        res_proj.set_tag("project")
        self.assertEqualTree(et.fromstring(text_xml), res_proj.to_element(), "Error on to element.")

if __name__ == '__main__':
    main()
