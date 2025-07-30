import unittest

from xml_common.utils import Language


class LanguageTest(unittest.TestCase):
    def test_word(self):
        self.assertEqual(Language.get_language("Spanish"), Language.SPA)
        self.assertEqual(Language.get_language("English"), Language.ENG)
        self.assertEqual(Language.get_language("Carolinian"), Language.CAL)
        self.assertEqual(Language.get_language("Undetermined"), Language.UND)

    def test_word_cap(self):
        self.assertEqual(Language.get_language("SPANISH"), Language.SPA)
        self.assertEqual(Language.get_language("ENGLISH"), Language.ENG)
        self.assertEqual(Language.get_language("CAROLINIAN"), Language.CAL)
        self.assertEqual(Language.get_language("UNDETERMINED"), Language.UND)

    def test_word_lower(self):
        self.assertEqual(Language.get_language("spanish"), Language.SPA)
        self.assertEqual(Language.get_language("english"), Language.ENG)
        self.assertEqual(Language.get_language("carolinian"), Language.CAL)
        self.assertEqual(Language.get_language("undetermined"), Language.UND)

    def test_two_letter(self):
        self.assertEqual(Language.get_language("es"), Language.SPA)
        self.assertEqual(Language.get_language("en"), Language.ENG)
        self.assertEqual(Language.get_language("mk"), Language.MKD)

    def test_three_letter(self):
        self.assertEqual(Language.get_language("spa"), Language.SPA)
        self.assertEqual(Language.get_language("eng"), Language.ENG)
        self.assertEqual(Language.get_language("mkd"), Language.MKD)
        self.assertEqual(Language.get_language("und"), Language.UND)

    def test_three_letter_cap(self):
        self.assertEqual(Language.get_language("SPA"), Language.SPA)
        self.assertEqual(Language.get_language("ENG"), Language.ENG)
        self.assertEqual(Language.get_language("CAL"), Language.CAL)
        self.assertEqual(Language.get_language("UND"), Language.UND)

    def test_special(self):
        self.assertEqual(Language.get_language(""), Language.UND)
        with self.assertRaisesRegex(NotImplementedError, "dfsgsdfg language not implemented yet"):
            Language.get_language("dfsgsdfg")

    def test_two_letters_return(self):
        self.assertEqual("es", Language.SPA.two_letters)
        self.assertEqual("en", Language.ENG.two_letters)
        with self.assertRaisesRegex(ValueError, "does not have a two-letters"):
            Language.CAL.two_letters


if __name__ == '__main__':
    unittest.main()
