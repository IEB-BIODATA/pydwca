import unittest
from unittest.mock import patch

import tqdm

from xml_common.utils import OptionalTqdm, iterate_with_bar
from xml_common.utils.iteratate import is_notebook, get_optional_iterator

orig_import = __import__

def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'IPython':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


def import_mock_tqdm(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'tqdm':
        raise ImportError(f"No module named '{name}'")
    return orig_import(name, globals, locals, fromlist, level)


class TestIterator(unittest.TestCase):
    @patch("IPython.get_ipython", return_value=True)
    def test_is_notebook(self, mock_get_ipython):
        self.assertTrue(is_notebook())

    def test_is_terminal(self):
        self.assertFalse(is_notebook())

    @patch('builtins.__import__', side_effect=import_mock)
    def test_is_terminal_no_module(self, mock_import):
        self.assertFalse(is_notebook())

    @patch('builtins.__import__', side_effect=import_mock_tqdm)
    def test_optional_iterator(self, mock_import):
        a = [1, 2, 6, 5]
        tqdm_optional = get_optional_iterator(iterator=a)
        self.assertEqual(a, tqdm_optional, "Incorrect iterator")
        new_tqdm = get_optional_iterator()
        self.assertIsNone(new_tqdm, "New tqdm is not None")
        iterate_bar = iterate_with_bar(a)
        self.assertEqual(a, tqdm_optional, "Incorrect bar iterator")

    def test_optional_tqdm_iterator(self):
        a = [1, 2, 6, 5]
        tqdm_optional = get_optional_iterator(iterator=a)
        self.assertTrue(isinstance(tqdm_optional, tqdm.tqdm), "Incorrect iterator")
        new_tqdm = get_optional_iterator()
        self.assertTrue(isinstance(new_tqdm, tqdm.tqdm), "Incorrect new tqdm")
        iterate_bar = iterate_with_bar(a)
        self.assertTrue(isinstance(iterate_bar, tqdm.tqdm), "Incorrect bar iterator")

    @patch("IPython.get_ipython", return_value=True)
    def test_optional_tqdm_ipython(self, mock_get_ipython):
        a = [1, 2, 6, 5]
        # Strange behaviour because of this is not a notebook
        tqdm_optional = get_optional_iterator(iterator=a)
        self.assertEqual(a, tqdm_optional, "Incorrect iterator")
        new_tqdm = get_optional_iterator()
        self.assertIsNone(new_tqdm, "New tqdm is not None")
        tqdm_optional = iterate_with_bar(a)
        self.assertEqual(a, tqdm_optional, "Incorrect bar iterator")

    def test_optional_tqdm(self):
        a = OptionalTqdm()
        self.assertTrue(isinstance(a.__tqdm__, tqdm.tqdm), "Incorrect tqdm")
        a.set_descriptor(desc="A descriptor")
        self.assertEqual("A descriptor: ", a.__tqdm__.desc, "Descriptor not set")
        self.assertEqual(0, a.__tqdm__.n, "Wrong initial")
        a.update()
        self.assertEqual(1, a.__tqdm__.n, "Not updated")
        a.reset()
        self.assertEqual(0, a.__tqdm__.n, "Not reset")
        self.assertIsNone(a.__tqdm__.postfix, "Postfix initialized")
        a.set_postfix()
        self.assertIsNotNone(a.__tqdm__.postfix, "Postfix not set")
        self.assertEqual("", a.__tqdm__.postfix, "Postfix not set")
        self.assertFalse(a.__tqdm__.disable, "Disable")
        a.close()
        self.assertTrue(a.__tqdm__.disable, "Not disable")

    @patch("builtins.__import__", side_effect=import_mock_tqdm)
    def test_optional_tqdm_none(self, mock_import):
        a = OptionalTqdm()
        self.assertIsNone(a.__tqdm__, "Incorrect tqdm (not none)")
        # Assert not raise any error
        a.set_descriptor(desc="A descriptor")
        a.update()
        a.reset()
        a.set_postfix()
        a.close()
        a.set_postfix()


if __name__ == '__main__':
    unittest.main()
