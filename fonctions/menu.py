# menu.py
import pandas as pd
from pathlib import Path
import streamlit as st
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
    meal_type = st.radio(
        "Do you want a snack or a full meal?",
        options=["Snack", "Full Meal"],
    )

    if meal_type == "Snack":
        propose_snack(allergens)
        # Offer a full meal after snacks
        if st.button("Would you also like a full meal?"):
            propose_menu(allergens)
    else:
        propose_menu(allergens)

def propose_snack(allergens):
    """
    Proposes snacks to the user based on allergens.
    """
    show_most_ordered_dishes_image()

    dishType = "snack"
    dishNames = menu_data[menu_data['meal_type'] == dishType]['dish_name'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)

    st.write("Here are the snack options:")
    for i, dish in enumerate(dishNames, 1):
        st.write(f"{i}. {dish}")

    choice = st.number_input("Choose a product by entering its number:", min_value=1, max_value=len(dishNames))
    if choice:
        st.write(f"You have chosen: {dishNames[choice - 1]}")
        chosen_products.append((choice, dishNames[choice - 1], dishType))

        if st.button("Add another snack"):
            propose_snack(allergens)

def propose_menu(allergens):
    """
    Proposes a full meal to the user based on allergens.
    """
    if st.checkbox("📌 1. Do you want a starter?"):
        propose_category("entree", allergens, "🥗 Here are the available starters:")
    if st.checkbox("📌 2. Do you want a main course?"):
        propose_category("plat principal", allergens, "🍛 Here are the available main courses:")
    if st.checkbox("📌 3. Do you want a side dish?"):
        propose_category("garniture", allergens, "🍚 Here are the available side dishes:")
    if st.checkbox("📌 4. Do you want a dessert?"):
        propose_category("dessert", allergens, "🍰 Here are the available desserts:")
    if st.checkbox("📌 5. Do you want bread?"):
        propose_category("pain", allergens, "🍞 Here are the available types of bread:")
    if st.checkbox("📌 6. Do you want a supplement?"):
        propose_category("autre", allergens, "➕ Here are the available supplements:")

    st.write("✅ We have taken your order into account.")
    print_recap(chosen_products)

def propose_category(dishType, allergens, category_message):
    """
    Proposes dishes from a specific category and allows the user to add multiple items.
    """
    dishNames = menu_data[menu_data['dish_type'] == dishType]['dish_name'].drop_duplicates().tolist()
    dishNames = filter_dishes_by_allergens(dishNames, allergens)

    st.write(category_message)
    for i, dish in enumerate(dishNames, 1):
        st.write(f"{i}. {dish}")

    choice = st.number_input("Choose a product by entering its number:", min_value=1, max_value=len(dishNames))
    if choice:
        st.write(f"You have chosen: {dishNames[choice - 1]}")
        chosen_products.append((choice, dishNames[choice - 1], dishType))

        if st.button("Add another item from this category"):
            propose_category(dishType, allergens, category_message)