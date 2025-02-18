from recap import print_recap, chosen_products

def validate_snack(products):
    chosen_product = input(f"Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)
    another_product = input("Do you want to choose another product? (yes/no): ").strip().lower()
    if another_product == "yes":
        validate_snack(products)
    else:
        print_recap()

def validate_product(products):
    chosen_product = input("Choose a product from the list above: ").strip()
    chosen_products.append(chosen_product)