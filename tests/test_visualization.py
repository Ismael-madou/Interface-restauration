import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest
from unittest.mock import patch
from src.interface.visualization import display_graph_image

class TestVisualizationFunctions(unittest.TestCase):

    @patch("builtins.print")
    def test_display_graph_image_file_not_found(self, mock_print):
        # Fichier imaginaire pour forcer l'erreur
        fake_path = Path("docs/non_existing_image.png")
        display_graph_image(fake_path)
        mock_print.assert_any_call(f"⚠️ Image not found: {Path(__file__).resolve().parent.parent / fake_path}")
