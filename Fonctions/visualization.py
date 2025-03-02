# visualization.py
import os

def show_most_ordered_dishes_image():
    """
    Displays an image of the most ordered dishes before the user makes their selection.
    """
    image_path = "path/to/your/image.png"  # Replace with the path to your image
    if os.path.exists(image_path):
        print(f"\nHere are the most ordered dishes: {image_path}")
    else:
        print(f"\n⚠️ The image '{image_path}' was not found.")