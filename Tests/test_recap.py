 import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Fonctions')))
from recap import print_recap, chosen_products

class TestRecapFunctions(unittest.TestCase):

    def setUp(self):
        chosen_products.clear()

    @patch('builtins.print')
    def test_print_recap(self, mock_print):
        chosen_products.extend(["Pizza", "Burger"])
        print_recap()
        mock_print.assert_any_call("Here is a summary of your order:")
        mock_print.assert_any_call("- Pizza")
        mock_print.assert_any_call("- Burger")

if __name__ == '__main__':
    unittest.main()