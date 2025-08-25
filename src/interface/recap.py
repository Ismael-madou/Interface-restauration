import sys
from typing import Optional

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

def print_recap() -> Optional[str]:
    """
    Displays a summary of the order with corresponding icons and categories.

    Returns:
        Optional[str]: 'continue' if the user wants to continue, None otherwise.
    """
    from src.interface.menu import chosen_products

    print("\nHere is a summary of your order:")
    for product in chosen_products:
        # Gère les deux formats de tuple (snack: 3 éléments, menu: 5 éléments)
        if len(product) == 3:
            choice, chosen_dish, dishType = product
            icon = ICONS.get(dishType, "❓")
            print(f"{icon} {dishType.capitalize()}: {chosen_dish}")
        elif len(product) == 5:
            choice, chosen_dish, dishType, included_ingredients, removed_ingredients = product
            icon = ICONS.get(dishType, "❓")
            print(f"{icon} {dishType.capitalize()}: {chosen_dish}")
            if included_ingredients:
                print(f"   ✔️ Ingredients: {', '.join(included_ingredients)}")
            if removed_ingredients:
                print(f"   ❌ Removed: {', '.join(removed_ingredients)}")
        else:
            print(f"❓ Unknown product format: {product}")


    while True:
        response = input("\nDo you want to continue or exit? (continue/exit): ").strip().lower()
        if response == "continue":
            chosen_products.clear()
            return "continue"
        elif response == "exit":
            print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")
            input("Press Enter to exit...")
            sys.exit()
        else:
            print("⚠️ Invalid response. Please enter 'continue' or 'exit'.")