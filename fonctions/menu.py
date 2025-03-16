import sys
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional
from allergies import filter_dishes_by_allergens, ask_allergies
from recap import print_recap, ICONS

# Chemins absolus
BASE_DIR = Path(__file__).resolve().parent.parent
MENU_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'menu.xlsx'
DISHES_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'dishes.xlsx'

# Charger les fichiers Excel
menu_data = pd.read_excel(MENU_FILE_PATH)
ingredients_data = pd.read_excel(DISHES_FILE_PATH)

# Liste partagée pour stocker les produits choisis
chosen_products: List[Tuple[int, str, str]] = []


def ask_meal(allergens: List[str]) -> None:
    """
    Demande à l'utilisateur s'il veut un snack ou un repas complet.

    Args:
        allergens (List[str]): Liste des allergènes à éviter.
    """
    while True:
        meal_type = input("Do you want a snack or a meal? (snack/meal/stop): ").strip().lower()

        if meal_type == "snack":
            propose_snack(allergens)
        elif meal_type == "meal":
            propose_menu(allergens)
        elif meal_type == "stop":
            stop()
        else:
            print("\n⚠️ Invalid response. Please answer 'snack', 'meal', or 'stop'.")


def propose_snack(allergens: List[str]) -> None:
    """
    Propose des snacks à l'utilisateur en fonction des allergènes.

    Args:
        allergens (List[str]): Liste des allergènes à éviter.
    """
    dishType = "snack"

    while True:
        dishNames = menu_data[menu_data['meal_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print("\nHere are the options for a snack:")
        for i, dish in enumerate(dishNames, 1):
            print(f"🥪 {i}. {dish}")
        choice = input(
            "\nChoose a product by entering its number, or type 'back' to choose again (snack/meal/stop): ").strip().lower()
        if choice == "back":
            return ask_meal(allergens)
        elif choice == "stop":
            stop()
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                chosen_dish = dishNames[choice - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")

                # Demander si l'utilisateur veut voir les ingrédients
                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product?")
                if see_ingredients:
                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))

                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for i, ingredient in enumerate(ingredients, 1):
                            print(f"{i}. {ingredient}")
                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Demander si l'utilisateur veut valider le choix
                    validate_choice = ask_yes_no("Do you want to validate this choice?")
                    if validate_choice:
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = ask_yes_no("Do you want to add another snack?")
                if not another:
                    print("\n✅ We have taken your order into account.")
                    print_recap()
                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number, 'back', or 'stop'.")


def propose_menu(allergens: List[str]) -> None:
    """
    Propose un menu complet à l'utilisateur en fonction des allergènes.

    Args:
        allergens (List[str]): Liste des allergènes à éviter.
    """
    if ask_yes_no_stop("📌 1. Do you want a starter?") == "yes":
        propose_category("entree", allergens, "🥗 Here are the available starters:")
    if ask_yes_no_stop("📌 2. Do you want a dish?") == "yes":
        propose_category("plat principal", allergens, "🍛 Here are the available main courses:")
    if ask_yes_no_stop("📌 3. Do you want a side dish?") == "yes":
        propose_category("garniture", allergens, "🍚 Here are the available side dishes:")
    if ask_yes_no_stop("📌 4. Do you want a dessert?") == "yes":
        propose_category("dessert", allergens, "🍰 Here are the available desserts:")
    if ask_yes_no_stop("📌 5. Do you want bread?") == "yes":
        propose_category("pain", allergens, "🍞 Here are the available types of bread:")
    if ask_yes_no_stop("📌 6. Do you want a supplement?") == "yes":
        propose_category("autre", allergens, "➕ Here are the available supplements:")

    print("\n✅ We have taken your order into account.")
    print_recap()


def ask_yes_no(question: str) -> bool:
    """
    Pose une question oui/non à l'utilisateur.

    Args:
        question (str): La question à poser.

    Returns:
        bool: True si la réponse est 'yes', False sinon.
    """
    while True:
        response = input(f"{question} (yes/no): ").strip().lower()
        if response in ["yes", "no"]:
            return response == "yes"
        print("⚠️ Invalid response. Please enter 'yes' or 'no'.")


def ask_yes_no_stop(question: str) -> str:
    """
    Pose une question oui/non/stop à l'utilisateur.

    Args:
        question (str): La question à poser.

    Returns:
        str: 'yes', 'no', ou 'stop' en fonction de la réponse de l'utilisateur.
    """
    while True:
        response = input(f"{question} (yes/no/stop): ").strip().lower()
        if response in ["yes", "no", "stop"]:
            return response
        print("⚠️ Invalid response. Please enter 'yes', 'no', or 'stop'.")


def stop() -> None:
    """
    Arrête le programme après avoir demandé à l'utilisateur s'il veut sauvegarder sa commande.
    """
    save_or_no = input("Do you want to save your order? (yes/no): ").strip().lower()
    if save_or_no == "yes":
        print("\nHere is a summary of your order:")
        for product in chosen_products:
            choice, chosen_dish, dishType = product
            icon = ICONS.get(dishType, "❓")
            print(f"{icon} {dishType.capitalize()}: {chosen_dish}")

        print("\nThank you for choosing our restaurant! We hope you enjoy your meal. 😊")
        input("Press Enter to exit...")
        sys.exit()
    elif save_or_no == "no":
        print("\nThank you for choosing our restaurant! Do not hesitate to reorder. 😊")
        input("Press Enter to exit...")
        sys.exit()
    else:
        print("⚠️ Invalid response. Please enter 'yes' or 'no'.")


def propose_category(dishType: str, allergens: List[str], category_message: str) -> None:
    """
    Propose des plats d'une catégorie spécifique et permet à l'utilisateur d'ajouter plusieurs articles.

    Args:
        dishType (str): Type de plat (ex: "entree", "plat principal").
        allergens (List[str]): Liste des allergènes à éviter.
        category_message (str): Message à afficher pour la catégorie.
    """
    while True:
        dishNames = menu_data[menu_data['dish_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print(f"\n{category_message}")
        for i, dish in enumerate(dishNames, 1):
            print(f"{i}. {dish}")
        choice = input(
            "\nChoose a product by entering its number, or type 'back' to return, or 'stop' to exit: ").strip().lower()
        if choice == "back":
            return
        elif choice == "stop":
            stop()
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                chosen_dish = dishNames[choice - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")

                # Demander si l'utilisateur veut voir les ingrédients
                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product?")
                if see_ingredients:
                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))

                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for i, ingredient in enumerate(ingredients, 1):
                            print(f"{i}. {ingredient}")
                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Demander si l'utilisateur veut valider le choix
                    validate_choice = ask_yes_no("Do you want to validate this choice?")
                    if validate_choice:
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = ask_yes_no("Do you want to add another product from this category?")
                if not another:
                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number, 'back', or 'stop'.")