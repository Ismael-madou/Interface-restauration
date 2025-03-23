from typing import List
from recap import print_recap
from menu import chosen_products  # Import the shared list from menu.py

def validate_snack(products: List[str]) -> None:
    """
    Validates the user's choice for a snack.

    Args:
        products (List[str]): List of available snacks.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)


    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products)
    else:
        print_recap()

def validate_product(products: List[str]) -> None:
    """
    Validates the user's choice for a product.

    Args:
        products (List[str]): List of available products.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)