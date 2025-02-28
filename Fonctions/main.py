# main.py
from menu import ask_meal
from allergies import ask_allergies
from visualization import plot_most_ordered_dishes  # Import the visualization function

if __name__ == "__main__":
    """
    Entry point of the program. Asks the user about allergies and proposes a menu.
    After the user completes their order, it displays a chart of the most ordered dishes.
    """

    allergens = ask_allergies()

    ask_meal(allergens)

    plot_most_ordered_dishes()

    print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")

    input("Press Enter to exit...")