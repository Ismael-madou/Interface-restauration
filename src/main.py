# main.py
from menu import ask_meal, display_graph_image
from allergies import ask_allergies
from recap import welcome_message, print_recap  # Import the print_recap function
from visualization import display_graph_image  # Import the visualization function
from shared_data import chosen_products  # Import the shared list
from pathlib import Path
print(welcome_message)
if __name__ == "__main__":

    image_path = "docs/Dish_occurrences.png"  
    display_graph_image(image_path)
    """
    Entry point of the program. Asks the user for their allergies and suggests a menu.
After the user completes their order, displays a summary and a graph image.
    """
    while True:
        
        allergens = ask_allergies()
        ask_meal(allergens)


        recap_result = print_recap()
        if recap_result == "continue":
            continue

