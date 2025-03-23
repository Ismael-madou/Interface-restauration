import pandas as pd
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MENU_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'menu.xlsx'

# Charger les fichiers Excel
menu_data = pd.read_excel(MENU_FILE_PATH)

def ask_allergies() -> List[str]:
    """
    Asks the user if they have any allergies and returns a list of allergens to avoid.

    Returns:
        List[str]: List of allergens to avoid.
    """
    while True:
        response = input("\nDo you have any allergies? (yes/no): ").strip().lower()
        if response == "yes":
            return get_allergens()
        elif response == "no":
            return []
        else:
            print("⚠️ Invalid response. Please enter 'yes' or 'no'.")

def get_allergens() -> List[str]:
    """
    Displays the list of available allergens and allows the user to select those to avoid.

    Returns:
        List[str]: List of allergens selected by the user.
    """
    allergens = set()

    for allergen_list in menu_data['dish_allergen'].dropna():
        allergens.update(allergen.strip() for allergen in allergen_list.split(','))

    allergens = sorted(list(allergens))

    print("\nHere are the allergens present in our dishes:")
    for i, allergen in enumerate(allergens, 1):
        print(f"⚠️ {i}. {allergen}")

    while True:
        choix = input("\nPlease enter the numbers of the allergens you are allergic to (separated by commas): ").strip()

        try:
            num_allergens = [int(num.strip()) for num in choix.split(",") if num.strip().isdigit()]

            selected_allergens = [allergens[i - 1].lower() for i in num_allergens if 1 <= i <= len(allergens)]

            if selected_allergens:
                print("\nYou have indicated that you avoid:", ", ".join(selected_allergens))
                return selected_allergens
            else:
                print("\nInvalid selection. Please enter valid numbers from the list.")

        except ValueError:
            print("\nInvalid input. Please enter only numbers separated by commas.")

def filter_dishes_by_allergens(dishes: List[str], allergens: List[str]) -> List[str]:
    """
    Filters dishes based on allergens to avoid.

    Args:
        dishes (List[str]): List of dishes to filter.
        allergens (List[str]): List of allergens to avoid.

    Returns:
        List[str]: List of filtered dishes.
    """
    filtered_dishes = []

    for dish in dishes:
        dish_data = menu_data[menu_data['dish_name'] == dish]

        # Vérifier si le plat existe bien dans la base
        if dish_data.empty:
            continue  # Passer au suivant

        dish_allergens = dish_data['dish_allergen'].values[0] if 'dish_allergen' in dish_data.columns else ""

        if pd.isna(dish_allergens) or dish_allergens == "":
            dish_allergens = ""

        dish_allergens = [allergen.strip().lower() for allergen in dish_allergens.split(',')]

        if not any(allergen in dish_allergens for allergen in allergens):
            filtered_dishes.append(dish)

    return filtered_dishes
