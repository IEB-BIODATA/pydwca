import unittest

from xml_common.utils import CamelCaseEnum


class TestCamelCaseEnum(unittest.TestCase):
    class ExampleCamelCaseEnum(CamelCaseEnum):
        ONE_VALUE = 1
        TWO_VALUE = 2
        THREE_VALUE = 3
        NOCONVERSIONVALUE = 4

    def test_to_camel_case(self):
        self.assertEqual(
            "oneValue",
            TestCamelCaseEnum.ExampleCamelCaseEnum.ONE_VALUE.to_camel_case(),
            "Wrong conversion to camel case (oneValue)."
        )
        self.assertEqual(
            "twoValue",
            TestCamelCaseEnum.ExampleCamelCaseEnum.TWO_VALUE.to_camel_case(),
            "Wrong conversion to camel case (twoValue)."
        )
        self.assertEqual(
            "threeValue",
            TestCamelCaseEnum.ExampleCamelCaseEnum.THREE_VALUE.to_camel_case(),
            "Wrong conversion to camel case (threeValue)."
        )
        self.assertEqual(
            "noconversionvalue",
            TestCamelCaseEnum.ExampleCamelCaseEnum.NOCONVERSIONVALUE.to_camel_case(),
            "Wrong conversion to camel case (noconversionvalue)."
        )

    def test_to_str(self):
        self.assertEqual(
            "One Value",
            str(TestCamelCaseEnum.ExampleCamelCaseEnum.ONE_VALUE),
            "Wrong conversion to str (One Value)."
        )
        self.assertEqual(
            "Two Value",
            str(TestCamelCaseEnum.ExampleCamelCaseEnum.TWO_VALUE),
            "Wrong conversion to str (Two Value)."
        )
        self.assertEqual(
            "Three Value",
            str(TestCamelCaseEnum.ExampleCamelCaseEnum.THREE_VALUE),
            "Wrong conversion to str (Three Value)."
        )
        self.assertEqual(
            "Noconversionvalue",
            str(TestCamelCaseEnum.ExampleCamelCaseEnum.NOCONVERSIONVALUE),
            "Wrong conversion to str (noconversionvalue)."
        )

    def test_get_enum(self):
        self.assertEqual(
            TestCamelCaseEnum.ExampleCamelCaseEnum.ONE_VALUE,
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("oneValue"),
            "Wrong parse one Value."
        )
        self.assertEqual(
            TestCamelCaseEnum.ExampleCamelCaseEnum.TWO_VALUE,
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("twoValue"),
            "Wrong parse two Value."
        )
        self.assertEqual(
            TestCamelCaseEnum.ExampleCamelCaseEnum.THREE_VALUE,
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("threeValue"),
            "Wrong parse three Value."
        )
        self.assertEqual(
            TestCamelCaseEnum.ExampleCamelCaseEnum.NOCONVERSIONVALUE,
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("noconversionvalue"),
            "Wrong parse noconversionvalue."
        )
        with self.assertRaisesRegex(ValueError, "No Conversion Value", msg="No Conversion Value parsed anyway."):
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("No Conversion Value")
        with self.assertRaisesRegex(ValueError, "fourValue", msg="Not present value parsed anyway."):
            TestCamelCaseEnum.ExampleCamelCaseEnum.get_enum("fourValue")


if __name__ == '__main__':
    unittest.main()
