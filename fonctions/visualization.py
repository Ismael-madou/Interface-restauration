import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def display_graph_image(image_path):
    """
    Displays a graph image in a graphical window.

    Args:
        image_path (str): The path to the graph image file to display.
    """
    try:
       
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"The image file '{image_path}' was not found.")

       
        img = mpimg.imread(image_path)


        plt.figure(figsize=(10, 6))  
        plt.imshow(img)
        plt.axis('off') 
        plt.title("Most Ordered Dishes")  
        plt.tight_layout() 

      
        plt.show(block=True)  

    except FileNotFoundError as e:
        print(f"⚠️ Error: {e}")
    except Exception as e:
        print(f"⚠️ An error occurred while displaying the image: {e}")


if __name__ == "__main__":
    image_path = "docs/Dish_occurrences.png"  
    display_graph_image(image_path)