import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

def display_graph_image(image_path: str) -> None:
    """
    Displays an image from a relative path to the project root, regardless of where the script is run from.
    """
    try:
        # Rebuild absolute path from project root
        base_dir = Path(__file__).resolve().parent.parent  # goes back to the root (outside src/)
        full_path = base_dir / image_path  # joins with the relative path

        img = mpimg.imread(full_path)
        plt.figure(figsize=(10, 6))
        plt.imshow(img)
        plt.axis('off')
        plt.title("Most Ordered Dishes")
        plt.tight_layout()
        plt.show(block=True)
    except FileNotFoundError:
        print(f"⚠️ Image not found: {full_path}")
