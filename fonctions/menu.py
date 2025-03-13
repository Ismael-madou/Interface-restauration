# menu.py
import sys
import pandas as pd
from pathlib import Path
from validation import validate_snack, validate_product
<<<<<<< HEAD
from recap import print_recap
from shared_data import chosen_products  # Import the shared list
from allergies import filter_dishes_by_allergens

=======
from recap import print_recap, ICONS
from shared_data import chosen_products
from allergies import filter_dishes_by_allergens, ask_allergies


# Define absolute paths
BASE_DIR = Path(__file__).resolve().parent.parent
MENU_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'menu.xlsx'
DISHES_FILE_PATH = BASE_DIR / 'data' / 'processed' / 'dishes.xlsx'
>>>>>>> 6e699fb9bf9e0b398ee650cbae9afee42031c237

# Load Excel files
menu_data = pd.read_excel('data/processed/menu.xlsx')
ingredients_data = pd.read_excel('data/processed/dishes.xlsx')

def ask_meal(allergens):
    """
    Asks the user if they want a snack or a full meal.

    Args:
        allergens (list): List of allergens to avoid.
    """
    while True:
        meal_type = input("Do you want a snack or a meal? (snack/meal): ").strip().lower()

        if meal_type == "snack":
            propose_snack(allergens)
        elif meal_type == "meal":
            propose_menu(allergens)
        else:
            print("\n⚠️ Invalid response. Please answer 'snack' or 'meal'.")

def propose_snack(allergens):
    """
    Proposes snacks to the user based on allergens.

    Args:
        allergens (list): List of allergens to avoid.
    """
    dishType = "snack"

    while True:
        dishNames = menu_data[menu_data['meal_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print("\nHere are the options for a snack:")
        for i, dish in enumerate(dishNames, 1):
            print(f"🥪 {i}. {dish}")
        choice = input(
            "\nChoose a product by entering its number, or type 'back' to choose again (snack/meal): ").strip().lower()
        if choice == "back":
            return ask_meal(allergens)
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                chosen_dish = dishNames[choice - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")

                # Ask if the user wants to see the ingredients
<<<<<<< HEAD
                see_ingredients = input("Do you want to see the ingredients of this product ? (yes/no): ").strip().lower()
                if see_ingredients == "yes":
                    ingredients = sorted(set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))
        
=======
                see_ingredients = input(
                    "Do you want to see the ingredients of this product? (yes/no): ").strip().lower()
                if see_ingredients == "yes":
                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))

>>>>>>> 3e6fda04ba4781d82fb0945782c449afabd29f75
                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for j, ingredient in enumerate(ingredients, 1):  # Numéroter les ingrédients
                            print(f"{j}. {ingredient}")

                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Ask if the user wants to validate the choice
                    validate_choice = input("Do you want to validate this choice? (yes/no): ").strip().lower()
                    if validate_choice == "yes":
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = input("Do you want to add another snack? (yes/no): ").strip().lower()
                if another != "yes":
                    print("\n✅ We have taken your order into account.")
                    print_recap(chosen_products)  # Pass the chosen_products list to print_recap
                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")

<<<<<<< HEAD

<<<<<<< HEAD
=======

>>>>>>> 3e6fda04ba4781d82fb0945782c449afabd29f75
=======
>>>>>>> 6e699fb9bf9e0b398ee650cbae9afee42031c237
def propose_menu(allergens):
    """
    Proposes a full menu to the user based on allergens.

    Args:
        allergens (list): List of allergens to avoid.
    """
    if ask_yes_no("📌 1. Do you want a starter?"):
        propose_category("entree", allergens, "🥗 Here are the available starters:")
    if ask_yes_no("📌 2. Do you want a dish?"):
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
    result = print_recap(chosen_products)  # Pass the chosen_products list to print_recap
    return result


def ask_yes_no(question):
    """
    Asks a yes/no question.

    Args:
        question (str): Question to ask.

    Returns:
        bool: True if the response is 'yes', False otherwise.
    """
    while True:
<<<<<<< HEAD
            response = input(f"{question} (yes/no): ").strip().lower()
            if response in ["yes", "no"]:
                return response == "yes"
            print("⚠️ Invalid response. Please enter 'yes' or 'no'.")
=======
        response = input(f"{question} (yes/no): ").strip().lower()
        if response in ["yes", "no"]:
            return response == "yes"
        print("⚠️ Invalid response. Please enter 'yes' or 'no'.")

def ask_yes_no_stop(question):
    """
    Asks a yes/no/stop question.

    Args:
        question (str): Question to ask.

    Returns:
        str: 'yes', 'no', or 'stop' based on the user's response.
    """
    while True:
        response = input(f"{question} (yes/no/stop): ").strip().lower()
        if response == "yes":
            return "yes"
        elif response == "no":
            return "no"
        elif response == "stop":
            stop()
        else:
            print("⚠️ Invalid response. Please enter 'yes', 'no', or 'stop'.")

def stop():
    """
    Stops the program.
    """
    save_or_no = input("Do you want to save your order ? (yes/no): ").strip().lower()
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
>>>>>>> 6e699fb9bf9e0b398ee650cbae9afee42031c237

def propose_category(dishType, allergens, category_message):
    """
    Proposes dishes from a specific category and allows the user to add multiple items.

    Args:
        dishType (str): Type of dish (e.g., "entree", "plat principal").
        allergens (list): List of allergens to avoid.
        category_message (str): Message to display for the category.
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
                chosen_dish = dishNames[choice - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")

                # Ask if the user wants to see the ingredients
                see_ingredients = input("Do you want to see the ingredients of this dish? (yes/no): ").strip().lower()
                if see_ingredients == "yes":
<<<<<<< HEAD
                    ingredients = sorted(set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))
        
=======
                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))

>>>>>>> 3e6fda04ba4781d82fb0945782c449afabd29f75
                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for j, ingredient in enumerate(ingredients, 1):  # Numéroter les ingrédients
                            print(f"{j}. {ingredient}")

                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Ask if the user wants to validate the choice
                    validate_choice = input("Do you want to validate this choice? (yes/no): ").strip().lower()
                    if validate_choice == "yes":
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = input("Do you want to add another product from this category? (yes/no): ").strip().lower()
                if another != "yes":
                    return  # Exit after a valid choice
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")