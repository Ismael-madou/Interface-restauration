import unittest
from unittest.mock import patch

class TestMainFunctions(unittest.TestCase):

    @patch('menu.ask_meal')
    def test_main(self, mock_ask_meal):
        import main
        main.ask_meal()
        mock_ask_meal.assert_called_once()

if __name__ == '__main__':
    unittest.main()