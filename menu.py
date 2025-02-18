import pandas as pd
from validation import validate_snack, validate_product
from recap import print_recap, chosen_products
from allergies import filter_dishes_by_allergens

menu_data = pd.read_excel('C:/Users/mathe/OneDrive/Documents/FAC/MASTER/S2/mana projet digitaux/data/antibes-menu-2025.xlsx')
ingredients_data = pd.read_excel('C:/Users/mathe/OneDrive/Documents/FAC/MASTER/S2/mana projet digitaux/data/antibes-plats-2025.xlsx')

def ask_meal(allergens):
    meal_type = input("Do you want a snack or a meal ? (snack/meal): ").strip().lower()
    if meal_type == "snack":
        propose_snack(allergens)
    elif meal_type == "meal":
        propose_menu(allergens)
    else:
        print("Invalid response. Please answer 'snack' or 'meal'.")
        ask_meal(allergens)

def propose_snack(allergens):
    dishType = "snack"
    dishNames = menu_data[menu_data['menuRepasType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the options for a snack:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_snack(dishNames)

def propose_menu(allergens):
    if ask_yes_no("Do you want a starter ?"):
        propose_starter(allergens)
    if ask_yes_no("Do you want a dishe?"):
        propose_dishe(allergens)
    if ask_yes_no("Do you want a side dish?"):
        propose_side_dish(allergens)
    if ask_yes_no("Do you want a dessert?"):
        propose_dessert(allergens)
    if ask_yes_no("Do you want bread?"):
        propose_bread(allergens)
    if ask_yes_no("Do you want a supplement?"):
        propose_other(allergens)
    print("We have taken your order into account.")
    print_recap()

def ask_yes_no(question):
    response = input(f"{question} (yes/no): ").strip().lower()
    return response == "yes"

def propose_starter(allergens):
    dishType = "entree"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available entrees:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_dishe(allergens):
    dishType = "plat principal"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available main courses:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_side_dish(allergens):
    dishType = "garniture"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available side dishes:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_dessert(allergens):
    dishType = "dessert"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available desserts:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_bread(allergens):
    dishType = "pain"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available types of bread:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_other(allergens):
    dishType = "autre"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)
    print("Here are the available supplements:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)