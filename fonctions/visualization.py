import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

def display_graph_image(image_path: Path) -> None:
    """
    Affiche une image de graphique dans une fenêtre graphique.

    Args:
        image_path (Path): Chemin vers l'image du graphique à afficher.
    """
    try:
        # Charger l'image
        img = mpimg.imread(image_path)

        # Afficher l'image
        plt.figure(figsize=(10, 6))
        plt.imshow(img)
        plt.axis('off')  # Masquer les axes
        plt.title("Most Ordered Dishes")
        plt.tight_layout()

        # Afficher la fenêtre graphique
        plt.show(block=True)
    except FileNotFoundError:
        print(f"⚠️ Error: The image file '{image_path}' was not found.")
    except Exception as e:
        print(f"⚠️ An error occurred while displaying the image: {e}")