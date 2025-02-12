import pandas as pd

menu_data = pd.read_excel('C:/Users/mathe/OneDrive/Documents/FAC/MASTER/S2/mana projet digitaux/data/antibes-menu-2025.xlsx')
ingredients_data = pd.read_excel('C:/Users/mathe/OneDrive/Documents/FAC/MASTER/S2/mana projet digitaux/data/antibes-plats-2025.xlsx')

chosen_products = []

def ask_meal():
    meal_type = input("Do you want a snack or a meal ? (snack/meal): ").strip().lower()
    if meal_type == "snack":
        propose_snack()
    elif meal_type == "meal":
        propose_menu()
    else:
        print("Invalid response. Please answer 'snack' or 'meal'.")
        ask_meal()

def propose_snack():
    dishType = "snack"
    dishNames = menu_data[menu_data['menuRepasType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the options for a snack:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_snack(dishNames)

def propose_menu():
    print("Do you want an entree? (yes/no): ")
    response = input().strip().lower()
    if response == "yes":
        propose_entree()
    propose_main_course()
    propose_side_dish()
    propose_dessert()
    propose_bread()
    propose_other()
    print("We have taken your order into account.")
    print_recap()

def propose_entree():
    dishType = "entree"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the available entrees:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_main_course():
    dishType = "plat principal"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the available main courses:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_side_dish():
    dishType = "garniture"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the available side dishes:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_dessert():
    dishType = "dessert"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the available desserts:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_bread():
    dishType = "pain"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Here are the available types of bread:")
    for dish in dishNames:
        print(f"- {dish}")
    validate_product(dishNames)

def propose_other():
    dishType = "autre"
    dishNames = menu_data[menu_data['menuPlatType'] == dishType]['menuPlatNom'].drop_duplicates().tolist()
    print("Do you want a supplement? (yes/no): ")
    response = input().strip().lower()
    if response == "yes":
        print("Here are the available supplements:")
        for dish in dishNames:
            print(f"- {dish}")
        validate_product(dishNames)

def validate_snack(products):
    chosen_product = input(f"Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)
    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products)
    else:
        print_recap()

def validate_product(products, is_first_call=False):
    if not is_first_call:
        print(f"Choose a product from the list above: ")
    chosen_product = input().strip()
    chosen_products.append(chosen_product)
    proceed_to_next = input("Do you want to proceed to the next step? (next/no): ").strip().lower()
    if proceed_to_next != "next":
        validate_product(products)

def print_recap():
    print("Here is a summary of your order:")
    for product in chosen_products:
        print(f"- {product}")

ask_meal()