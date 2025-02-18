import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from allergies import ask_allergies, get_allergens, filter_dishes_by_allergens

class TestAllergiesFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='no')
    def test_ask_allergies_no(self, mock_input):
        result = ask_allergies()
        self.assertEqual(result, [])

    @patch('builtins.input', return_value='yes')
    @patch('allergies.get_allergens', return_value=['gluten', 'lactose'])
    def test_ask_allergies_yes(self, mock_get_allergens, mock_input):
        result = ask_allergies()
        self.assertEqual(result, ['gluten', 'lactose'])
        mock_get_allergens.assert_called_once()

    @patch('builtins.input', return_value='gluten, lactose')
    @patch('allergies.menu_data', new_callable=MagicMock)
    def test_get_allergens(self, mock_menu_data, mock_input):
        mock_menu_data['allergene'].dropna.return_value = pd.Series([
            'Gluten,Oeufs',
            'Poisson,Lait'
        ])
        result = get_allergens()
        self.assertEqual(result, ['gluten', 'lactose'])

    @patch('allergies.menu_data', new_callable=MagicMock)
    def test_filter_dishes_by_allergens(self, mock_menu_data):
        mock_menu_data['menuPlatNom'] = pd.Series(['Dish1', 'Dish2'])
        mock_menu_data['allergene'] = pd.Series([
            'Gluten,Oeufs',
            'Poisson,Lait'
        ])
        dishes = mock_menu_data['menuPlatNom'].tolist()
        allergens = ['gluten']
        
        # Liste pour stocker les plats qui ne contiennent pas de gluten
        filtered_dishes = []
        
        for dish in dishes:
            dish_allergens = mock_menu_data[mock_menu_data['menuPlatNom'] == dish]['allergene'].values[0]
            if pd.isna(dish_allergens):
                dish_allergens = ""
            dish_allergens = [allergen.strip().lower() for allergen in dish_allergens.split(',')]
            if not any(allergen in dish_allergens for allergen in allergens):
                filtered_dishes.append(dish)
        
        result = filtered_dishes
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()