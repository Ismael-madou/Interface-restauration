from Fonctions.recap import print_recap, chosen_products
from pathlib import Path
import pandas as pd
import os

# Chemin absolu du projet (remonte d'un niveau depuis le script)
BASE_DIR = Path(os.getcwd()).parent  # Remonte d'un niveau depuis le dossier actuel
print(BASE_DIR)
# Définit le dossier "Databases" (suppose qu'il est à la racine du projet)
DATABASE_DIR = BASE_DIR / "Databases"

# Chargement des fichiers Excel
menu = pd.read_excel(DATABASE_DIR / "antibes-menu-2025.xlsx")
dishes = pd.read_excel(DATABASE_DIR / "antibes-plats-2025.xlsx")

chosen_products = []

def validate_product(products, chosen_products):
    chosen_product = input("Choose a product from the list above: ").strip()
    if chosen_product in products:
        chosen_products.append(chosen_product)
    else:
        print(f"{chosen_product} is not a valid product. Please choose again.")
        validate_product(products, chosen_products)


def validate_snack(products, chosen_products):
    chosen_product = input(f"Choose a product from the list above: ").strip()
    if chosen_product in products:
        chosen_products.append(chosen_product)
    else:
        print(f"{chosen_product} is not a valid product. Please choose again.")
        validate_snack(products, chosen_products)

    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products, chosen_products)
