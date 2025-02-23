import unittest
from unittest.mock import patch
import sys
import os
# Ajouter le répertoire contenant 'menu.py' au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Fonctions')))
from menu import ask_meal


class TestMainFunctions(unittest.TestCase):

    @patch('menu.ask_meal')
    def test_main(self, mock_ask_meal):
        import main
        main.ask_meal()
        mock_ask_meal.assert_called_once()

if __name__ == '__main__':
    unittest.main()