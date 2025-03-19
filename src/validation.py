from typing import List
from recap import print_recap
from menu import chosen_products  # Import the shared list from menu.py

def validate_snack(products: List[str]) -> None:
    """
    Valide le choix de l'utilisateur pour un snack.

    Args:
        products (List[str]): Liste des snacks disponibles.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)  # Ajouter le produit choisi à la liste partagée

    # Demander si l'utilisateur veut ajouter un autre snack
    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products)  # Appel récursif pour ajouter un autre snack
    else:
        print_recap()  # Afficher le récapitulatif de la commande

def validate_product(products: List[str]) -> None:
    """
    Valide le choix de l'utilisateur pour un produit.

    Args:
        products (List[str]): Liste des produits disponibles.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)  # Ajouter le produit choisi à la liste partagée