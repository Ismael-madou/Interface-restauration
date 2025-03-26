#Pour lancer ce code il faut le lancer depuis un terminal et dans le dossier 'management_projet_digitaux' (la ou à été cloner le projet) :
# python -m tests.test_main

import unittest
from unittest.mock import patch
from src.interface import recap


class TestMain(unittest.TestCase):
    @patch("builtins.print")
    def test_welcome_message_is_defined_and_printable(self, mock_print):
        """
        Vérifie que le message d'accueil existe bien et peut être affiché.
        C’est un test indirect de ce que main.py affiche au lancement.
        """
        message = recap.welcome_message
        print(message)  # Simule ce que fait main.py

        mock_print.assert_any_call(message)


if __name__ == '__main__':
    unittest.main()
