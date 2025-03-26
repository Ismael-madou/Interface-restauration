import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import pandas as pd

# Ajouter le bon chemin vers le module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.interface.allergies import ask_allergies, get_allergens, filter_dishes_by_allergens
from src.interface.shared_data import chosen_products


class TestAskAllergies(unittest.TestCase):

    @patch('builtins.input', return_value='no')
    def test_ask_allergies_no_input(self, mock_input):
        """Test si l'utilisateur n'a pas d'allergies."""
        result = ask_allergies()
        self.assertEqual(result, [])

    @patch('builtins.input', side_effect=['maybe', 'yes'])
    @patch('src.interface.allergies.get_allergens', return_value=['gluten'])
    def test_ask_allergies_invalid_then_yes(self, mock_get_allergens, mock_input):
        """Test avec une mauvaise réponse suivie d'une bonne."""
        result = ask_allergies()
        self.assertEqual(result, ['gluten'])
        mock_get_allergens.assert_called_once()


class TestGetAllergens(unittest.TestCase):

    @patch('builtins.input', return_value='1, 2')
    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_allergen': ['Gluten,Oeufs', 'Poisson,Lait']
    }))
    def test_get_allergens_multiple_selection(self, mock_input):
        """Test de sélection de plusieurs allergènes."""
        result = get_allergens()
        self.assertEqual(result, ['gluten', 'lait'])

    @patch('builtins.input', side_effect=['a,b', '3'])
    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_allergen': ['Gluten,Oeufs', 'Poisson,Lait', 'Fruits à coque']
    }))
    def test_get_allergens_invalid_then_valid(self, mock_input):
        """Test avec une entrée invalide suivie d'une valide."""
        result = get_allergens()
        self.assertEqual(result, ['lait'])  # ← correction ici


class TestFilterDishesByAllergens(unittest.TestCase):

    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_name': ['Dish1', 'Dish2'],
        'dish_allergen': ['Gluten,Oeufs', 'Poisson']
    }))
    def test_filter_with_matching_allergen(self):
        """Test que les plats avec allergène sont filtrés."""
        dishes = ['Dish1', 'Dish2']
        allergens = ['gluten']
        result = filter_dishes_by_allergens(dishes, allergens)
        self.assertEqual(result, ['Dish2'])

    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_name': ['Dish1', 'Dish2'],
        'dish_allergen': ['', '']
    }))
    def test_filter_with_no_allergens(self):
        """Test quand aucun plat n’a d’allergènes listés."""
        dishes = ['Dish1', 'Dish2']
        allergens = ['gluten']
        result = filter_dishes_by_allergens(dishes, allergens)
        self.assertEqual(result, ['Dish1', 'Dish2'])


if __name__ == '__main__':
    unittest.main()
