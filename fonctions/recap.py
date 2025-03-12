# recap.py
import sys

ICONS = {
    "entree": "🥗",
    "plat principal": "🍛",
    "garniture": "🍚",
    "dessert": "🍰",
    "pain": "🍞",
    "autre": "➕",
}

welcome_message = (
    "\nWelcome to our restaurant, \n"
    "We will help you choose a dish from our menu \n"
    "depending on your allergens and preferences"
)

def print_recap(chosen_products):
    """
    Displays a summary of the order with corresponding icons and categories.

    Args:
        chosen_products (list): List of chosen products.
    """
    print("\nHere is a summary of your order:")
    for product in chosen_products:
        choice, chosen_dish, dishType = product
        icon = ICONS.get(dishType, "❓")
        print(f"{icon} {dishType.capitalize()}: {chosen_dish}")

    # Ask if the user wants to continue or exit
    while True:
        response = input("\nDo you want to continue or exit? (continue/exit): ").strip().lower()
        if response == "continue":
            return True
        elif response == "exit":
            print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")
            input("Press Enter to exit...")
            sys.exit()
        else:
            print("⚠️ Invalid response. Please enter 'continue' or 'exit'.")