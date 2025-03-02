# allergies.py
import pandas as pd
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent
MENU_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'menu.xlsx'

# Load Excel file
menu_data = pd.read_excel(MENU_FILE_PATH)

def ask_allergies():
    """
    Asks the user if they have any allergies and returns a list of allergens to avoid.

    Returns:
        list: List of allergens to avoid.
    """
    response = input(
        "Welcome to our restaurant!\n"
        "We will help you choose a dish from our menu based on your allergies and preferences.\n"
        "Do you have any allergies? (yes/no): "
    ).strip().lower()

    if response == "yes":
        return get_allergens()
    return []

def get_allergens():
    """
    Displays the list of available allergens and allows the user to select those to avoid.

    Returns:
        list: List of allergens selected by the user.
    """
    allergens = set()

    # Extract allergens from the menu data
    for allergen_list in menu_data['dish_allergen'].dropna():
        allergens.update(allergen.strip() for allergen in allergen_list.split(','))

    allergens = sorted(list(allergens))

    print("\nHere are the allergens present in our dishes:")
    for i, allergen in enumerate(allergens, 1):
        print(f"⚠️ {i}. {allergen}")

    while True:
        choice = input("\nPlease enter the numbers of the allergens you are allergic to (separated by commas): ").strip()

        try:
            # Parse user input
            num_allergens = [int(num.strip()) for num in choice.split(",") if num.strip().isdigit()]

            # Map numbers to allergens
            selected_allergens = [allergens[i - 1].lower() for i in num_allergens if 1 <= i <= len(allergens)]

            if selected_allergens:
                print("\nYou have indicated that you avoid:", ", ".join(selected_allergens))
                return selected_allergens
            else:
                print("\nInvalid selection. Please enter valid numbers from the list.")
        except ValueError:
            print("\nInvalid input. Please enter only numbers separated by commas.")

def filter_dishes_by_allergens(dishes, allergens):
    """
    Filters dishes based on allergens to avoid.

    Args:
        dishes (list): List of dishes to filter.
        allergens (list): List of allergens to avoid.

    Returns:
        list: List of filtered dishes.
    """
    filtered_dishes = []

    for dish in dishes:
        dish_allergens = menu_data[menu_data['dish_name'] == dish]['dish_allergen'].values[0]

        if pd.isna(dish_allergens):
            dish_allergens = ""

        dish_allergens = [allergen.strip().lower() for allergen in dish_allergens.split(',')]

        # Check if the dish contains any allergens to avoid
        if not any(allergen in dish_allergens for allergen in allergens):
            filtered_dishes.append(dish)

    return filtered_dishes