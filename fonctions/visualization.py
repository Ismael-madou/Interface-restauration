# visualization.py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display_graph_image(graph_image_path):
    """
    Displays a graph image in a graphical window.

    Args:
        image_path (str): The path to the graph image file to display.
    """
    try:
        # Load the image
        img = mpimg.imread(graph_image_path)

        # Display the image
        plt.figure(figsize=(10, 6))
        plt.imshow(img)
        plt.axis('off')  # Hide the axes
        plt.title("Most Ordered Dishes")
        plt.tight_layout()

        # Show the graphical window
        plt.show(block=True)
    except FileNotFoundError:
        print(f"⚠️ Error: The image file '{graph_image_path}' was not found.")
    except Exception as e:
        print(f"⚠️ An error occurred while displaying the image: {e}")