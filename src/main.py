# main.py
from menu import ask_meal, display_graph_image
from allergies import ask_allergies
from recap import welcome_message, print_recap  # Import the print_recap function
from visualization import display_graph_image  # Import the visualization function
from shared_data import chosen_products  # Import the shared list
from pathlib import Path
print(welcome_message)
if __name__ == "__main__":
        # Display the graph image
    image_path = "docs/Dish_occurrences.png"  
    display_graph_image(image_path)
    """
    Point d'entrée du programme. Demande à l'utilisateur ses allergies et propose un menu.
    Après que l'utilisateur a terminé sa commande, affiche un récapitulatif et une image de graphique.
    """
    while True:
        
        allergens = ask_allergies()
        ask_meal(allergens)

        # Afficher le récapitulatif de la commande
        recap_result = print_recap()
        if recap_result == "continue":
            continue  # Redémarrer le processus

    