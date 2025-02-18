import unittest
from unittest.mock import patch
from menu import ask_meal, propose_snack, propose_menu, ask_yes_no
from validation import validate_snack, validate_product
from recap import chosen_products

class TestMenuFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_ask_yes_no_yes(self, mock_input):
        self.assertTrue(ask_yes_no("Do you want an entree?"))

    @patch('builtins.input', return_value='no')
    def test_ask_yes_no_no(self, mock_input):
        self.assertFalse(ask_yes_no("Do you want an entree?"))

    @patch('builtins.input', side_effect=["Sandwich", "no"])
    def test_validate_snack(self, mock_input):
        products = ["Sandwich", "Chips"]
        validate_snack(products)
        self.assertIn("Sandwich", chosen_products)

    @patch('builtins.input', return_value="Pizza")
    def test_validate_product(self, mock_input):
        products = ["Pizza", "Burger"]
        validate_product(products)
        self.assertIn("Pizza", chosen_products)

if __name__ == '__main__':
    unittest.main()