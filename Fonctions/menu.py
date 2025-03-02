# menu.py
import pandas as pd
from pathlib import Path
from recap import print_recap
from shared_data import chosen_products
from allergies import filter_dishes_by_allergens
from visualization import show_most_ordered_dishes_image

# Define absolute paths
BASE_DIR = Path(__file__).resolve().parent.parent
MENU_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'menu.xlsx'
DISHES_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'dishes.xlsx'

# Load Excel files
menu_data = pd.read_excel(MENU_FILE_PATH)
ingredients_data = pd.read_excel(DISHES_FILE_PATH)

def ask_meal(allergens):
    """
    Asks the user if they want a snack or a full meal.
    """
    while True:
        meal_type = input("\nDo you want a snack or a full meal? (snack/meal): ").strip().lower()

        if meal_type == "snack":
            propose_snack(allergens)
            # Offer a full meal after snacks
            propose_meal_after_snack = input("\nWould you also like a full meal? (yes/no): ").strip().lower()
            if propose_meal_after_snack == "yes":
                propose_menu(allergens)
            break
        elif meal_type == "meal":
            propose_menu(allergens)
            break
        else:
            print("\n⚠️ Invalid response. Please answer 'snack' or 'meal'.")

def propose_snack(allergens):
    """
    Proposes snacks to the user based on allergens.
    """
    # Display the image of the most ordered dishes
    show_most_ordered_dishes_image()

    dishType = "snack"
    while True:
        dishNames = menu_data[menu_data['meal_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print("\nHere are the snack options:")
        for i, dish in enumerate(dishNames, 1):
            print(f"🥪 {i}. {dish}")
        choice = input("\nChoose a product by entering its number, or type 'back' to return: ").strip().lower()
        if choice == "back":
            return ask_meal(allergens)
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                print(f"\n✅ You have chosen: {dishNames[choice - 1]}")
                chosen_products.append((choice, dishNames[choice - 1], dishType))

                another = input("Do you want to add another snack? (yes/no): ").strip().lower()
                if another != "yes":
                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")

def propose_menu(allergens):
    """
    Proposes a full meal to the user based on allergens.
    """
    if ask_yes_no("📌 1. Do you want a starter?"):
        propose_category("entree", allergens, "🥗 Here are the available starters:")
    if ask_yes_no("📌 2. Do you want a main course?"):
        propose_category("plat principal", allergens, "🍛 Here are the available main courses:")
    if ask_yes_no("📌 3. Do you want a side dish?"):
        propose_category("garniture", allergens, "🍚 Here are the available side dishes:")
    if ask_yes_no("📌 4. Do you want a dessert?"):
        propose_category("dessert", allergens, "🍰 Here are the available desserts:")
    if ask_yes_no("📌 5. Do you want bread?"):
        propose_category("pain", allergens, "🍞 Here are the available types of bread:")
    if ask_yes_no("📌 6. Do you want a supplement?"):
        propose_category("autre", allergens, "➕ Here are the available supplements:")

    print("\n✅ We have taken your order into account.")
    print_recap(chosen_products)

def ask_yes_no(question):
    """
    Asks a yes/no question.
    """
    response = input(f"{question} (yes/no): ").strip().lower()
    return response == "yes"

def propose_category(dishType, allergens, category_message):
    """
    Proposes dishes from a specific category and allows the user to add multiple items.
    """
    while True:
        dishNames = menu_data[menu_data['dish_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print(f"\n{category_message}")
        for i, dish in enumerate(dishNames, 1):
            print(f"{i}. {dish}")
        choice = input("\nChoose a product by entering its number, or type 'back' to return: ").strip().lower()
        if choice == "back":
            return

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                print(f"\n✅ You have chosen: {dishNames[choice - 1]}")
                chosen_products.append((choice, dishNames[choice - 1], dishType))

                another = input("Do you want to add another item from this category? (yes/no): ").strip().lower()
                if another != "yes":
                    return  # Exit after a valid choice
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")