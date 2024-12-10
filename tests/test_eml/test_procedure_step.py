from unittest import main
from lxml import etree as et
from pygments.lexers import q

from eml.resources import EMLCitation, EMLProtocol
from eml.types import ProcedureStep, EMLTextType
from test_xml.test_xml import TestXML


class TestProcedureStep(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        'scope': 'document',
    }

    def test_parse_none(self):
        self.assertIsNone(ProcedureStep.parse(None, {}), "Procedure Step from nowhere.")

    def test_parse_simple(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_citation_protocol_error(self):
        citation = EMLCitation(_id="cite-id", referencing=True)
        protocol = EMLProtocol(_id="protocol-id", referencing=True)
        with self.assertRaisesRegex(TypeError, "allow only one"):
            ProcedureStep(description=EMLTextType(paragraphs=["Lorem ipsum"]), citation=citation, protocol=protocol)

    def test_parse_error(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <citation>
        <references>cite-id</references>
    </citation>
    <protocol>
        <references>protocol-id</references>
    </protocol>
</methodStep>
        """
        with self.assertRaisesRegex(TypeError, "allow only one"):
            ProcedureStep.from_string(xml_text)

    def test_parse_citation(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <citation>
        <references>cite-id</references>
    </citation>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertEqual("cite-id", procedure.citation.id, "Error parsing citation.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_protocol(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <protocol>
        <references>protocol-id</references>
    </protocol>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertEqual("protocol-id", procedure.protocol.id, "Error parsing protocol.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_single_instrumentation(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <instrumentation>LACHAT analyzer, model XYX</instrumentation>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(1, len(procedure.instrumentation), "Error parsing single instrumentation.")
        self.assertEqual("LACHAT analyzer, model XYX", procedure.instrumentation[0], "Error parsing instrumentation.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_instrumentation(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <instrumentation>LACHAT analyzer, model XYX</instrumentation>
    <instrumentation>Microscope, model ABBA</instrumentation>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(2, len(procedure.instrumentation), "Error parsing instrumentations.")
        self.assertEqual("Microscope, model ABBA", procedure.instrumentation[1], "Error parsing second instrumentation.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_software(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <software>
        <references>software-id</references>
    </software>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual("software-id", procedure.software[0].id, "Error parsing software.")
        self.assertEqual(0, len(procedure.sub_step), "Sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_sub_step(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <subStep>
        <description>
            <para>Nested sub step</para>
        </description>
    </subStep>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(1, len(procedure.sub_step), "Error parsing sub step.")
        self.assertEqual(
            "Nested sub step",
            procedure.sub_step[0].description.paragraphs[0],
            "Error parsing sub step description."
        )
        self.assertIsNone(procedure.sub_step[0].citation, "Citation from nowhere.")
        self.assertIsNone(procedure.sub_step[0].protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.sub_step[0].instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.sub_step[0].software), "Software from nowhere.")
        self.assertEqual(0, len(procedure.sub_step[0].sub_step), "Sub sub step from nowhere.")
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")

    def test_parse_complex_sub_step(self):
        xml_text = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
    <subStep>
        <description>
            <para>Nested sub step</para>
        </description>
        <subStep>
            <description>
                <para>First second nested sub step</para>
            </description>
        </subStep>
        <subStep>
            <description>
                <para>Second second nested sub step</para>
            </description>
        </subStep>
    </subStep>
</methodStep>
        """
        procedure = ProcedureStep.from_string(xml_text)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            procedure.description.paragraphs[0],
            "Error parsing description."
        )
        self.assertIsNone(procedure.citation, "Citation from nowhere.")
        self.assertIsNone(procedure.protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.software), "Software from nowhere.")
        self.assertEqual(1, len(procedure.sub_step), "Error parsing sub step.")
        self.assertEqual(
            "Nested sub step",
            procedure.sub_step[0].description.paragraphs[0],
            "Error parsing sub step description."
        )
        self.assertIsNone(procedure.sub_step[0].citation, "Citation from nowhere.")
        self.assertIsNone(procedure.sub_step[0].protocol, "Protocol from nowhere.")
        self.assertEqual(0, len(procedure.sub_step[0].instrumentation), "Instrumentation from nowhere.")
        self.assertEqual(0, len(procedure.sub_step[0].software), "Software from nowhere.")
        self.assertEqual(2, len(procedure.sub_step[0].sub_step), "Error parsing nested sub step.")
        self.assertEqual(
            "Second second nested sub step",
            procedure.sub_step[0].sub_step[1].description.paragraphs[0],
            "Error parsing nested sub step description."
        )
        procedure.set_tag("methodStep")
        self.assertEqualTree(et.fromstring(xml_text), procedure.to_element(), "Error on element conversion.")


if __name__ == '__main__':
    main()
