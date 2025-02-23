# test_validation.py
import unittest
from unittest.mock import patch
from validation import validate_product, validate_snack  # Assurez-vous d'importer correctement

class TestValidationFunctions(unittest.TestCase):

    @patch('builtins.input', return_value="Pizza")
    def test_validate_product(self, mock_input):
        chosen_products = []  # Initialiser chosen_products dans chaque test
        products = ["Pizza", "Burger"]
        validate_product(products, chosen_products)
        self.assertIn("Pizza", chosen_products)

    @patch('builtins.input', side_effect=["Sandwich", "no"])
    def test_validate_snack(self, mock_input):
        chosen_products = []  # Initialiser chosen_products dans chaque test
        products = ["Sandwich", "Chips"]
        validate_snack(products, chosen_products)
        self.assertIn("Sandwich", chosen_products)
