import datetime
import os
import unittest

import requests
import datetime as dt
from lxml import etree as et

from eml.base import EML, EMLVersion
from dwca.utils import Language
from eml.resources import EMLResource, EMLKeywordSet, EMLLicense, EMLDistribution, EMLCoverage
from eml.resources.coverage import TemporalCoverage
from eml.resources.distribution import EMLOnline, EMLOffline
from eml.types import Scope, ResponsibleParty, IndividualName, OrganizationName, PositionName, Role, I18nString, \
    EMLTextType, SemanticAnnotation
from test_xml.test_xml import TestXML

PATH = os.path.abspath(os.path.dirname(__file__))


class TestEML(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "phonetype": "voice",
    }

    def setUp(self) -> None:
        eml_path = os.path.join(PATH, os.pardir, "example_data", "eml.xml")
        self.eml = EML.from_xml(eml_path)
        with open(eml_path, "r", encoding="utf-8") as file:
            self.text_eml = file.read()
        self.element_eml = et.fromstring(self.text_eml)
        self.empty_eml = EML(
            package_id="Example package",
            system="http://my.system",
            resource_type=EMLResource.DATASET,
        )
        return

    def initialize_resource(self, **kwargs):
        self.empty_eml.initialize_resource(
            "Example Title",
            ResponsibleParty(individual_name=IndividualName(first_name="Joe", last_name="Doe")),
            contact=[ResponsibleParty(position_name=PositionName("Contact"))],
            **kwargs
        )

    @staticmethod
    def check_online_test(text: str) -> bool:
        try:
            status = text.split(": ")[-1].lower().strip(".")
            if status == "passed":
                return True
            elif status == "failed":
                return False
            else:
                raise AssertionError(f"Unexpected status: {status}")
        except Exception as e:
            raise AssertionError("Error parsing response status" + str(e))

    @staticmethod
    def validate(eml: str):
        url = "https://knb.ecoinformatics.org/emlparser/parse"
        form_data = {
            "action": "textparse",
            "doctext": eml
        }
        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            root = et.fromstring(response.content, parser=et.HTMLParser())
            h4_elements = root.xpath('//h4')
            # EML Test
            eml_response = TestEML.check_online_test(h4_elements[0].text)
            if not eml_response:
                errors = "\n\t".join([error.text for error in h4_elements[0].getnext().getnext()])
                raise AssertionError(f"Error on parsing EML specific test:\n\t{errors}")
            # XML Test
            xml_response = TestEML.check_online_test(h4_elements[1].text)
            if not xml_response:
                raise AssertionError(f"Error on parsing XML specific test: {h4_elements[1].getnext().getnext().text}")
        else:
            raise AssertionError("Request failed with status code:", response.status_code)

    def test_simple_eml(self):
        self.initialize_resource()
        self.validate(self.empty_eml.to_xml())

    def test_parse(self):
        self.assertEqual("Example Package", self.eml.package_id, "Error on package id read")
        self.assertEqual("http://gbif.org", self.eml.system, "Error on system")
        self.assertEqual(Scope.SYSTEM, self.eml.scope, "Error on Scope")
        self.assertEqual(Language.ENG, self.eml.language, "Wrong language")
        self.assertEqual(EMLResource.DATASET, self.eml.resource_type, "Wrong resource type found")
        self.assertIsNone(self.eml.access, "Access from nothing")
        self.assertEqual(0, len(self.eml.annotations), "Annotations from nothing")
        self.assertEqual(1, len(self.eml.additional_metadata), "Additional metadata not found")
        self.assertEqualTree(self.element_eml, self.eml.to_element(), "Error on generated element")

    def test_eml_version(self):
        self.assertEqual(EMLVersion.LATEST, EMLVersion.get_version(None), "Wrong default")
        self.assertRaises(
            NotImplementedError,
            EMLVersion.get_version,
            "any_url another_url"
        )

    def test_str(self):
        self.assertEqual(
            """EML:
\tResource Type: DATASET
\tTitle: Example for Darwin Core Archive
\tCreator: Creator Organization
\tMetadataProvider: Metadata Manager at Metadata Provider Organization
\tCustodian Steward: Doe, J. (Custodian Steward)
\tOriginator: Doe, J.
\tAuthor: Example, J.""",
            str(self.eml),
            "Wrong string of EML"
        )

    def test_referrer(self):
        self.assertRaises(ValueError, self.eml.get_referrer, et.Element("example"), {})

    def test_set_title(self):
        self.initialize_resource()
        self.assertEqual(
            "Example Title",
            self.empty_eml.resource.title,
            "Title did not set"
        )
        self.assertEqual(
            Language.ENG,
            self.empty_eml.resource.title.language,
            "Language did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_title_lang(self):
        self.initialize_resource()
        self.empty_eml.add_title("Título de ejemplo", Language.ESP)
        self.assertEqual(
            "Título de ejemplo",
            self.empty_eml.resource.titles[1],
            "Title did not set"
        )
        self.assertEqual(
            Language.ESP,
            self.empty_eml.resource.titles[1].language,
            "Language did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_titles(self):
        self.empty_eml.initialize_resource(
            ["Example Title", I18nString("Título de ejemplo", Language.ESP)],
            ResponsibleParty(individual_name=IndividualName(first_name="Joe", last_name="Doe")),
            contact=[ResponsibleParty(position_name=PositionName("Contact"))]
        )
        self.assertEqual(
            "Example Title",
            self.empty_eml.resource.title,
            "Title did not set"
        )
        self.assertEqual(
            Language.ENG,
            self.empty_eml.resource.title.language,
            "Language did not set"
        )
        self.assertEqual(
            "Título de ejemplo",
            self.empty_eml.resource.titles[1],
            "Title did not set"
        )
        self.assertEqual(
            Language.ESP,
            self.empty_eml.resource.titles[1].language,
            "Language did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_creator(self):
        self.initialize_resource()
        self.assertEqual(
            "Doe, J.",
            str(self.empty_eml.resource.creator),
            "First creator did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_add_creator(self):
        self.empty_eml.initialize_resource(
            "Example title", [
                ResponsibleParty(individual_name=IndividualName(first_name="Joe", last_name="Doe")),
                ResponsibleParty(organization_name=OrganizationName("Example Organization")),
            ],
            contact=[ResponsibleParty(position_name=PositionName("Contact"))]
        )
        self.empty_eml.add_creator(
            ResponsibleParty(individual_name=IndividualName(first_name="John", last_name="Doe"))
        )
        self.assertEqual(
            "Doe, J.",
            str(self.empty_eml.resource.creator),
            "First creator did not set"
        )
        self.assertEqual(
            "Example Organization",
            str(self.empty_eml.resource.creators[1]),
            "Creator did not set"
        )
        self.assertEqual(
            "Doe, J.",
            str(self.empty_eml.resource.creators[2]),
            "Creator did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_alternative(self):
        self.initialize_resource()
        self.assertEqual(
            0, len(self.empty_eml.resource.alternative_identifiers),
            "Alternative identifiers initialized from nowhere"
        )
        self.empty_eml.add_alternative_identifier("Example Alternative Identifier")
        self.assertEqual(
            "Example Alternative Identifier",
            self.empty_eml.resource.alternative_identifiers[0],
            "Alternative identifier did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_short_name(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.short_name)
        self.empty_eml.set_short_name("A short Name")
        self.assertEqual(
            "A short Name", self.empty_eml.resource.short_name,
            "Short Name did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_metadata_provider(self):
        self.initialize_resource()
        self.assertEqual(
            0, len(self.empty_eml.resource.metadata_provider),
            "Metadata Provider from nowhere"
        )
        self.empty_eml.add_metadata_provider(ResponsibleParty(
            individual_name=IndividualName(first_name="Joe", last_name="Doe")
        ))
        self.empty_eml.add_metadata_provider(ResponsibleParty(
            organization_name=OrganizationName("Example Organization")
        ))
        self.assertEqual(
            "Doe, J.",
            str(self.empty_eml.resource.metadata_provider[0]),
            "Metadata provider did not set"
        )
        self.assertEqual(
            "Example Organization",
            str(self.empty_eml.resource.metadata_provider[1]),
            "Metadata provider did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_associated_party(self):
        self.initialize_resource()
        self.assertEqual(
            0, len(self.empty_eml.resource.associated_party),
            "Associated Party from nowhere"
        )
        self.empty_eml.add_associated_party(
            ResponsibleParty(
                individual_name=IndividualName(first_name="Joe", last_name="Doe")
            ), Role.USER
        )
        self.empty_eml.add_associated_party(
            ResponsibleParty(
                individual_name=IndividualName(first_name="John", last_name="Doe")
            ), Role.ORIGINATOR
        )
        self.assertEqual(
            "Doe, J.", str(self.empty_eml.resource.associated_party[0][0]),
            "Associated Party did not set"
        )
        self.assertEqual(
            "Doe, J.", str(self.empty_eml.resource.associated_party[1][0]),
            "Associated Party did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_pub_date(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.publication_date, "Publication date from nowhere")
        date = datetime.date.today()
        self.empty_eml.set_pub_date(date)
        self.assertEqual(
            date, self.empty_eml.resource.publication_date,
            "Publication date did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_language(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.language, "Language from nowhere")
        self.empty_eml.set_language(Language.ENG)
        self.assertEqual(
            Language.ENG, self.empty_eml.resource.language,
            "Language did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_series(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.series, "Series from nowhere")
        self.empty_eml.set_series("Volume 20")
        self.assertEqual(
            "Volume 20", self.empty_eml.resource.series,
            "Series did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_abstract(self):
        abstract = ("Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit. Etiam vitae diam nec eros "
                    "interdum posuere. Class aptent taciti sociosqu "
                    "ad litora torquent per conubia nostra, "
                    "per inceptos himenaeos. Etiam vel dui "
                    "dignissim, aliquet felis ut, varius ligula. "
                    "Ut condimentum sapien in felis posuere, eu "
                    "aliquam enim lobortis. Vivamus sodales tortor "
                    "at augue gravida feugiat. Aenean faucibus "
                    "felis id aliquet euismod egestas.")
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.abstract, "Abstract from nowhere")
        self.empty_eml.set_abstract(EMLTextType(paragraphs=[abstract]))
        self.assertEqual(
            abstract, self.empty_eml.resource.abstract.paragraphs[0],
            "Abstract did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_keyword_set(self):
        self.initialize_resource()
        self.assertEqual(0, len(self.empty_eml.resource.keyword_set), "Keyword set from nowhere")
        self.empty_eml.add_keyword_set(EMLKeywordSet(["biodiversity"]))
        self.assertEqual(
            1, len(self.empty_eml.resource.keyword_set),
            "Keyword set did not set"
        )
        self.empty_eml.add_keyword_set(EMLKeywordSet(["checklist"]))
        self.assertEqual(
            2, len(self.empty_eml.resource.keyword_set),
            "Keyword set did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_additional_info(self):
        self.initialize_resource()
        self.assertEqual(0, len(self.empty_eml.resource.additional_info), "Additional information from nowhere")
        self.empty_eml.add_additional_info(EMLTextType())
        self.assertEqual(
            1, len(self.empty_eml.resource.additional_info),
            "Additional info did not set"
        )
        self.empty_eml.add_additional_info(EMLTextType())
        self.assertEqual(
            2, len(self.empty_eml.resource.additional_info),
            "Additional info did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_intellectual_rights(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.intellectual_rights, "Intellectual rights from nowhere")
        self.empty_eml.set_intellectual_rights(EMLTextType(paragraphs=["CC-by"]))
        self.assertEqual(
            "CC-by", self.empty_eml.resource.intellectual_rights.paragraphs[0],
            "Intellectual rights did not set"
        )
        self.empty_eml.set_intellectual_rights(EMLTextType(paragraphs=["by-nc-nd"]))
        self.assertEqual(
            "by-nc-nd", self.empty_eml.resource.intellectual_rights.paragraphs[0],
            "Intellectual rights did not overwrite"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_licensed(self):
        self.initialize_resource()
        self.assertEqual(0, len(self.empty_eml.resource.licensed), "Licensed from nowhere")
        self.empty_eml.add_licensed(EMLLicense(name="Apache License 1.0"))
        self.assertEqual(
            1, len(self.empty_eml.resource.licensed),
            "Licensed did not set"
        )
        self.empty_eml.add_licensed(EMLLicense(name="Apache License 2.0"))
        self.assertEqual(
            2, len(self.empty_eml.resource.licensed),
            "Licensed did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_distribution(self):
        self.initialize_resource()
        self.assertEqual(0, len(self.empty_eml.resource.distribution), "Distribution from nowhere")
        self.empty_eml.add_distribution(EMLDistribution(online=EMLOnline(url="http://data.org/getdata?id=98332")))
        self.assertEqual(
            1, len(self.empty_eml.resource.distribution),
            "Distribution did not set"
        )
        self.validate(self.empty_eml.to_xml())
        self.empty_eml.add_distribution(EMLDistribution(offline=EMLOffline("Tape, 3.5 inch Floppy Disk, hardcopy")))
        self.assertEqual(
            2, len(self.empty_eml.resource.distribution),
            "Distribution did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_coverage(self):
        self.initialize_resource()
        self.assertIsNone(self.empty_eml.resource.coverage, "Coverage from nowhere")
        self.empty_eml.set_coverage(EMLCoverage(
            temporal=TemporalCoverage(single_datetime=[dt.date.today()])
        ))
        self.assertIsNotNone(
            self.empty_eml.resource.coverage,
            "Coverage did not set"
        )
        self.validate(self.empty_eml.to_xml())

    def test_set_annotation(self):
        self.initialize_resource(_id="1")
        self.assertEqual(0, len(self.empty_eml.resource.annotation), "Annotation from nowhere")
        self.empty_eml.add_annotation(SemanticAnnotation(
            ("http://example.org/height", "height"),
            ("http://example.org/tall", "tall"))
        )
        self.assertEqual(
            1, len(self.empty_eml.resource.annotation),
            "Annotation did not set"
        )
        self.empty_eml.add_annotation(SemanticAnnotation(
            ("http://example.org/widht", "width"),
            ("http://example.org/thick", "thick"))
        )
        self.assertEqual(
            2, len(self.empty_eml.resource.annotation),
            "Annotation did not set"
        )
        self.validate(self.empty_eml.to_xml())


if __name__ == '__main__':
    unittest.main()
