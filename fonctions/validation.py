# validation.py
from recap import print_recap
from shared_data import chosen_products  # Import the shared list

def validate_snack(products):
    """
    Validates the user's choice of a snack.

    Args:
        products (list): List of available snacks.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)  # Add the chosen product to the shared list

    # Ask if the user wants to add another snack
    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products)  # Recursively call the function to add another snack
    else:
        print_recap(chosen_products)  # Display the order summary


def validate_product(products):
    """
    Validates the user's choice of a product.

    Args:
        products (list): List of available products.
    """
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)  # Add the chosen product to the shared list