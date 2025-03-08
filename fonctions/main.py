# main.py
from menu import ask_meal
from allergies import ask_allergies
from recap import welcome_message, print_recap  # Import the print_recap function
from visualization import display_graph_image  # Import the visualization function
from shared_data import chosen_products  # Import the shared list

print(welcome_message)

if __name__ == "__main__":
    """
    Entry point of the program. Asks the user about allergies and proposes a menu.
    After the user completes their order, it displays a summary and a graph image.
    """
    while True:
        allergens = ask_allergies()
        ask_meal(allergens)

        # Display the order summary
        recap_result = print_recap(chosen_products)  # Get the result from print_recap
        if recap_result == "continue":
            chosen_products.clear()  # Clear the chosen products list for the next order
            continue  # Restart the process

        # Display the graph image
        graph_image_path = "most_ordered_dishes.png"
        display_graph_image(graph_image_path)