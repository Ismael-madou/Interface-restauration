import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest
from unittest.mock import patch
from src.interface.validation import validate_snack, validate_product
from src.interface.shared_data import chosen_products

class TestValidationFunctions(unittest.TestCase):

    def setUp(self):
        chosen_products.clear()

    @patch('src.interface.recap.print_recap', autospec=True)
    @patch('builtins.input', side_effect=["Sandwich", "no"])
    def test_validate_snack(self, mock_input, mock_print_recap):
        products = ["Sandwich", "Chips"]
        with patch('src.interface.validation.print_recap'):
            validate_snack(products)
        self.assertIn("Sandwich", chosen_products)

    @patch('builtins.input', return_value="Pizza")
    def test_validate_product(self, mock_input):
        products = ["Pizza", "Burger"]
        validate_product(products)
        self.assertIn("Pizza", chosen_products)

if __name__ == '__main__':
    unittest.main()
