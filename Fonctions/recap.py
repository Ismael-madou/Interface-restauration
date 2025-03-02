# recap.py
ICONS = {
    "entree": "🥗",
    "plat principal": "🍛",
    "garniture": "🍚",
    "dessert": "🍰",
    "pain": "🍞",
    "autre": "➕",
}

def print_recap(chosen_products):
    """
    Displays a summary of the order with corresponding icons.

    Args:
        chosen_products (list): List of chosen products.
    """
    print("\nHere is a summary of your order:")
    for product in chosen_products:
        choice, chosen_dish, dishType = product
        icon = ICONS.get(dishType, "❓")
        print(f"{icon} {choice}. {chosen_dish}")