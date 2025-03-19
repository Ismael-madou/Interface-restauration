import sys  # Import the sys module for sys.exit()
import pandas as pd
from pathlib import Path
from validation import validate_snack, validate_product
from recap import print_recap, ICONS
from shared_data import chosen_products  # Import the shared list
from allergies import filter_dishes_by_allergens, ask_allergies
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
# Define absolute paths
base_dir= Path(__file__).resolve().parent.parent
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
                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product?")
                if see_ingredients:
                    ingredients = sorted(set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))
        
                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for ingredient in ingredients:
                            print(f"- {ingredient}")

                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Ask if the user wants to validate the choice
                    validate_choice = ask_yes_no("Do you want to validate this choice?")
                    if validate_choice:
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = ask_yes_no("Do you want to add another snack?")
                if not another:
                    print("\n✅ We have taken your order into account.")
                    print_recap(chosen_products)  # Pass the chosen_products list to print_recap
                    return
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")

def propose_menu(allergens):
    """
    Proposes a full menu to the user based on allergens.

    Args:
        allergens (list): List of allergens to avoid.
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
                see_ingredients = ask_yes_no("Do you want to see the ingredients of this product ?")
                if see_ingredients:
                    ingredients = sorted(set(ingredients_data[ingredients_data['dish_name'] == chosen_dish]['product_name'].tolist()))
        
                    if ingredients:
                        print(f"\nIngredients of {chosen_dish}:")
                        for ingredient in ingredients:
                            print(f"- {ingredient}")

                    else:
                        print(f"\nNo ingredients found for {chosen_dish}.")

                    # Ask if the user wants to validate the choice
                    validate_choice = ask_yes_no("Do you want to validate this choice?")
                    if validate_choice:
                        chosen_products.append((choice, chosen_dish, dishType))
                else:
                    chosen_products.append((choice, chosen_dish, dishType))

                another = ask_yes_no("Do you want to add another product from this category?")
                if not another:
                    return  # Exit after a valid choice
            else:
                print("\n⚠️ Invalid choice. Please enter a valid number.")
        else:
            print("\n⚠️ Invalid input. Please enter a number or 'back'.")