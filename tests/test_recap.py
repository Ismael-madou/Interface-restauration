import unittest
from unittest.mock import patch
from src.interface.menu import chosen_products
import sys

# Import the module you want to test
from src.interface.recap import print_recap

class TestRecapFunctions(unittest.TestCase):

    def setUp(self):
        chosen_products.clear()

    @patch('builtins.input', return_value='continue')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_print_recap(self, mock_exit, mock_print, mock_input):
        # Adapter à l'ancien format attendu : (dish_code, dish_name, dish_type)
        chosen_products.extend([
            (1, "Pizza", "plat principal"),
            (2, "Burger", "plat principal")
        ])

        print_recap()

        # Vérifier que le résumé a bien été imprimé avec les bons plats
        mock_print.assert_any_call("\nHere is a summary of your order:")
        mock_print.assert_any_call("🍛 Plat principal: Pizza")
        mock_print.assert_any_call("🍛 Plat principal: Burger")
        
        # Vérifier que sys.exit() n'a PAS été appelé
        mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()