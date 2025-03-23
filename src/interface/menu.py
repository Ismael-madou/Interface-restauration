import sys
import pandas as pd
from pathlib import Path
from typing import List
from src.interface.allergies import filter_dishes_by_allergens
from src.interface.nutrients import show_nutrient_stats
from src.interface.recap import print_recap, ICONS
from src.interface.shared_data import chosen_products
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from src.interface.nutrients import display_chosen_products_nutrients

# Define absolute paths
base_dir= Path(__file__).resolve().parent.parent.parent
menu_file_path = base_dir / 'data' / 'processed' / 'menu.xlsx'
dishes_file_path = base_dir / 'data' / 'processed' / 'dishes.xlsx'

# Load Excel files
menu_data = pd.read_excel(menu_file_path)
ingredients_data = pd.read_excel(dishes_file_path)

def display_graph_image(image_path):
    """
    Displays a graph image in a graphical window.

    Args:
        image_path (str): The path to the graph image file to display.
    """
    try:

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"The image file '{image_path}' was not found.")


        img = mpimg.imread(image_path)


        plt.figure(figsize=(10, 6))
        plt.imshow(img)
        plt.axis('off')
        plt.title("Most Ordered Dishes")
        plt.tight_layout()


        plt.show(block=True)

    except FileNotFoundError as e:
        print(f"⚠️ Error: {e}")
    except Exception as e:
        print(f"⚠️ An error occurred while displaying the image: {e}")


if __name__ == "__main__":
    image_path = "docs/Dish_occurrences.png"
    display_graph_image(image_path)
def ask_meal(allergens):
    """
   Asks the user if they want a snack, a meal, or to view statistics.

    Args:
        allergens (List[str]): List of allergens to avoid.
    """
    while True:
        meal_type = input("Do you want a snack, a meal, or view stats? (snack/meal/stats/stop): ").strip().lower()

        if meal_type == "snack":
            propose_snack(allergens)
        elif meal_type == "meal":
            propose_menu(allergens)
        elif meal_type == "stats":
            show_nutrient_stats(allergens)

        elif meal_type == "stop":
            stop()
        else:
            print("\n⚠️ Invalid response. Please answer 'snack', 'meal', 'stats', or 'stop'.")




def propose_snack(allergens: List[str]) -> None:
    """
    Suggests snacks to the user based on allergens.

    Args:
        allergens (List[str]): List of allergens to avoid.
    """
    dishType = "snack"

    while True:
        dishNames = menu_data[menu_data['meal_type'] == dishType]['dish_name'].drop_duplicates().tolist()
        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print("\nHere are the options for a snack:")
        for i, dish in enumerate(dishNames, 1):
            print(f"🥪 {i}. {dish}")
        choice = input(
            "\nChoose a product by entering its number, or type 'back' to choose again, or 'stop' to exit: ").strip().lower()

        if choice == "back":
            return ask_meal(allergens)
        elif choice == "stop":
            stop()
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dishNames):
                chosen_dish = dishNames[choice - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")


                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product?")
                validate_choice = True
                if see_ingredients:
                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))

                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for i, ingredient in enumerate(ingredients, 1):
                            print(f"{i}. {ingredient}")


                        remove_ingredients = ask_yes_no("\nDo you want to remove any ingredients?")
                        if remove_ingredients:
                            print("\nEnter the numbers of the ingredients you want to remove (separated by commas):")
                            for i, ingredient in enumerate(ingredients, 1):
                                print(f"{i}. {ingredient}")
                            to_remove = input("Numbers: ").strip()
                            removed_indices = []
                            for num_str in to_remove.split(','):
                                num = num_str.strip()
                                if num.isdigit():
                                    idx = int(num) - 1
                                    if 0 <= idx < len(ingredients):
                                        removed_indices.append(idx)

                            removed_indices = sorted(set(removed_indices), reverse=True)
                            for idx in removed_indices:
                                if 0 <= idx < len(ingredients):
                                    del ingredients[idx]

                            has_allergen = any(ingredient in allergens for ingredient in ingredients)
                            if has_allergen:
                                print("\n⚠️ The modified dish still contains allergens. Please choose another snack.")
                                validate_choice = False
                            else:
                                print("\n✅ Ingredients removed successfully. The dish is now allergen-free.")
                                validate_choice = ask_yes_no("Do you want to validate this choice?")
                        else:
                            validate_choice = ask_yes_no("Do you want to validate this choice?")
                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")
                        validate_choice = ask_yes_no("Do you want to validate this choice?")

                if validate_choice:
                    chosen_products.append((choice, chosen_dish, dishType))
                    another = ask_yes_no("Do you want to add another snack?")
                    if not another:
                        print("\n✅ We have taken your order into account.")
                        print_recap()
                        return
                else:
                    another = ask_yes_no("Do you want to choose another snack?")
                    if not another:
                        print("\n✅ We have taken your order into account.")
                        print_recap()
                        return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number, 'back', or 'stop'.")

def propose_menu(allergens: List[str]) -> None:
    # ───────────────
    #  QUESTION 1
    # ───────────────
    while True:
        answer = input("📌 1. Do you want a starter? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("entree", allergens, "🥗 Here are the available starters:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Veuillez choisir entre 'yes', 'no' ou 'stop'.")

    # ───────────────
    #  QUESTION 2
    # ───────────────
    while True:
        answer = input("📌 2. Do you want a dish? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("plat principal", allergens, "🍛 Here are the available main courses:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Veuillez choisir entre 'yes', 'no' ou 'stop'.")

    # ───────────────
    #  QUESTION 3
    # ───────────────
    while True:
        answer = input("📌 3. Do you want a side dish? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("garniture", allergens, "🍚 Here are the available side dishes:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Please choose between 'yes', 'no', or 'stop'.")

    # ───────────────
    #  QUESTION 4
    # ───────────────
    while True:
        answer = input("📌 4. Do you want a dessert? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("dessert", allergens, "🍰 Here are the available desserts:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Please choose between 'yes', 'no', or 'stop'.")

    # ───────────────
    #  QUESTION 5
    # ───────────────
    while True:
        answer = input("📌 5. Do you want bread? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("pain", allergens, "🍞 Here are the available types of bread:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Please choose between 'yes', 'no', or 'stop'.")

    # ───────────────
    #  QUESTION 6
    # ───────────────
    while True:
        answer = input("📌 6. Do you want a supplement? (yes/no/stop): ").strip().lower()

        if answer == "yes":
            propose_category("autre", allergens, "➕ Here are the available supplements:")
            break
        elif answer == "no":
            break
        elif answer == "stop":
            stop()
            return
        else:
            print("⚠️ Please choose between 'yes', 'no', or 'stop'.")


    print("\n✅ We have taken your order into account.")
    print_recap()



def ask_yes_no(question: str) -> bool:
    """
    Asks a yes/no question to the user.

    Args:
        question (str): The question to ask.

    Returns:
        bool: True if the answer is 'yes', False otherwise.
    """
    while True:
        response = input(f"{question} (yes/no): ").strip().lower()
        if response in ["yes", "no"]:
            return response == "yes"
        print("⚠️ Invalid response. Please enter 'yes' or 'no'.")


def ask_yes_no_stop(question: str) -> str:
    """
    Asks a yes/no/stop question to the user.

    Args:
        question (str): The question to ask.

    Returns:
        str: 'yes', 'no', or 'stop' based on the user's response.
    """
    while True:
        response = input(f"{question} (yes/no/stop): ").strip().lower()
        if response in ["yes", "no", "stop"]:
            return response
        print("⚠️ Invalid response. Please enter 'yes', 'no', or 'stop'.")


def stop() -> None:
    save_or_no = input("Do you want to save your order? (yes/no): ").strip().lower()

    if save_or_no == "yes":
        print("\nHere is a summary of your order:")
        for index, product in enumerate(chosen_products, start=1):
            choice, chosen_dish, dishType, included_ingredients, removed_ingredients = product
            icon = ICONS.get(dishType, "❓")
            print(f"{icon} {dishType.capitalize()}: {chosen_dish} ({index})")

            if included_ingredients:
                print(f"   ✔️ Ingredients: {', '.join(included_ingredients)}")

            if removed_ingredients:
                print(f"   ❌ Removed: {', '.join(removed_ingredients)}")

        display_chosen_products_nutrients()

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
    while True:

        dishNames = menu_data[menu_data['dish_type'] == dishType]['dish_name'].drop_duplicates().tolist()

        dishNames = filter_dishes_by_allergens(dishNames, allergens)

        print(f"\n{category_message}")
        for i, dish in enumerate(dishNames, 1):
            print(f"{i}. {dish}")

        choice = input(
            "\nChoose a product by entering its number, or type 'back' to return, or 'stop' to exit: "
        ).strip().lower()

        if choice == "back":

            return
        elif choice == "stop":

            stop()
        elif choice.isdigit():

            choice_num = int(choice)
            if 1 <= choice_num <= len(dishNames):
                chosen_dish = dishNames[choice_num - 1]
                print(f"\n✅ You have chosen: {chosen_dish}")

                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product?")
                if see_ingredients:

                    ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist())
                    )
                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for idx, ing in enumerate(ingredients, 1):
                            print(f"{idx}. {ing}")
                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")


                    removed_ingredients = []


                    remove_ingredient = ask_yes_no("Do you want to remove any ingredient from this dish?")
                    if remove_ingredient:
                        while True:
                            print("\nHere are the current ingredients:")
                            for idx, ing in enumerate(ingredients, 1):
                                print(f"{idx}. {ing}")

                            to_remove = input(
                                "Enter the number of the ingredient to remove (or 'done' if finished): "
                            ).strip().lower()

                            if to_remove == "done":

                                break

                            if to_remove.isdigit():
                                num = int(to_remove)
                                if 1 <= num <= len(ingredients):
                                    removed_item = ingredients.pop(num - 1)
                                    removed_ingredients.append(removed_item)
                                    print(f"Removed: {removed_item}")
                                else:
                                    print("⚠️ Invalid number.")
                            else:
                                print("⚠️ Please enter a valid number or 'done'.")

                    print("\nFinal ingredient list for this dish:")
                    for idx, ing in enumerate(ingredients, 1):
                        print(f"{idx}. {ing}")

                    validate_choice = ask_yes_no("Do you want to validate this choice?")
                    if validate_choice:
                        chosen_products.append((
                            choice_num,
                            chosen_dish,
                            dishType,
                            ingredients,         # Liste des ingrédients restants
                            removed_ingredients  # Liste des ingrédients supprimés
                        ))
                else:


                    all_ingredients = sorted(
                        set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist())
                    )

                    chosen_products.append((
                        choice_num,
                        chosen_dish,
                        dishType,
                        all_ingredients,
                        []
                    ))


                another = ask_yes_no("Do you want to add another product from this category?")
                if not another:

                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number, 'back', or 'stop'.")
