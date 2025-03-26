import sys
from pathlib import Path
import unittest
from unittest.mock import patch

# Chemin d'accès au code source
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.interface.validation import validate_snack, validate_product
from src.interface.shared_data import chosen_products


class TestValidateSnack(unittest.TestCase):

    def setUp(self):
        """Réinitialise les produits choisis avant chaque test."""
        chosen_products.clear()

    @patch('builtins.input', side_effect=["Chips", "no"])
    @patch('src.interface.validation.print_recap')
    def test_validate_snack_single_product(self, mock_recap, mock_input):
        """Ajout d'un seul snack et arrêt après."""
        products = ["Chips", "Barres", "Fruit"]
        validate_snack(products)
        self.assertIn("Chips", chosen_products)
        self.assertEqual(len(chosen_products), 1)

    @patch('builtins.input', side_effect=["Chips", "yes", "Barres", "no"])
    @patch('src.interface.validation.print_recap')
    def test_validate_snack_multiple_products(self, mock_recap, mock_input):
        """Ajout de deux snacks successifs."""
        products = ["Chips", "Barres", "Fruit"]
        validate_snack(products)
        self.assertIn("Chips", chosen_products)
        self.assertIn("Barres", chosen_products)
        self.assertEqual(len(chosen_products), 2)


class TestValidateProduct(unittest.TestCase):

    def setUp(self):
        """Réinitialise les produits choisis avant chaque test."""
        chosen_products.clear()

    @patch('builtins.input', return_value="Pizza")
    def test_validate_product_addition(self, mock_input):
        """Test d'ajout simple d'un produit."""
        products = ["Pizza", "Burger"]
        validate_product(products)
        self.assertIn("Pizza", chosen_products)
        self.assertEqual(len(chosen_products), 1)

    @patch('builtins.input', return_value="Nuggets")
    def test_validate_product_not_in_list(self, mock_input):
        """Saisie d'un produit qui n'est pas dans la liste (comportement autorisé ici)."""
        products = ["Pizza", "Burger"]
        validate_product(products)
        self.assertIn("Nuggets", chosen_products)  # On accepte tous les choix libres
        self.assertEqual(len(chosen_products), 1)


if __name__ == '__main__':
    unittest.main()
