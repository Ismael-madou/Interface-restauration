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
    Affiche un récapitulatif de la commande avec les icônes et catégories correspondantes.

    Returns:
        Optional[str]: 'continue' si l'utilisateur veut continuer, None sinon.
    """
    from menu import chosen_products  # Importation de la liste partagée

    print("\nHere is a summary of your order:")
    for product in chosen_products:
        choice, chosen_dish, dishType = product
        icon = ICONS.get(dishType, "❓")
        print(f"{icon} {dishType.capitalize()}: {chosen_dish}")

    # Demander si l'utilisateur veut continuer ou quitter
    while True:
        response = input("\nDo you want to continue or exit? (continue/exit): ").strip().lower()
        if response == "continue":
            chosen_products.clear()  # Vider la liste pour la prochaine commande
            return "continue"
        elif response == "exit":
            print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")
            input("Press Enter to exit...")
            sys.exit()
        else:
            print("⚠️ Invalid response. Please enter 'continue' or 'exit'.")