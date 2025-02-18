import pandas as pd

menu_data = pd.read_excel('C:/Users/mathe/OneDrive/Documents/FAC/MASTER/S2/mana projet digitaux/data/antibes-menu-2025.xlsx')

def ask_allergies():
    response = input("Do you have any allergies? (yes/no): ").strip().lower()
    if response == "yes":
        return get_allergens()
    return []

def get_allergens():
    allergens = set()
    for allergen_list in menu_data['allergene'].dropna():
        allergens.update(allergen.strip() for allergen in allergen_list.split(','))
    allergens = list(allergens)
    print("Here are the allergens present in our dishes:")
    for allergen in allergens:
        print(f"- {allergen}")
    selected_allergens = input("Please list the allergens you are allergic to, separated by commas: ").strip().lower().split(',')
    return [allergen.strip() for allergen in selected_allergens]

def filter_dishes_by_allergens(dishes, allergens):
    filtered_dishes = []
    for dish in dishes:
        dish_allergens = menu_data[menu_data['menuPlatNom'] == dish]['allergene'].values[0]
        if pd.isna(dish_allergens):
            dish_allergens = ""
        dish_allergens = [allergen.strip().lower() for allergen in dish_allergens.split(',')]
        if not any(allergen in dish_allergens for allergen in allergens):
            filtered_dishes.append(dish)
    return filtered_dishes