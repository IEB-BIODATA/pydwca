import unittest

from dwca.terms import DWCLanguage
from xml_common.utils import Language


class RecordLevelTest(unittest.TestCase):

    def test_format(self):
        language_field = DWCLanguage(1)
        self.assertEqual(language_field.format("en"), Language.ENG)
        self.assertEqual(language_field.format("english"), Language.ENG)
        self.assertEqual(language_field.format("English"), Language.ENG)
        self.assertEqual(language_field.format("ENG"), Language.ENG)
        self.assertEqual(language_field.format("eng"), Language.ENG)
        self.assertEqual(language_field.format("es"), Language.SPA)
        self.assertEqual(language_field.format("spanish"), Language.SPA)
        self.assertEqual(language_field.format("Spanish"), Language.SPA)
        self.assertEqual(language_field.format("SPA"), Language.SPA)
        self.assertEqual(language_field.format("spa"), Language.SPA)
        self.assertEqual(language_field.format("sdgdfgd"), Language.UND)

    def test_unformat(self):
        language_field = DWCLanguage(1)
        self.assertEqual(language_field.unformat(Language.ENG), "eng")
        self.assertEqual(language_field.unformat(Language.SPA), "spa")
        self.assertEqual(language_field.unformat(Language.CAL), "cal")

    def test_unformat_two_letters(self):
        language_field = DWCLanguage(1, two_letter_coding=True)
        self.assertEqual(language_field.unformat(Language.ENG), "en")
        self.assertEqual(language_field.unformat(Language.SPA), "es")
        with self.assertRaisesRegex(ValueError, "does not have a two-letters"):
            language_field.unformat(Language.CAL)
            language_field.unformat(Language.UND)


if __name__ == '__main__':
    unittest.main()
