import unittest

from dwca.utils import EstablishmentMeans


class TestEstablishmentMeans(unittest.TestCase):
    def test_camel_case(self):
        native = EstablishmentMeans(1)
        self.assertEqual("native", native.to_camel_case(), "Error on one word establishment")
        assisted = EstablishmentMeans(4)
        self.assertEqual(
            "introducedAssistedColonisation",
            assisted.to_camel_case(),
            "Error on multiple word establishment"
        )

    def test_iri(self):
        native = EstablishmentMeans.NATIVE
        self.assertEqual(
            "http://rs.tdwg.org/dwcem/values/e001",
            native.get_iri(),
            "Error on uri generation"
        )

    def test_get_establishment(self):
        self.assertEqual(
            EstablishmentMeans.NATIVE,
            EstablishmentMeans.get_enum("native"),
            "Error on one word establishment")
        self.assertEqual(
            EstablishmentMeans.INTRODUCED_ASSISTED_COLONISATION,
            EstablishmentMeans.get_enum("introducedAssistedColonisation"),
            "Error on multiple word establishment"
        )


if __name__ == '__main__':
    unittest.main()
