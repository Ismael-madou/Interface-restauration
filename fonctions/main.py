# main.py
from menu import ask_meal
from allergies import ask_allergies
from recap import print_recap
from visualization import display_graph_image  # Import the visualization function

if __name__ == "__main__":
    """
    Entry point of the program. Asks the user about allergies and proposes a menu.
    After the user completes their order, it displays a summary and a graph image.
    """
    allergens = ask_allergies()

    while True:
        ask_meal(allergens)

        # Display the order summary
        if not print_recap(chosen_products):  # If the user chooses to exit
            break

        # Display the graph image
        graph_image_path = "most_ordered_dishes.png"  # Replace with the path to your graph image
        display_graph_image(graph_image_path)

    print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")
    input("Press Enter to exit...")