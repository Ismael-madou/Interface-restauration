#Pour lancer ce code il faut le lancer depuis un terminal et dans le dossier 'management_projet_digitaux' (la ou à été cloner le projet) :
# python -m tests.test_recap

import unittest
from unittest.mock import patch
import sys

# Accès aux modules
from src.interface.menu import chosen_products
from src.interface.recap import print_recap


class TestPrintRecap(unittest.TestCase):

    def setUp(self):
        """Prépare une commande fictive avant chaque test."""
        chosen_products.clear()
        chosen_products.extend([
            (1, "Pizza", "plat principal"),
            (2, "Compote", "dessert")
        ])

    @patch('builtins.input', return_value='continue')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_print_recap_continue(self, mock_exit, mock_print, mock_input):
        """L'utilisateur veut continuer, la liste est vidée."""
        result = print_recap()
        self.assertEqual(result, "continue")
        self.assertEqual(len(chosen_products), 0)
        mock_exit.assert_not_called()

    @patch('builtins.input', return_value='exit')
    @patch('builtins.print')
    def test_print_recap_exit(self, mock_print, mock_input):
        """L'utilisateur veut quitter, le programme doit se terminer."""
        with self.assertRaises(SystemExit):
            print_recap()

    @patch('builtins.input', side_effect=['blah', 'continue'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_print_recap_invalid_then_continue(self, mock_exit, mock_print, mock_input):
        """L'utilisateur tape une mauvaise entrée, puis 'continue'."""
        result = print_recap()
        self.assertEqual(result, "continue")
        self.assertEqual(len(chosen_products), 0)
        self.assertIn(
            unittest.mock.call("⚠️ Invalid response. Please enter 'continue' or 'exit'."),
            mock_print.call_args_list
        )


if __name__ == '__main__':
    unittest.main()
