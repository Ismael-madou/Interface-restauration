import unittest
from unittest.mock import patch
from validation import validate_snack, validate_product
from recap import chosen_products

class TestValidationFunctions(unittest.TestCase):

    def setUp(self):
        chosen_products.clear()

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