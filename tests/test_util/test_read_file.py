import unittest

from xml_common.utils import read_string


class TestReadFile(unittest.TestCase):
    def test_read_string(self):
        self.assertEqual(
            "This is a string",
            read_string("This is a string"),
            "String parsed correctly."
        )

    def test_read_bytes(self):
        self.assertEqual(
            "This is a bytes",
            read_string(b"This is a bytes"),
            "Bytes parsed correctly."
        )

    def test_read_with_encoding(self):
        an_string = "This is a string to be passed as ascii"
        as_ansi = an_string.encode("ascii")
        self.assertEqual(
            an_string,
            read_string(as_ansi, encoding="ascii"),
            "String as ansi parsed correctly."
        )


if __name__ == "__main__":
    unittest.main()
