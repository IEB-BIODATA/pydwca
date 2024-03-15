import unittest
from lxml import etree as et

from dwca.utils import Language
from eml.types import EMLAddress
from test_xml.test_xml import TestXML


class TestEMLAddress(TestXML):
    DEFAULT_TAGS = {
        "scope": "document",
    }

    EXAMPLE_XML = """
<address id="1" scope="system" system="https://ieb-chile.cl">
    <deliveryPoint xml:lang="esp">Calle Las Palmeras #3425</deliveryPoint>
    <city xml:lang="esp">Ñuñoa</city>
    <administrativeArea xml:lang="esp">Región Metropolitana</administrativeArea>
    <postalCode xml:lang="esp">7800003</postalCode>
    <country xml:lang="esp">Chile</country>
</address>
    """

    def test_eml_address(self):
        address = EMLAddress(
            delivery_point="7209 Coast Drive, Building 44",
            city="San Francisco",
            administrative_area="Colorado",
            postal_code="93106-2231",
            country="U.S.A.",
        )
        self.assertEqual("7209 Coast Drive, Building 44", address.delivery_point[0], "Incorrect delivery point")
        self.assertEqual(Language.ENG, address.delivery_point[0].language, "Incorrect language of delivery point")
        self.assertEqual("San Francisco", address.city, "Incorrect city")
        self.assertEqual(Language.ENG, address.city.language, "Incorrect language of city")
        self.assertEqual("Colorado", address.administrative_area, "Incorrect administrative area")
        self.assertEqual(
            Language.ENG,
            address.administrative_area.language,
            "Incorrect language of administrative area"
        )
        self.assertEqual("93106-2231", address.postal_code, "Incorrect postal_code")
        self.assertEqual(Language.ENG, address.postal_code.language, "Incorrect language of postal_code")
        self.assertEqual("U.S.A.", address.country, "Incorrect country")
        self.assertEqual(Language.ENG, address.country.language, "Incorrect language of country")

    def test_eml_address_spanish(self):
        address = EMLAddress(
            delivery_point="Calle Las Palmeras #3425",
            city="Ñuñoa",
            administrative_area="Región Metropolitana",
            postal_code="7800003",
            country="Chile",
            language=Language.ESP,
        )
        self.assertEqual("Calle Las Palmeras #3425", address.delivery_point[0], "Incorrect delivery point")
        self.assertEqual(Language.ESP, address.delivery_point[0].language, "Incorrect language of delivery point")
        self.assertEqual("Ñuñoa", address.city, "Incorrect city")
        self.assertEqual(Language.ESP, address.city.language, "Incorrect language of city")
        self.assertEqual("Región Metropolitana", address.administrative_area, "Incorrect administrative area")
        self.assertEqual(
            Language.ESP,
            address.administrative_area.language,
            "Incorrect language of administrative area"
        )
        self.assertEqual("7800003", address.postal_code, "Incorrect postal_code")
        self.assertEqual(Language.ESP, address.postal_code.language, "Incorrect language of postal_code")
        self.assertEqual("Chile", address.country, "Incorrect country")
        self.assertEqual(Language.ESP, address.country.language, "Incorrect language of country")

    def test_parse_none(self):
        self.assertIsNone(EMLAddress.parse(None, {}), "Object from None")

    def test_parse(self):
        address = EMLAddress.from_string(self.EXAMPLE_XML)
        self.assertEqual("Calle Las Palmeras #3425", address.delivery_point[0], "Incorrectly set delivery point")
        self.assertEqual("Ñuñoa", address.city, "Incorrectly set city")
        self.assertEqual(
            "Región Metropolitana",
            address.administrative_area,
            "Incorrectly set city administrative area"
        )
        self.assertEqual("7800003", address.postal_code, "Incorrectly set postal code")
        self.assertEqual("Chile", address.country, "Incorrectly set country")
        self.assertEqualTree(et.fromstring(self.EXAMPLE_XML), address.to_element(), "Error on to element")

    def test_mode_delivery_point(self):
        example_xml = self.EXAMPLE_XML.replace(
            '<deliveryPoint xml:lang="esp">Calle Las Palmeras #3425</deliveryPoint>',
            """
<deliveryPoint
    xml:lang="esp"
>Calle Las Palmeras #3425</deliveryPoint>
<deliveryPoint
    xml:lang="eng"
>Street Las Palmeras #3425</deliveryPoint>
            """
        )
        address = EMLAddress.from_string(example_xml)
        self.assertEqual(2, len(address.delivery_point), "Incorrectly set delivery point")
        self.assertEqual(
            "Calle Las Palmeras #3425",
            address.delivery_point[0],
            "Incorrectly set spanish delivery point"
        )
        self.assertEqual(
            "Street Las Palmeras #3425",
            address.delivery_point[1],
            "Incorrectly set english delivery point"
        )
        self.assertEqual(
            Language.ESP,
            address.delivery_point[0].language,
            "Incorrectly set spanish delivery point language"
        )
        self.assertEqual(
            Language.ENG,
            address.delivery_point[1].language,
            "Incorrectly set english delivery point language"
        )
        self.assertEqualTree(et.fromstring(example_xml), address.to_element(), "Error on to element")

    def test_wrong_scope(self):
        example_xml = self.EXAMPLE_XML.replace('scope="system"', 'scope="invalidScope"')
        self.assertRaises(ValueError, EMLAddress.from_string, example_xml)

    def test_reference(self):
        reference_xml = """
<address>
    <references>1</references>
</address>
        """
        eml_address = EMLAddress.from_string(reference_xml)
        self.assertEqual("1", eml_address.id, "Id set incorrectly")
        self.assertTrue(eml_address.referencing, "Referencing wrong initialized")
        self.assertIsNone(
            eml_address.references.system,
            "References system wrong initialized"
        )
        self.assertEqualTree(
            et.fromstring(reference_xml),
            eml_address.to_element(),
            "Wrong referrer to element"
        )

    def test_reference_system(self):
        reference_xml = """
<address>
    <references system="http://gbif.org">1</references>
</address>
        """
        eml_address = EMLAddress.from_string(reference_xml)
        self.assertEqual("1", eml_address.id, "Id set incorrectly")
        self.assertTrue(eml_address.referencing, "Referencing wrong initialized")
        self.assertEqual(
            "http://gbif.org",
            eml_address.references.system,
            "References system wrong initialized"
        )
        self.assertEqualTree(
            et.fromstring(reference_xml),
            eml_address.to_element(),
            "Wrong referrer to element"
        )

    def test_invalid_reference(self):
        reference_xml = """
<address id="10">
    <references>1</references>
</address>
        """
        self.assertRaises(
            AssertionError,
            EMLAddress.from_string,
            reference_xml
        )

    # TODO: Test different ways to equal on Address


if __name__ == '__main__':
    unittest.main()
