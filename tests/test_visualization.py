import sys
from pathlib import Path
import unittest
from unittest.mock import patch

# Ajoute dynamiquement la racine du projet au chemin
root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

from src.interface.visualization import display_graph_image


class TestVisualizationFunction(unittest.TestCase):

    @patch("builtins.print")
    def test_display_graph_image_file_not_found(self, mock_print):
        """
        Test que la fonction affiche une erreur si l'image est introuvable.
        """
        fake_path = "docs/non_existing_image.png"
        display_graph_image(fake_path)

        expected_message = f"⚠️ Image not found: {root_path / fake_path}"
        mock_print.assert_any_call(expected_message)


if __name__ == '__main__':
    unittest.main()
