from unittest import main
from lxml import etree as et

from eml.resources import EMLDataset
from eml.types import Methods, ProcedureStep
from test_xml.test_xml import TestXML


class TestMethods(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "scope": "document"
    }

    def test_parse_none(self):
        self.assertIsNone(Methods.parse(None, {}), "Methods from nowhere.")

    def test_parse_empty(self):
        text_xml = """
<methods>
</methods>
        """
        with self.assertRaisesRegex(TypeError, "At least one step must be given."):
            Methods.from_string(text_xml)

    def test_parse_simple(self):
        text_xml = """
<methods>
    <methodStep>
        <description>
            <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
        </description>
    </methodStep>
</methods>
        """
        methods = Methods.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            methods.method_steps[0].description.paragraphs[0],
            "Error parsing method step."
        )
        self.assertIsNone(methods.sampling, "Sampling method from nowhere.")
        self.assertEqual(0, len(methods.quality_control), "Quality control from nowhere.")
        self.assertEqualTree(et.fromstring(text_xml), methods.to_element(), "Error on to element.")

    def test_parse_data_source(self):
        text_xml = """
<methods>
    <methodStep>
        <description>
            <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
        </description>
        <dataSource>
            <references>dataset-1</references>
        </dataSource>
    </methodStep>
</methods>
        """
        methods = Methods.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            methods.method_steps[0].description.paragraphs[0],
            "Error parsing method step."
        )
        self.assertIsNone(methods.sampling, "Sampling method from nowhere.")
        self.assertEqual(0, len(methods.quality_control), "Quality control from nowhere.")
        self.assertEqualTree(et.fromstring(text_xml), methods.to_element(), "Error on to element.")

    def test_parse_data_source_complex(self):
        text_xml = """
<methods>
    <methodStep>
        <description>
            <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</para>
        </description>
        <dataSource>
            <references>dataset-1</references>
        </dataSource>
    </methodStep>
    <methodStep>
        <description>
            <para>Etiam vitae diam nec eros interdum posuere.</para>
        </description>
    </methodStep>
</methods>
        """
        methods = Methods.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            methods.method_steps[0].description.paragraphs[0],
            "Error parsing method step."
        )
        self.assertIsNone(methods.sampling, "Sampling method from nowhere.")
        self.assertEqual(0, len(methods.quality_control), "Quality control from nowhere.")
        self.assertEqualTree(et.fromstring(text_xml), methods.to_element(), "Error on to element.")

    def test_incomplete_data_source(self):
        methods = Methods(
            method_steps=[
                ProcedureStep.from_string("<methodStep><description>"
                                          "<para>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</para>"
                                          "</description></methodStep>"),
                ProcedureStep.from_string("<methodStep><description>"
                                          "<para>Etiam vitae diam nec eros interdum posuere.</para>"
                                          "</description></methodStep>"),
            ],
            data_sources=[
                [EMLDataset(_id="dataset-1", referencing=True)],
            ]
        )
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            methods.method_steps[0].description.paragraphs[0],
            "Error initializing methods."
        )
        self.assertEqual(
            0, len(methods.method_steps[1].data_source),
            "Data source from nowhere on second step."
        )

    def test_parse_method_step(self):
        text_xml = """
<methodStep>
    <description>
        <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
    </description>
</methodStep>
        """
        method_step = Methods.MethodStep.from_string(text_xml)
        self.assertEqualTree(et.fromstring(text_xml), method_step.to_element(), "Error on step method to element.")

    def test_parse_sampling(self):
        text_xml = """
<methods>
    <methodStep>
        <description>
            <para>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.</para>
        </description>
    </methodStep>
    <sampling>
    </sampling>
</methods>
        """
        methods = Methods.from_string(text_xml)
        self.assertEqual(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae diam nec eros interdum posuere.",
            methods.method_steps[0].description.paragraphs[0],
            "Error parsing method step."
        )
        # self.assertIsNone(methods.sampling, "Sampling method from nowhere.")
        # self.assertEqual(0, len(methods.quality_control), "Quality control from nowhere.")
        # self.assertEqualTree(et.fromstring(text_xml), methods.to_element(), "Error on to element.")


if __name__ == '__main__':
    main()
