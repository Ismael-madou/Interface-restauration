import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest
from unittest.mock import patch
import pandas as pd
from src.interface.allergies import ask_allergies, get_allergens, filter_dishes_by_allergens

class TestAllergiesFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='no')
    def test_ask_allergies_no(self, mock_input):
        result = ask_allergies()
        self.assertEqual(result, [])

    @patch('builtins.input', return_value='yes')
    @patch('src.interface.allergies.get_allergens', return_value=['gluten', 'lactose'])
    def test_ask_allergies_yes(self, mock_get_allergens, mock_input):
        result = ask_allergies()
        self.assertEqual(result, ['gluten', 'lactose'])
        mock_get_allergens.assert_called_once()

    @patch('builtins.input', return_value='1, 2')
    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_allergen': ['Gluten,Oeufs', 'Poisson,Lait']
    }))
    def test_get_allergens(self, mock_input):
        result = get_allergens()
        self.assertEqual(result, ['gluten', 'lait'])  # car 1 = gluten, 2 = lait

    @patch('src.interface.allergies.menu_data', new=pd.DataFrame({
        'dish_name': ['Dish1', 'Dish2'],
        'dish_allergen': ['Gluten,Oeufs', 'Poisson,Lait']
    }))
    def test_filter_dishes_by_allergens(self):
        dishes = ['Dish1', 'Dish2']
        allergens = ['gluten']
        result = filter_dishes_by_allergens(dishes, allergens)
        self.assertEqual(result, ['Dish2'])  # Dish2 ne contient pas gluten

if __name__ == '__main__':
    unittest.main()
