import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest
from unittest.mock import patch, MagicMock
from src.interface.menu import ask_yes_no, ask_yes_no_stop, display_graph_image, propose_category, stop
from src.interface.shared_data import chosen_products

class TestMenuFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_ask_yes_no_yes(self, mock_input):
        self.assertTrue(ask_yes_no("Do you want something?"))

    @patch('builtins.input', return_value='no')
    def test_ask_yes_no_no(self, mock_input):
        self.assertFalse(ask_yes_no("Do you want something?"))

    @patch('builtins.input', return_value='stop')
    def test_ask_yes_no_stop(self, mock_input):
        result = ask_yes_no_stop("Do you want to continue?")
        self.assertEqual(result, 'stop')

    @patch('os.path.exists', return_value=False)
    @patch('builtins.print')
    def test_display_graph_image_file_not_found(self, mock_print, mock_exists):
        display_graph_image("fake/path/image.png")
        mock_print.assert_any_call("\u26a0️ Error: The image file 'fake/path/image.png' was not found.")

    @patch('src.interface.menu.menu_data', new=MagicMock())
    @patch('src.interface.menu.ingredients_data', new=MagicMock())
    @patch('src.interface.menu.filter_dishes_by_allergens', return_value=['Dish1', 'Dish2'])
    def test_propose_category_simple(self, mock_filter):
        from src.interface.menu import propose_category
        chosen_products.clear()

        # Simuler les entrées utilisateur pour sélectionner le 1er plat et répondre "no" ensuite
        with patch('builtins.input', side_effect=['1', 'no', 'no']):
            propose_category("plat principal", [], "Test category")

        self.assertTrue(len(chosen_products) >= 1)

    @patch('builtins.input', side_effect=['yes', 'no'])  # Simule : save = yes, exit
    @patch('src.interface.menu.display_chosen_products_nutrients')
    @patch('builtins.print')
    @patch('builtins.input', return_value='')  # Pour "Press Enter to exit..."
    def test_stop_saves_order(self, mock_enter, mock_print, mock_nutrients, mock_input_save):
        from src.interface.menu import stop
        chosen_products.clear()
        chosen_products.append((1, 'Pizza', 'meal', ['cheese'], ['gluten']))
        with self.assertRaises(SystemExit):  # car stop appelle sys.exit()
            stop()

if __name__ == '__main__':
    unittest.main()

