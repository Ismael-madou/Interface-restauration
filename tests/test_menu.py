import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import os

# Accès aux modules
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.interface.menu import ask_yes_no, ask_yes_no_stop, display_graph_image, propose_category, stop
from src.interface.shared_data import chosen_products


class TestAskYesNo(unittest.TestCase):

    @patch('builtins.input', return_value='yes')
    def test_ask_yes_no_yes(self, mock_input):
        """Test réponse 'yes'."""
        self.assertTrue(ask_yes_no("Do you want something?"))

    @patch('builtins.input', return_value='no')
    def test_ask_yes_no_no(self, mock_input):
        """Test réponse 'no'."""
        self.assertFalse(ask_yes_no("Do you want something?"))


class TestAskYesNoStop(unittest.TestCase):

    @patch('builtins.input', return_value='stop')
    def test_ask_yes_no_stop_stop(self, mock_input):
        """Test réponse 'stop'."""
        self.assertEqual(ask_yes_no_stop("Do you want to continue?"), 'stop')


class TestDisplayGraphImage(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    @patch('builtins.print')
    def test_display_graph_image_file_not_found(self, mock_print, mock_exists):
        """Test si le fichier image est introuvable."""
        display_graph_image("fake/path/image.png")
        mock_print.assert_any_call("⚠️ Error: The image file 'fake/path/image.png' was not found.")


class TestProposeCategory(unittest.TestCase):

    @patch('src.interface.menu.menu_data', new=MagicMock())
    @patch('src.interface.menu.ingredients_data', new=MagicMock())
    @patch('src.interface.menu.filter_dishes_by_allergens', return_value=['Dish1'])
    def test_propose_category_simple(self, mock_filter):
        """Ajout d’un produit simple depuis une catégorie."""
        from src.interface.menu import propose_category
        chosen_products.clear()

        # Simule le choix de "Dish1", sans suppression d’ingrédients, validation directe
        with patch('builtins.input', side_effect=['1', 'no', 'no']):
            propose_category("plat principal", [], "Liste des plats")
        self.assertEqual(len(chosen_products), 1)


class TestStopFunction(unittest.TestCase):

    def setUp(self):
        chosen_products.clear()
        chosen_products.append((1, 'Pizza', 'meal', ['cheese'], ['gluten']))

    @patch('builtins.input', side_effect=['yes', ''])  # "save = yes", "press enter"
    @patch('src.interface.menu.display_chosen_products_nutrients')
    @patch('builtins.print')
    def test_stop_saves_order(self, mock_print, mock_nutrients, mock_input):
        """Test si l’utilisateur sauvegarde son menu et quitte."""
        with self.assertRaises(SystemExit):
            stop()

    @patch('builtins.input', side_effect=['no', ''])  # "save = no", "press enter"
    @patch('builtins.print')
    def test_stop_no_save(self, mock_print, mock_input):
        """Test si l’utilisateur quitte sans sauvegarder."""
        with self.assertRaises(SystemExit):
            stop()


if __name__ == '__main__':
    unittest.main()
